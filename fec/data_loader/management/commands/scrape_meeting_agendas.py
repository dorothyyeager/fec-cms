from typing import Callable, List, NamedTuple, Tuple
from datetime import datetime
from dateutil import parser as dparser
from lxml.html import fromstring, tostring, Element  # type: ignore
from operator import attrgetter
from urllib.parse import urljoin, urlparse
import json
import re
import requests


from ipdb import set_trace as st


"""
This script scrapes <www.fec.gov>'s Commission Meetings content and outputs a
JSON array containing one object literal per individual meeting agenda.

Steps:

#.  From a starting URL, follows appropriate links to find all of the links to
    individual meetings.

    (Note that http://www.fec.gov/agenda/2016/agendas2016.shtml has a number of
    broken links on it, and incomplete content.)
#.  From each list of links to meetings, acquire:

    +   The date of the meeting.
    +   The current URL for the meeting documents.
    +   The URL for the draft minutes of the meeting.
    +   The date of the approved minutes of the meeting.
    +   The URL for the approved minutes of the meeting.
    +   Any URLs (and their titles) for associated Sunshine Act Notices.

    All URLs will need to be cleaned and/or verified.
#.  Given the above data for each meeting, get the HTML for its meeting
    documents page and from it acquire:

    +   The URL for its full audio, if available.
    +   The URL for the full video, if available.
    +   The URL for the closed captioning text, if available.
    +   The main body of HTML for the page.
    +   The PDF disclaimer as a separate property?
    +   A list of links (text and URL) of documents from the meeting.

    All URLs will need to be cleaned and/or verified.
#.  Turn each instance of that data into a Meeting object.
#.  Serialize the list of Meeting objects to JSON.
    Optionally also serialize the list of broken URLs to JSON.
"""

Date = NamedTuple(
    "Date",
    [
        ("datetime", datetime),  # Python datetime.datetime object
        ("iso8601", str),  # ISO 8601 date, e.g.  ("2016-12-13")
        ("original", str),  # The original form of the date string
        ("source", str)  # Where we actually got the date info from
    ])

Link = NamedTuple(
    "Link",
    [
        ("text", str),  # The text of the link
        ("title", str),  # The value of the link's title attribute, if any
        ("url", str)  # URL
    ])
Links = List[Link]

Meeting = NamedTuple(
    "Meeting",
    [
        ("agenda_documents_linked", Links),  # list (Links)
        ("approved_minutes_date", str),  # ISO 8601 date, e.g.  ("2016-12-13")
        ("approved_minutes_url", str),  # URL
        ("audio_url", str),  # URL
        ("body", str),  # HTML,
        ("closed_captioning_url", str),  # URL
        ("draft_minutes_links", Links),  # list (Links)
        ("link_title_text", str),  # Plain text
        ("pdf_disclaimer", str),  # HTML ?? Not sure about this one.
        ("posted_date", str),  # ISO 8601 date, such as ("2016-12-13")
        ("previous_url", str),  # URL
        ("sunshine_act_links", Links),  # list (Links)
        ("title_text", str),  # HTML
        ("video_url", str)  # URL
    ])
Meetings = List[Meeting]

