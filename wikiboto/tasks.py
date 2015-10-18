from urllib import request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from dotFoods.celery import app
from dotFoods import settings

from wikiboto.utils import \
    url_name_of, \
    url_name_of_cat,\
    LINK_FILTERS, \
    bs_preprocess, \
    can_access

from wikipage.models import \
    WikiList, WikiPage, WikiCategory

from wikiboto.models import BotoFinished

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@app.task(rate_limit=settings.RATE_LIMIT,
          time_limit=settings.TIME_LIMIT)
def crawl_page(url, parent=None, depth=0):
    # check if already crawled
    if BotoFinished.objects.filter(url=url).exists():
        if parent:
            try:
                page = WikiPage.objects.get(
                    url_name=url_name_of(url))
                wl, exist = WikiList.objects.get_or_create(
                    url_name=parent)
                page.lists.add(wl)
                page.save()
            except:
                logger.warning('list not added')
        return
    else:
        BotoFinished(url=url).save()

    if can_access(url):
        logger.info('Starting to crawl {0}'.format(url))
        req = request.Request(
            url, data=None,
            headers={
                'User-Agent': settings.USER_AGENT,
            })
        f = request.urlopen(req)
        process_page(url, f.read(), parent, depth)

    else:
        logger.warning('Banned to access {0}'.format(url))


@app.task
def process_page(url, raw, parent, depth):
    logger.info('Processing page {0}'.format(url))

    page = BeautifulSoup(raw, "html.parser")
    title = str(page.find(id='firstHeading').string)
    content = str(page.find(id='bodyContent'))

    if title.lower().startswith('list of') or \
       title.lower().startswith('lists of'):
        title = title.split('of ')[1]
        process_list(url, title, content, depth)

    else:
        process_article(url, title, content, parent)


@app.task
def process_list(url, title, raw_content, depth):
    if depth <= 0:
        logger.info('Reached depth limit: {0}'.format(title))
        return

    logger.info('Processing list {0}'.format(title))

    content = BeautifulSoup(
        bs_preprocess(raw_content), 'html.parser')

    url_name = url_name_of(url)
    WikiList.objects.get_or_create(
        url_name=url_name,
        defaults={'title': title})

    # remove noisy links
    link_list = [a for a in content.find_all('a')]
    for f in LINK_FILTERS:
        link_list = filter(f, link_list)

    # crawl all links of the list
    for link in link_list:
        abs_url = urljoin(url, link['href'])
        crawl_page.delay(abs_url, url_name, depth - 1)


@app.task
def process_article(url, title, raw_content, parent=None):
    logger.info('Processing article {0}'.format(title))

    content = BeautifulSoup(
        bs_preprocess(raw_content), 'html.parser')

    body = BeautifulSoup(raw_content, 'html.parser')
    for edits in body.find_all(class_='mw-editsection'):
        edits.extract()
    body.find(id='jump-to-nav').extract()
    body = BeautifulSoup(str(body), 'html.parser')

    page, exist = WikiPage.objects.get_or_create(
        url_name=url_name_of(url),
        defaults={
            'title': title,
            'origin': url})
    page.body = str(body)
    page.save()

    # add lists
    if parent:
        wl, exist = WikiList.objects.get_or_create(
            url_name=parent)
        page.lists.add(wl)

    # add categories
    for cat in content.find(id='mw-normal-catlinks')\
            .find_all('li'):
        url_name = url_name_of_cat(cat.find('a')['href'])
        if not url_name:
            continue
        wc, exist = WikiCategory.objects.get_or_create(
            url_name=url_name,
            defaults={'title': str(cat.text)})
        page.categories.add(wc)
