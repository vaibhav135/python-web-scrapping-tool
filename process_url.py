from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def process_url_input(url):
    """taking url input"""
    process_running = True
    while process_running:
        req = Request(url)
        try:
            page = urlopen(req)
        except HTTPError as error:
            print("The server couldn't fulfill the request.")
            print("Error code: ", error.code)
        except URLError as error:
            print("We failed to reach a server.")
            print("Reason: ", error.reason)
        else:
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            return html