"""
The following are URLs I identified as broken in the first pass and found
working equivalents of, so during the "write fully-qualified URLs" stage the
script replaces the broken ones with the working equivalents.
"""
urls_to_change = {

    "http://www.fec.gov/agenda/2014/approved_14-2-a.pdf":
    None,

    "http://www.fec.gov/agenda/2014/approved_14-1-a.pdf":
    None,

    "http://www.fec.gov/sunshine/2013/notice20131205.pdf":
    None,

    "http://www.fec.gov/sunshine/2012/notice20120711.pdf":
    None,

    "http://www.fec.gov/sunshine/2012/notice20120315.pdf":
    None,

    "http://www.fec.gov/agenda/2010/2011/mtgdoc1101.pdf":
    "http://www.fec.gov/agenda/2011/mtgdoc1101.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20091210.pdf":
    "http://www.fec.gov/sunshine/2009/notice20091210.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20091202.pdf":
    "http://www.fec.gov/sunshine/2009/notice20091202.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20091117.pdf":
    "http://www.fec.gov/sunshine/2009/notice20091117.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20091103.pdf":
    "http://www.fec.gov/sunshine/2009/notice20091103.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20091027.pdf":
    "http://www.fec.gov/sunshine/2009/notice20091027.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20091001.pdf":
    "http://www.fec.gov/sunshine/2009/notice20091001.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090917.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090917.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090820.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090820.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090722.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090722.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090709.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090709.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090617.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090617.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090610.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090610.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090512.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090512.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090501.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090501.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090428.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090428.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090417.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090417.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090409.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090409.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090313.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090313.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090306.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090306.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090227.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090227.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090205.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090205.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090122.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090122.pdf",

    "http://www.fec.gov/agenda/sunshine/2009/notice20090107.pdf":
    "http://www.fec.gov/sunshine/2009/notice20090107.pdf",

    "http://www.fec.gov/agenda/sunshine/2008/notice20081231.pdf":
    "http://www.fec.gov/sunshine/2008/notice20081231.pdf"

}


def cli_main(args: list=None) -> None:
    base_url = "http://www.fec.gov/agenda/agendas.shtml"
    annual_urls = [base_url] + extract_annual_urls(base_url)
    meetings = []
    broken_links = []
    for url in annual_urls:
        url_meetings, url_broken_links = extract_meeting_metadata(url,
                                                                  broken_links)
        meetings.extend(url_meetings)
        broken_links.extend(broken_links)
        # meetings.extend(extract_meeting_metadata(url))
    fulldates = []
    strdates = []
    badmeetings = []
    goodmeetings = []
    agendameetings = []
    noticemeetings = []

    for meeting in meetings:
        if type(meeting) == Meeting:
            date = meeting.posted_date
            if type(date) == Date:
                fulldates.append((date.original, date.source, date.iso8601))
                goodmeetings.append(meeting)
            else:
                strdates.append(date)
                badmeetings.append(meeting)
        else:
            badmeetings.append(meeting)

    def is_notice_meeting(m):
        no_url = m.previous_url in (None, "")
        no_minutes = m.approved_minutes_url in (None, "")
        sunshine_links = len(m.sunshine_act_links) > 0
        return no_url and no_minutes and sunshine_links

    for meeting in goodmeetings:
        if is_notice_meeting(meeting):
            noticemeetings.append(meeting)
        else:
            agendameetings.append(meeting)

    # all_links, tried_links, broken_links = [], [], []

    # print("Link testing")

    """
    for meeting in goodmeetings:
        if meeting.approved_minutes_url is not None:
            url = meeting.approved_minutes_url
            all_links.append(meeting.approved_minutes_url)
            if meeting.approved_minutes_url not in tried_links:
                tried_links.append(meeting.approved_minutes_url)
                try:
                    response = requests.head(url)
                    if response.status_code != 200:
                        broken_links.append(url)
                except:
                    broken_links.append(url)

        for link in meeting.draft_minutes_links:
            url = link.url
            if url not in tried_links:
                try:
                    response = requests.head(url)
                    if response.status_code != 200:
                        broken_links.append(url)
                except:
                    broken_links.append(url)
        for link in meeting.sunshine_act_links:
            url = link.url
            if url not in tried_links:
                try:
                    response = requests.head(url)
                    if response.status_code != 200:
                        broken_links.append(url)
                except:
                    broken_links.append(url)
    """

    st()


def extract_annual_urls(url: str) -> List[str]:
    # response = requests.get(url)
    # content = response.content
    # html = fromstring(content)
    html = fromstring(requests.get(url).content)
    links = html.xpath("//ul/li/a[text()[contains(.,'Open Meetings')]]")
    urls = [urljoin(url, link.attrib["href"]) for link in links]
    return urls


