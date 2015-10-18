from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from urllib.request import Request, urlopen
from urllib.parse import quote

from dotFoods import settings
from wikiboto.utils import can_access
from wikipage.models import \
    WikiList, WikiPage, WikiCategory

from bs4 import BeautifulSoup


def show(request, url_name):
    try:
        page = WikiPage.objects.get(url_name=url_name)
        return render(request, 'wikipage/show.html',
                      {'title': page.title,
                       'body': page.body,
                       'lists': page.lists,
                       'categories': page.categories})

    except ObjectDoesNotExist:
        url = "https://en.wikipedia.org/wiki/" + quote(url_name)
        if can_access(url):
            req = Request(
                url, data=None,
                headers={
                    'User-Agent': settings.USER_AGENT,
                })
            response = urlopen(req).read()
            page = BeautifulSoup(response, 'html.parser')
            title = str(page.find(id='firstHeading').string)
            body = page.find(id='bodyContent')
            for edits in body.find_all(class_='mw-editsection'):
                edits.extract()
            body.find(id='jump-to-nav').extract()
            return render(request, 'wikipage/show.html',
                          {'title': title,
                           'body': str(body)})
        else:
            return HttpResponseRedirect(url)

