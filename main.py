"""docstring."""
import os
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from colorama import Back, Fore, init

import check_html_tags

# url = "https://github.com/about"
init(autoreset=True)


def process_url_input():
    """taking url input"""
    process_running = True
    while process_running:
        url = input("\nplease enter the url: ")
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


def process_tags(tag, res):
    """process the tag input and update the result"""
    print("current tag: ", tag)


def show_options():
    """showing menu options"""
    pre_statement = "press one of the key given below: "
    options = {
        "s": "show menu again",
        "sw": "show web-scrapping options",
        "p": "print the html result",
        "c": "clear the screen",
        "q": "quit",
    }
    print(Back.LIGHTGREEN_EX + Fore.BLACK + "\n{}".format(pre_statement))
    for key, value in options.items():
        print(Fore.GREEN + "{}: {}".format(key, value))


def start_web_scrapping(res):
    """webscrapping"""
    stop = False
    while not stop:
        attr = input(Fore.LIGHTBLUE_EX + "\nenter any tag which you want to look for: ")
        res = check_html_tags.check_tag(attr)
        if res:
            process_tags(attr, res)
        else:
            print(Fore.RED + "sorry the tag is invalid\n")

        inp = input(
            Fore.LIGHTCYAN_EX
            + "====> press any key if you want to\
 continue OR press q to quit:"
        )
        if inp == "q":
            break


def print_result(res):
    """printing result"""
    print(res.b.prettify())
    input("press any key to continue")


def clear_screen():
    """clearing the screen"""
    os.system("cls" if os.name == "nt" else "clear -x")
    subprocess.call(["tput", "reset"])


# alternative of switch-case statement
def process_selected_options(selected_opt, res):
    """process the selected option"""
    if selected_opt == "s":
        show_options()
    elif selected_opt == "p":
        print_result(res)
    elif selected_opt == "c":
        clear_screen()
    elif selected_opt == "sw":
        start_web_scrapping(res)


def process_list():
    """getting input for options"""
    show_options()
    inp = input()
    return inp


def process_options(res):
    """process options"""
    ans = input("\npress 'o' to see all options or 'q' to quit: ")
    if ans == "o":
        selected_opt = process_list()
        if selected_opt == "q":
            return selected_opt
        process_selected_options(selected_opt, res)

    elif ans == "q":
        return ans
    else:
        print("\n!!! please enter a valid option !!!")


if __name__ == "__main__":
    res_html = process_url_input()
    soup = BeautifulSoup(res_html, "html.parser")
    QUITTING = False
    while not QUITTING:
        returned_ans = process_options(soup)
        if returned_ans == "q":
            QUITTING = not QUITTING