def parse_a_element(a_el: Callable) -> Link:
    text = a_el.text_content()
    url = a_el.attrib["href"]
    title = ""
    if "title" in a_el.attrib:
        title = a_el.attrib["title"]
    return Link(text=text, title=title, url=url)


def d_to_iso(d: str, original: str=None) -> Date:
    """
    ISO 8601 date format from FEC date string.
    """
    if original is None:
        original = d
    d = d.strip()
    d = d.replace("Ocober", "October")

    try:
        dt = datetime.strptime(d, "%B %d, %Y")
    except:
        try:
            dt = dparser.parse(d)
        except:
            st()
            print(d)
            return Date(datetime=None, iso8601=None, original=original,
                        source=original)

    return Date(datetime=dt, iso8601=dt.strftime("%Y-%m-%d"),
                original=original, source=original)


def extract_date(a_el) -> str:
    """
    While most of the links are just "<month> <day>, <year>", some of them have
    other content, which we want to ignore.
    """
    url = a_el.attrib["href"]
    text = ("%s%s" % (a_el.text_content(),
                      a_el.tail if a_el.tail else "")).strip()
    # TODO: Should we also grab a_el.tail?
    datematch = re.match(r"[a-zA-Z]+[ ]+[0-9]{1,2},? ?[0-9]{4}", text)
    if datematch:
        datestring = datematch.group(0)
        return d_to_iso(datestring, original=text)
    else:
        # It has non-standard content.
        # st()
        path = urlparse(url).path
        name = path.split("/")[-1]
        name_base = name.split(".")[0]
        if "agenda" in name_base:
            date = name_base[6:]
            if "2000" in date:
                if date.startswith("2000"):
                    dt = datetime.strptime(date, "%Y%m%d")
                    print(date, dt.strftime("%Y-%m-%d"))
                elif date.endswith("2000"):
                    dt = datetime.strptime(date, "%m%d%Y")
                    print(date, dt.strftime("%Y-%m-%d"))
                    st()
            elif len(date) < 8:
                st()
            else:
                dt = datetime.strptime(date, "%Y%m%d")
            return Date(datetime=dt, iso8601=dt.strftime("%Y-%m-%d"),
                        original=text, source=name)
        elif "oral_hearing" in name_base:
            date = name_base[12:]
            dt = datetime.strptime(date, "%Y%m%d")
            return Date(datetime=dt, iso8601=dt.strftime("%Y-%m-%d"),
                        original=text, source=name)
        elif "notice" in name_base:
            date = name_base[6:]
            dt = datetime.strptime(date, "%Y-%m-%d")
            return Date(datetime=dt, iso8601=dt.strftime("%Y-%m-%d"),
                        original=text, source=name)
        else:
            st()


