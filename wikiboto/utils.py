import re

from urllib import robotparser
from urllib.parse import urlparse, unquote

from dotFoods import settings

# wiki utils
def url_name_of(url):
    return unquote(str(url).split('/')[-1])

def url_name_of_cat(url):
    return unquote(str(url).split('/Category:')[-1])

# filters to get list href
def valid_parent(a):
    td = a.find_parent('td')
    if td and not a.previous_sibling:
        tr = td.find_parent('tr')
        if tr and not td.previous_sibling:
            return True

    li = a.find_parent('li')
    if li and not a.previous_sibling:
        return True

    return False

VALID_HREF = re.compile(r'^/wiki/[^:.?/#]+$')

LINK_FILTERS = (
    valid_parent,
    lambda a: VALID_HREF.match(a['href']),
    lambda a: not a.find_parent(class_='navbox'),
)

def bs_preprocess(html):
    """
    remove distracting whitespaces and newline characters
    https://groups.google.com/forum/#!topic/beautifulsoup/F3sdgObXbO4
    """
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    # remove leading and trailing whitespaces
    html = re.sub(pat, '', html)
    # convert newlines to spaces
    # this preserves newline delimiters
    html = re.sub('\n', ' ', html)
    # remove whitespaces before opening tags
    html = re.sub('[\s]+<', '<', html)
    html = re.sub('>[\s]+', '>', html)
    # remove whitespaces after closing tags
    return html

# setup robots.txt restrictions
ROBOT_PARSERS = {}
def can_access(url):
    robot_file = robot_file_of(url)
    if robot_file not in ROBOT_PARSERS:
        ROBOT_PARSERS[robot_file] = \
            robot_parser_for(robot_file)
    return ROBOT_PARSERS[robot_file].can_fetch(
        settings.USER_AGENT, url)

def robot_parser_for(robot_file):
    rp = robotparser.RobotFileParser()
    rp.set_url(robot_file)
    rp.read()
    return rp

def robot_file_of(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/' \
        .format(uri=parsed_uri)
    return domain + 'robots.txt'
