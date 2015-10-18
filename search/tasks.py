from bs4 import BeautifulSoup
from collections import Counter

from dotFoods.celery import app
from wikipage.models import WikiPage
from search.models import PageKeyword
from search.utils import tokenize

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@app.task
def parse_all():
    logger.info('Start parsing all pages')
    for page in WikiPage.objects.all():
        if not page.pagekeyword_set.exists():
            parse_page.delay(page.url_name)

@app.task
def parse_page(url_name):
    logger.info('Parsing ' + url_name)

    page = WikiPage.objects.get(url_name=url_name)

    # remove noisy info on the page
    soup = BeautifulSoup(page.body, 'html.parser')
    for class_name in ('reflist', 'citation',
                       'navbox', 'noprint',
                       'reference', 'vertical-navbox'):
        for item in soup.find_all(class_=class_name):
            item.extract()
    soup.find(id='siteSub').extract()
    soup = BeautifulSoup(str(soup), 'html.parser')

    # count and save
    tokens = tokenize(soup.get_text())
    counts, total = Counter(tokens), len(tokens)
    title_tokens = tokenize(page.title)
    t_counts, t_total = Counter(title_tokens), len(title_tokens)

    for keyword in counts:
        key = PageKeyword()
        key.keyword = keyword

        # Term Frequency: n / sum + tn / t_sum
        key.count = counts[keyword] / total
        if keyword in t_counts:
            key.count += t_counts[keyword] / t_total

        key.page = page
        key.save()

    for keyword in t_counts:
        if keyword in counts:
            continue

        key = PageKeyword()
        key.keyword = keyword
        key.count = t_counts[keyword] / t_total
        key.page = page
        key.save()