def parse_meeting_row(row: Callable) -> Meeting:
    """
    Given an ``lxml.html.Element`` object for the table row for a meeting,
    returns a ``Meeting`` object.
    """

    """
    There should be four columns:

    #.  Link to documents.
    #.  Link to draft minutes.
    #.  Link to approved minutes.
    #.  Link(s) to Sunshine Act notices.
    """
    # TODO: Have to redo this to accommodated the fact that some Sunshine
    # Notice links show up in the first cell (in addition to docs links).
    draft_minutes_links = []
    approved_minutes_date, approved_minutes_url = None, None
    sunshine_act_links = []
    cells = row.xpath("./td")
    if len(cells) == 4:
        docs, draft, approved, sunshine = cells
    elif len(cells) == 3:
        docs, approved, sunshine = cells
        draft = None
    elif len(cells) == 1 and "adobe reader" in row.text_content().lower():
        return "Adobe Reader"
    elif len(cells) == 2 and "approved minutes" in row.text_content().lower():
        return "Header Row"
    elif len(cells) == 2:
        docs, approved = cells
        draft = None
        sunshine = None
    else:
        st()

    docs_links = docs.xpath("./a")
    posted_date = None
    if len(docs_links) > 0:
        """
        TODO:
            +   Handle 2010's cancellations
            +   Handle 2005's notices ending up in this cell
        """
        agenda_links = []
        for a_el in docs_links:
            href = a_el.attrib["href"]
            # TODO: there's at least one case where a link is repeated; if
            # we have two links with the same href, we should detect that
            # and combine all the text and pass that to extract_date()
            if "notice" in href:
                text = ("%s%s" % (a_el.text_content(),
                                  a_el.tail if a_el.tail else "")).strip()
                url = a_el.attrib["href"]
                # print(url)
                # All the 2009 links are broken:
                url = url.replace("fec.gov/agenda/", "fec.gov/")
                # print(url)
                sunshine_title = ""
                if "title" in a_el.attrib:
                    sunshine_title = a_el.attrib["title"]
                sunshine_act_links.append(Link(text=text, title=sunshine_title,
                                               url=url))
            elif "agenda" in href:
                title = ""
                if "title" in a_el.attrib:
                    title = a_el.attrib["title"]
                agenda_links.append((
                    "%s%s" % (a_el.text_content(),
                              a_el.tail if a_el.tail else ""),
                    extract_date(a_el), a_el.attrib["href"], title))
                """
                title_text = "%s%s" % (a_el.text_content(),
                                       a_el.tail if a_el.tail else "")
                posted_date = extract_date(a_el)
                previous_url = a_el.attrib["href"]
                """
            else:
                st()

        if len(agenda_links) == 1:
            title_text, posted_date, previous_url, title = agenda_links[0]
        elif len(agenda_links) > 1:
            links = [_[2] for _ in agenda_links]
            unique_links = set(links)
            if len(unique_links) != 1:
                st()
            else:
                best = max(agenda_links, key=lambda _: len(_[0].strip()))
                title_text, posted_date, previous_url, title = best

        if posted_date is None:
            # This means we've gone through the a elements in the cell and
            # they're all notices.
            previous_url = None
            title = ""
            title_text = docs.text_content().strip().replace(" ,", ",")
            datematch = re.match(r"[a-zA-Z]+ [0-9]{1,2}, [0-9]{4}",
                                 title_text)
            if datematch:
                datestring = datematch.group(0)
                posted_date = d_to_iso(datestring)
            else:
                st()

        """
        else:
            docs_link = docs_links[0]
            title_text = "%s%s" % (docs_link.text_content(),
                                   docs_link.tail if docs_link.tail else "")
            # posted_date = extract_date(docs_link).iso8601
            posted_date = extract_date(docs_link)
            previous_url = docs_link.attrib["href"]
            if "agenda" not in previous_url:
                st()
            assert "agenda" in previous_url
        """
    else:
        previous_url = None
        title = ""
        title_text = docs.text_content().strip().replace(" ,", ",")
        datematch = re.match(r"[a-zA-Z]+ [0-9]{1,2}, [0-9]{4}", title_text)
        if datematch:
            datestring = datematch.group(0)
            posted_date = d_to_iso(datestring)
        else:
            st()

    if draft is not None:
        draft_minutes_links = [parse_a_element(e) for e in draft.xpath("./a")]

    if len(approved.xpath("./a")) > 1:
        st()

    if len(approved.xpath("./a")) == 1:
        # TODO: Deal with 'Transcript Available'
        approved_link = approved.xpath("./a")[0]
        title_text = approved.text_content()
        datematch = re.match(r"[a-zA-Z]+ [0-9]{1,2}, [0-9]{4}", title_text)
        if datematch:
            datestring = datematch.group(0)
            approved_minutes_date = d_to_iso(datestring)
        else:
            approved_minutes_date = d_to_iso(
                approved_link.text_content()).iso8601

        approved_minutes_url = approved_link.attrib["href"]

    if sunshine is not None and len(sunshine.xpath("./a")) > 0:
        for sunshine_link in sunshine.xpath("./a"):
            text = sunshine_link.text_content()
            url = sunshine_link.attrib["href"]
            # print(url)
            # All the 2009 links are broken:
            url = url.replace("fec.gov/agenda/", "fec.gov/")
            # print(url)
            sunshine_title = ""
            if "title" in sunshine_link.attrib:
                sunshine_title = sunshine_link.attrib["title"]
            sunshine_act_links.append(Link(text=text, title=sunshine_title,
                                           url=url))

    if len(sunshine_act_links) > len(set([_.url for _ in sunshine_act_links])):
        # We have more than one link to the same thing for the Sunshine Act
        # Notices.
        sunshine_act_links = [max(sunshine_act_links,
                                  key=lambda _: len(_.text.strip()))]

    return Meeting(
        agenda_documents_linked=[],
        approved_minutes_date=approved_minutes_date,
        approved_minutes_url=approved_minutes_url,
        audio_url=None,
        body=None,
        closed_captioning_url=None,
        draft_minutes_links=draft_minutes_links,
        link_title_text=title,
        pdf_disclaimer=None,
        posted_date=posted_date,
        previous_url=previous_url,
        sunshine_act_links=sunshine_act_links,
        title_text=title_text,
        video_url=None)


