from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import bs4
from bs4 import BeautifulSoup


# test url = "https://github.com/about"
def remove_spaces_from_tags(tags):
    tags = tags.strip()
    return tags


def play_with_tags(soup):
    # print("all the li:\n\n", soup.li)
    # print(soup.li.get_text())

    # finds all the occurences of li
    # for line in soup.find_all("li"):
    # print(line.get_text())
    multiple_tags = input("enter multiple tags separated with comma: ")
    multiple_tags = multiple_tags.split(",")

    # using list comprehension to remove extra spaces from the tags
    some_list = [remove_spaces_from_tags(m_tags) for m_tags in multiple_tags]
    # print(some_list)

    res = soup.find_all(some_list)
    some_new_text = ""
    for some in res:
        some_new_text += some.text + "\n"

    print(some_new_text)

    # for m_tags in multiple_tags:
    # multiple_tags.replace(m_tags, m_tags.strip())
    # print(

    search = soup.footer
    relative_search = search.contents
    continuation_search = search.find_all("ul")

    if type(continuation_search) == bs4.element.ResultSet:
        print("yup dats true tho\n")
    else:
        print("that's false boiii\n")

    # print(continuation_search)
    print(
        "soup type: {},   search type: {},  continuation_search type: {},\
 relative_search type: {}".format(
            type(soup), type(search), type(continuation_search), type(relative_search)
        )
    )
    some_str = "hello"
    if type(some_str) == str:
        print("thats wussup")
    print(len(relative_search))
    # print("\n\n", relative_search[1].get_text())

    # print(search.get_text())

    # for string in continuation_search.stripped_strings:
    # print(repr(string))

    # print(soup)
    # print(soup.get_text())


def test_func():
    url = input("Enter url:")
    req = Request(url)
    result = ""

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
        result = html
    soup = BeautifulSoup(result, "html.parser")
    play_with_tags(soup)


if __name__ == "__main__":
    test_func()
