import tkinter as tk
import webbrowser
from tkinter import Button, Grid, Scrollbar, filedialog, ttk
from tkinter.messagebox import showerror, showinfo, showwarning

from bs4 import BeautifulSoup

import check_html_tags
import process_url


def clear_text_screen():
    textBox["state"] = "normal"
    textBox.delete(1.0, tk.END)
    textBox["state"] = "disabled"


def change_textBox_content(result):
    # print(result)
    textBox["state"] = "normal"
    textBox.insert("1.0", result)
    textBox["state"] = "disabled"


# test url = "https://github.com/about"
def set_process_url_input(url):
    global result, soup
    html_res = process_url.process_url_input(url)

    # ignore: the error below on html_res
    soup = BeautifulSoup(html_res, "html.parser")
    result = soup
    change_textBox_content(result)


def formatted_tags(tags):
    """Removes the extra space from tags ex: [" head", " h1 "] => ["head", "h1"]"""
    tags = tags.strip()
    return tags


def process_tag(tag):
    # tag_res : if the tag is valid or not result in boolean
    tag_list = tag.split(",")
    formatted_tag_list = [formatted_tags(m_tags) for m_tags in tag_list]
    for s_tag in formatted_tag_list:
        tag_res = check_html_tags.check_tag(s_tag)
        if not tag_res:
            showwarning(
                title="invalid tag {}".format(s_tag), message="please enter a valid tag"
            )
            return

    result = soup.find_all(formatted_tag_list)
    # print(type(result))
    clear_text_screen()
    change_textBox_content(result)


def OpenUrl(help_url):
    """This will open the help url in the web browser"""
    webbrowser.open_new(help_url)


def change_text_wrap_type(wrap_type):
    """This will change the wrap type i.e., char, word, none"""
    textBox.configure(wrap=wrap_type)


def create_input_frame(container):
    s = ttk.Style()
    s.configure("Danger.TFrame", borderwidth=2, relief="sunken")
    frame = ttk.Frame(container, style="Danger.TFrame")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    # frame.grid_columnconfigure(2, weight=1)

    # grid row configuration
    frame.grid_rowconfigure(0, weight=2)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_rowconfigure(3, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_rowconfigure(5, weight=1)
    frame.grid_rowconfigure(6, weight=8)

    # for getting the info about the width of the column

    # ttk.Separator(frame, orient="vertical").grid(
    # column=0, row=0, rowspan=17, sticky="nse"
    # )
    # ttk.Separator(frame, orient="vertical").grid(
    # column=1, row=0, rowspan=17, sticky="nse"
    # )
    # ttk.Separator(frame, orient="vertical").grid(
    # column=2, row=0, rowspan=17, sticky="nse"
    # )

    # label instructing to enter input
    ttk.Label(frame, text="Enter input's here", font=("sans", 14)).grid(
        column=1, row=0, sticky="w"
    )

    # label and entry for url
    url_label = ttk.Label(frame, text="url")
    url_label.grid(column=1, row=1, sticky="w")

    # get url input
    url = tk.StringVar()
    url_entry = ttk.Entry(frame, textvariable=url, width=30)
    url_entry.focus()
    url_entry.grid(column=1, row=1)

    # Submit button to fetch the url result
    global submit_button
    submit_button = Button(
        frame,
        width=15,
        text="fetch data",
        command=lambda: set_process_url_input(url=url_entry.get()),
    )
    submit_button.grid(column=1, row=2)

    # label for instructing multiple inputs
    multiple_tags_label = ttk.Label(
        frame,
        text="you can also use multiple tags separated by comma",
        font=("sans", 14),
    )
    multiple_tags_label.grid(column=1, row=3, columnspan=2, sticky="w")

    # label and entry for tag
    tags_label = ttk.Label(
        frame,
        text="tag",
    )
    tags_label.grid(column=1, row=4, sticky="w")

    # entry for tags
    tags = tk.StringVar()
    tags_entry = ttk.Entry(frame, textvariable=tags, width=30)
    tags_entry.grid(column=1, row=4)

    # Submit button to get the tag result from the html output
    global tag_submit_button
    tag_submit_button = Button(
        frame,
        width=15,
        text="get tag result",
        command=lambda: process_tag(tags_entry.get()),
    )
    tag_submit_button.grid(column=1, row=5)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=20)

    # create a menubar
    menubar = tk.Menu(container)
    container.config(menu=menubar)

    # create a option menu
    option_menu = tk.Menu(container, tearoff=False)

    # create help menu
    help_menu = tk.Menu(container, tearoff=False)
    help_url = "https://github.com/vaibhav135/python-web-scrapping-tool"
    help_menu.add_command(label="help", command=lambda: OpenUrl(help_url))
    help_menu.add_command(label="quit", command=container.destroy)

    # add wrap submenu like wrap = "char"|"word"|"none"
    wrap_sub_menu = tk.Menu(option_menu, tearoff=False)
    wrap_sub_menu.add_command(
        label="char", command=lambda: change_text_wrap_type("char")
    )
    wrap_sub_menu.add_command(
        label="word", command=lambda: change_text_wrap_type("word")
    )
    wrap_sub_menu.add_command(
        label="none", command=lambda: change_text_wrap_type("none")
    )

    # add a menu item to the menu
    option_menu.add_cascade(label="wrap", menu=wrap_sub_menu)

    # add the File menu to the menubar
    menubar.add_cascade(label="options", menu=option_menu)
    menubar.add_cascade(label="help", menu=help_menu)

    return frame