def extract_meeting_metadata(url: str,
                             broken_links: List) -> Tuple[Meetings, List]:
    """
    This will get all the metadata possible about meetings from the annual
    pages.
    """
    exprs = [
        "//table[@class='agenda_table'][@summary='Data table']",
        "//table[@summary='Data table']",
        "//table[@border='0'][@width='60%']"
    ]

    html = fromstring(requests.get(url).content)
    tables, count = [], 0
    while len(tables) != 1 and count < len(exprs):
        tables = html.xpath(exprs[count])
        count = count + 1
    if not len(tables):     # Work around this URL going down randomly
                            # http://www.fec.gov/agenda/2010/agendas2010.shtml
        print("%s not working" % url)
        return []
    if not len(tables) == 1:
        import ipdb
        ipdb.set_trace()
    table, broken_links = fix_urls(tables[0], url, broken_links,
                                   urls_to_change)

    all_rows = table.xpath(".//tr")
    # We don't want header rows:
    rows = [r for r in all_rows if "th" not in
            [e.tag for e in r.iterchildren()]]
    meetings = []
    for row in rows:
        if row is not None and row.text_content().strip():
            meetings.append(parse_meeting_row(row))
    return (meetings, broken_links)


"""
html.xpath("//table[@class='agenda_table'][@summary='Data table']")
"""


def extract_archive_urls(base_url: str, archive_urls: list=[],
                         visited: list=[]):
    """
    Identifies the list on the base_url page, then follows the links from that,
    looking for more links.

    (The full list of URLs isn't available on any one page and has to be
    collated from several sources.)

    Each of the URLs can itself contain more links to more URLs, which is why
    we need both ``archive_urls`` and ``visited``.

    Recursively calls itself, removing from the ``archive_urls`` list and
    adding to the ``visited`` list, while each pass adds to ``archive_urls``,
    until each URL has been added.

    :arg str base_url: The URL for the starting point.
    :arg list[str] archive_urls: List of URLs of "archive" pages, i.e. pages
        containing Tips for Treasurers and/or links to Tips for Treasurers
        pages.
    :arg list[str] visited: List of URLs that the script has acquired from the
        various pages. When done, this holds the full list of unique URLs to
        read Tips for Treasurers from.

    :rtype: tuple[list, list]
    :returns: A pair of lists, the first of which should be empty when the last
        iteration of the function is done.

    Impure
        Requests content from the URLs.
    Side effects
        Makes HTTP requests.
    """
    base_response = requests.get(base_url)
    base_content = base_response.content
    base_html = fromstring(base_content)

    # Check for ``li`` elements containing ``a`` elements whose ``href``
    # properties, lower-cased, contain "tipsarchive":
    links = base_html.xpath("//li/a")
    tip_links = [link for link in links if "tipsarchive" in
                 link.attrib["href"].lower()]
    tip_urls = [urljoin(base_url, link.attrib["href"]) for link in tip_links]

    # Add the URLs from the first page:
    for tip_url in tip_urls:
        # Since we're grabbing the entire page, we strip fragments.
        parsed = urlparse(tip_url)
        bare = "%s://%s%s" % (parsed.scheme, parsed.netloc, parsed.path)
        if bare not in archive_urls:
            archive_urls.append(bare)

    # Recursively go through the other pages:
    while archive_urls:
        next_url = archive_urls.pop()
        if next_url not in visited:
            visited.append(next_url)
            archive_urls, visited = extract_archive_urls(next_url,
                                                         archive_urls, visited)

    return (archive_urls, visited)


