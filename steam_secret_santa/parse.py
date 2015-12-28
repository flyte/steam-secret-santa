import email
from urlparse import urlparse

from BeautifulSoup import BeautifulSoup


is_html_email = lambda msg: str(msg.get_content_type()).lower() == "text/html"


def parse_email_file(path):
    """
    Opens the email file and parses it with built-in email parser lib.

    @returns: email.message.Message object
    """
    return email.message_from_file(open(path))


def get_first_html_payload(email_msg):
    """
    Takes an email.message.Message instance and returns the first of its payloads which
    has a content-type of text/html.
    """
    try:
        return filter(is_html_email, email_msg.get_payload())[0]
    except IndexError:
        raise ValueError("None of the Email Messages had a content-type of text/html")


def parse_email_content(email_msg):
    """
    Takes an email.message.Message and returns a BeautifulSoup object containing its payload.
    """
    return BeautifulSoup(email_msg.get_payload())


def extract_gift_link_url(soup):
    """
    Takes a BeautifulSoup representation of the HTML Steam gift email and returns the gift link URL
    as an urlparse.ParseResult object.
    """
    try:
        gift_link = [x for x in soup.findAll("a") if "ackgift" in x.get("href", "")][0]
    except IndexError:
        raise ValueError("No link was found in the email containing 'ackgift'")
    return urlparse(gift_link["href"])


def strip_redeemer_qs_param(url, client=True):
    """
    Takes an urlparse.ParseResult object and rebuilds it without the redeemer querystring param.
    """
    client_string = "?client=1" if client else ""
    return urlparse("%s://%s%s%s" % (url.scheme, url.netloc, url.path, client_string))


def gift_link_url_from_email_file(path):
    """
    Take a path to a file containing a Steam gift email, parses it and returns the Steam
    gift link URL as an urlparse.ParseResult object.
    """
    msg = parse_email_file(path)
    pl = get_first_html_payload(msg)
    soup = parse_email_content(pl)
    url = extract_gift_link_url(soup)
    return strip_redeemer_qs_param(url)