def file_save():
    f = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
    # asksaveasfile return `None` if dialog closed with "cancel".
    if f is None:
        return
    # starts from `1.0`, not `0.0`
    text2save = str(result)
    f.write(text2save)
    # `()` was missing.
    f.close()


def remove_empty_lines():
    """remove the extra empty line from the text extracted from the html"""
    if raw_text == "":
        showwarning(title="no text found", message="please fetch the text first")
        return

    formatted_lines = raw_text.split("\n")
    count = 0
    for index, line in enumerate(formatted_lines):
        if line == " " or line == "":
            count += 1
            # print("add: ", index, "count: ", count, "line: ", line)
            if count > 2:
                formatted_lines[index] = "-"
        else:
            count = 0
            # print("zero: ", index)

    final_line = [line for line in formatted_lines if line != "-"]
    new_result = ""
    for fl in final_line:
        new_result += "  " + fl.strip() + "\n"
    # print(new_result)
    clear_text_screen()
    change_textBox_content(new_result)


# extracting text from the html result
def get_text():
    global raw_text
    raw_text = soup.get_text()
    result = raw_text
    # print(type(result))
    clear_text_screen()
    change_textBox_content(result)


# reverting the text back to code
def get_code():
    result = soup
    clear_text_screen()
    change_textBox_content(result)


def create_output_frame(container):
    s = ttk.Style()
    s.configure("Danger.TFrame", borderwidth=2, relief="sunken")
    frame = ttk.Frame(container, style="Danger.TFrame")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=1)
    frame.grid_columnconfigure(4, weight=1)
    frame.grid_columnconfigure(5, weight=1)

    frame.grid_rowconfigure(0, weight=18)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=2)

    # making the text global so that when the button is\
    # pressed it changes the contents inside of the text widget
    global textBox
    textBox = tk.Text(frame)
    textBox.grid(column=1, row=0, sticky="nsew", columnspan=5)
    yscrollbar = Scrollbar(frame, orient="vertical", command=textBox.yview)
    xscrollbar = Scrollbar(frame, orient="horizontal", command=textBox.xview)
    yscrollbar.grid(column=6, row=0, sticky="ns")
    xscrollbar.grid(column=1, row=0, columnspan=6, sticky="sew")
    textBox["yscrollcommand"] = yscrollbar.set
    textBox["xscrollcommand"] = xscrollbar.set

    # do something here
    ttk.Separator(frame, orient="horizontal").grid(
        column=1, row=1, sticky="ew", columnspan=6
    )
    # ttk.Label(frame, text="options here soon...").grid(column=1, row=2)
    save_button = Button(frame, text="save as", command=lambda: file_save())
    save_button.grid(column=1, row=2)

    # getting the text from the code
    get_text_button = Button(frame, text="get text", command=get_text)
    get_text_button.grid(column=2, row=2)

    # format the text
    format_text = Button(frame, text="format text", command=remove_empty_lines)
    format_text.grid(column=3, row=2)

    # revert the text state back to code
    get_code_button = Button(frame, text="revert back", command=get_code)
    get_code_button.grid(column=4, row=2)

    # ttk.Label(frame, text="options here soon...").grid(column=1, row=2)
    save_button = Button(frame, text="clear textbox", command=clear_text_screen)
    save_button.grid(column=5, row=2)

    return frame


def create_main_window():
    root = tk.Tk()
    root.title("Web-Scrapper GUI")
    root.geometry("1366x1080+50+50")

    # # create a menubar
    # menubar = tk.Menu(root)
    # root.config(menu=menubar)
    # # create a file menu
    # option_menu = tk.Menu(root, tearoff=False)
    # # add a menu item to the menu
    # option_menu.add_command(label="Exit", command=root.destroy)
    # # add the File menu to the menubar
    # menubar.add_cascade(label="options", menu=option_menu)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    input_frame = create_input_frame(root)
    input_frame.grid(column=0, row=0, sticky="nsew", padx=2, pady=2)

    # separator.pack(fill="x")

    output_frame = create_output_frame(root)
    output_frame.grid(column=1, row=0, columnspan=2, sticky="nsew", pady=2, padx=2)

    root.mainloop()


result = ""
soup = ""
raw_text = ""

if __name__ == "__main__":
    create_main_window()