def extract_tips(tip_urls: list, urls_to_change: dict):
    """
    Pass each URL to ``parse_tips_from_page()``, accumulating lists of parsed
    tips and of URLs from the pages that don't appear to work.

    :arg list[str] tip_urls: The URLs for pages containing the tips.
    :arg dict[str, str] urls_to_change: Known broken URLs and their
        replacements.

    :rtype: tuple[list, list]
    :returns: A tuple containing a list of ``tip`` objects and a list of URLs
        that are apparently broken.
    """
    tips, broken_urls = [], []  # type: List[Tip], List[str]
    for tip_url in tip_urls:
        tips, broken_urls = parse_tips_from_page(tip_url, tips, broken_urls,
                                                 urls_to_change)
    return (tips, broken_urls)


def parse_tips_from_page(tip_url: str, tips: list, broken_urls: list,
                         urls_to_change: dict):
    """
    Parse the list of tips from the page. Note that some URLs (such as
    <http://www.fec.gov/info/TimelyTipsArchive.shtml>) don't have any actual
    tips on them.

    :arg str tip_url: The URL for the page supposedly containing tips.
    :arg list[Tip] tips: The list of ``Tip`` objects, which this adds to.
    :arg list[str] broken_urls: The list of broken URLs, which this adds to.
    :arg dict[str, str] urls_to_change: The list of known broken URLs and
        replacements.

    :rtype: tuple[list, list]
    :returns: A tuple containing a list of ``tip`` objects and a list of URLs
        that are apparently broken.

    Impure
        Reads content from the page.
    Side effects
        Makes HTTP requests.
    """
    response = requests.get(tip_url)
    encoding = response.encoding if response.encoding else "utf-8"
    html = fromstring(response.content)
    rows = html.xpath("//div[@id='fec_mainContent']/table//tr")

    for row in rows:
        if len(row.xpath("./td")) == 2:
            # All the rows we want have exactly two cells.
            date_cell, body_cell = row.xpath("./td")
            datestamp = None
            try:
                date_text = date_cell.text_content().strip()
                # At least one date has a period instead of a comma...
                if "." in date_text:
                    datestamp = datetime.strptime(date_text, "%B %d. %Y")
                else:
                    datestamp = datetime.strptime(date_text, "%B %d, %Y")
                # ISO 8601:
                datestr = datestamp.strftime("%Y-%m-%d")
            except ValueError as err:
                print(err)
            # If cell one has a date we can parse, cell two is the tip content.
            if datestamp:
                # Fix the URLs before parsing the HTML:
                tip_cell, broken_urls = fix_urls(body_cell, tip_url,
                                                 broken_urls, urls_to_change)
                tips.append(parse_tip(tip_url, datestr, tip_cell, encoding))

    return (tips, broken_urls)


def parse_tip(url: str, datestamp: str, cell: Element, encoding: str):
    """
    Create a ``Tip`` object out of the information we have and the HTML element
    for the table cell.

    The majority of the cells open with a ``strong`` element whose content is
    the title, but the HTML isn't completely consistent.

    If that element is there, we want its contents (as HTML) and then the
    remaining contents of the cell (also as HTML), but we want the contents as
    a string, stripped of the opening and closing tags.

    :arg str url: The URL for the page.
    :arg str datestamp: ISO 8601 date for the tip.
    :arg Element cell: ``lxml.html.Element`` object, HTML for the table cell.
    :arg str encoding: The encoding for the page.

    :rtype: Tip
    :returns: The parsed tip as a ``Tip`` object.
    """
    children = [_ for _ in cell.iterchildren()]
    first = children[0]
    # The ``strong`` element is often the first child:
    if first.tag == "strong":
        tail = "%s " % first.tail.strip() if first.tail else ""
        title = innerhtml(first)
        new_children = children[1:]
    # But sometimes there's an enclosing ``p`` element:
    elif first.tag == "p":
        strong = first.xpath("./strong")[0]
        title = innerhtml(strong)
        tail = "%s " % strong.tail.strip() if strong.tail else ""
        # Note: none of the ``p`` elements have trailing content, so we don't
        # have to worry about first.tail.
        new_children = [_ for _ in first.iterchildren()][1:]
    # And sometimes there's no ``strong`` element at all:
    elif "strong" not in [_.tag for _ in children]:
        # Some of the early tips don't have titles.
        title_date = datetime.strptime(datestamp,
                                       "%Y-%m-%d").strftime("%B %d, %Y")
        title = "Timely Tip for %s" % title_date
        tail = ""
        new_children = children
    # We don't know what to do if none of those conditions are met.
    else:
        raise

    # Now we want the rest of the HTML (not quite the same as ``innerhtml()``)
    body = "%s%s" % (tail, "".join([tostring(c).decode(encoding) for
                                    c in new_children]))

    return Tip(body=body.strip(), posted_date=datestamp, previous_url=url,
               title_text=title.strip())


def innerhtml(el: Element, encoding: str="utf-8"):
    """
    Returns the HTML of an element as a ``str``, with the opening and closing
    tags removed.

    :arg Element el: ``lxml.html.Element`` object.
    :arg str encoding: The character encoding for the HTML.

    :rtype: str
    :returns: A string of HTML without the opening and closing tags.
    """
    children = [_ for _ in el.iterchildren()]
    if not len(children):
        return el.text_content()
    text = "%s" % el.text if el.text else ""
    return "%s%s" % (text, "".join([tostring(c).decode(encoding) for
                                    c in el.iterchildren()]))


def fix_urls(el: Element, base_url: str, broken_urls: list,
             urls_to_change: dict) -> Tuple[Callable, List]:
    """
    Given an HTML element, turns all ``href`` parameters of ``a`` elements
    inside it into fully-qualified absolute URLs instead of the relative paths
    that are common in the tips content.

    :arg Element el: ``lxml.html.Element`` object, the content to change.
    :arg str base_url: The URL for the page, which serves as the absolute
        point with which to calculate the absolute paths.
    :arg list broken_urls: The list of broken URLs to add to as we find them.
    :arg dict[str, str] urls_to_change: Known broken URLs and their
        replacements.

    :rtype: tuple[Element, list]
    :returns: The Element with its ``a`` elements altered, and the list of
        broken URLs.
    """
    tested_urls = []  # type: List[str]
    for desc in el.iterdescendants():
        if desc.tag == "a" and "href" in desc.attrib:
            # Some of the links had line breaks in them:
            url = desc.attrib["href"].strip()
            fixed_url, tested_urls, broken_urls = fix_url(
                base_url, url, tested_urls, broken_urls,
                urls_to_change)
            desc.attrib["href"] = fixed_url
    return (el, broken_urls)


def fix_url(base_url: str, url: str, tested_urls: list, broken_urls: list,
            urls_to_change: dict):
    """
    Given an HTML element, turns all ``href`` parameters of ``a`` elements
    inside it into fully-qualified absolute URLs instead of the relative paths
    that are common in the tips content.

    Checks URLs against ``urls_to_change``, and substitutes the
    replacement URL if applicable.

    The line calling ``check_url()`` is commented out but left in because it's
    vaguely possible that re-scraping might be necessary at some point in the
    future when enough content has been added to warrant checking for broken
    links again.

    :arg str base_url: The URL for the page, which serves as the absolute
        point with which to calculate the absolute paths.
    :arg str url: The URL passed in, to be made absolute.
        If this is already a fully-qualified URL, it won't be altered.
    :arg list tested_urls: The list of URLs we've already tested.
    :arg list broken_urls: The list of broken URLs to add to as we find them.
    :arg dict[str, str] urls_to_change: Known broken URLs and their
        replacements.

    :rtype: tuple[str, list, list]
    :returns: The fixed and fully-qualified absolute URL, the list of tested
        URLs, and the list of broken URLs.

    Impure
        Via ``verify_url()``, reads from URLs to check whether or not they're
        working.
    Side effects
        Via ``verify_url()``, makes HTTP requests.
    """
    fixed_url = urljoin(base_url, url)
    if fixed_url in urls_to_change and urls_to_change[fixed_url] is not None:
        fixed_url = urls_to_change[fixed_url]
        tested_urls.append(fixed_url)
        return (fixed_url, tested_urls, broken_urls)
    if fixed_url in urls_to_change and urls_to_change[fixed_url] is None:
        tested_urls.append(fixed_url)
        broken_urls.append((base_url, fixed_url))
        return (fixed_url, tested_urls, broken_urls)
    # Uncomment the following two lines to re-enable checking for broken URLs:
    tested_urls, broken_urls = check_url(base_url, fixed_url,
                                         tested_urls, broken_urls)
    return (fixed_url, tested_urls, broken_urls)


def check_url(base_url: str, url: str, tested_urls: list, broken_urls: list):
    """
    Add the URL to ``tested_urls``, attempts to GET it, and if unsuccessful
    adds it to ``broken_urls``.

    :arg str base_url: The URL for the page that the URL to be checked was on.
    :arg str url: The URL to verify (should be a fully-qualified URL).
    :arg list tested_urls: The list of URLs we've already tested.
    :arg list broken_urls: The list of broken URLs to add to as we find them.

    :rtype: tuple[list, list]
    :returns: The the list of tested URLs and the list of broken URLs.

    Impure
        Reads from URLs to check whether or not they're working.
    Side effects
        Makes HTTP requests.
    """
    if url not in tested_urls:
        tested_urls.append(url)
        parsed_url = urlparse(url)
        if parsed_url.scheme in ("http", "https"):
            try:
                response = requests.head(url)
                if response.status_code != 200:
                    print(url)
                    broken_urls.append((base_url, url))
            except requests.exceptions.ConnectionError:
                print(url)
                broken_urls.append((base_url, url))

    return (tested_urls, broken_urls)


def write_tips(tips: list, broken_links: list) -> None:
    """
    Given a list of Tip objects, sorts them by date, converts them to JSON,
    and writes them to a file.

    If there are broken links, writes them to a file as well.

    :arg list articles: The list of Article objects.

    :rtype: None
    :returns: None

    Side effects
        Writes to the filesystem.
    """
    by_date = sorted(tips, key=attrgetter("posted_date"))
    out_lines = ",\n".join([json.dumps(t._asdict()) for t in by_date])
    out_string = "[\n%s\n]" % out_lines
    fname = datetime.now().strftime("tips--%Y-%m-%d-%H%M%S.json")
    with open(fname, "w+") as f:
        f.write(out_string)

    if len(broken_links) > 0:
        fname = datetime.now().strftime("tips--bad-urls--%Y-%m-%d-%H%M%S.json")
        with open(fname, "w+") as f:
            f.write(json.dumps(broken_links))

if __name__ == '__main__':
    cli_main()
