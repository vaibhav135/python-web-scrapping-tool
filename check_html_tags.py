def all_html_tags():
    """gets all the html tags from the text file"""
    with open("html_tags_list.txt") as f:
        read_data = f.read()
    return read_data.splitlines(True)
    # print(read_data)


def check_tag(attr):
    """checks the tags and tells if the tags is valid"""
    len_attr = len(attr)
    start_tag = attr.find("<") + attr.find("/") + (attr.find(">") - (len_attr - 1)) + 1
    end_tag = attr.find("<") + (attr.find("/") - 1) + (attr.find(">") - (len_attr - 1))

    if (attr.find("<") + attr.find("/") + attr.find(">")) == -3:
        pass
    else:
        if start_tag == 0:
            attr = attr.strip("<>")
        elif end_tag == 0:
            attr = attr.strip("</>")
        else:
            return False

    gets_tags_list = all_html_tags()
    for value in gets_tags_list:
        value = value.split("\n")[0]
        # print("attr: {}  value: {} length: {}".format(attr, value, len(value)))
        if attr == value:
            return True
    return False


# if __name__ == "__main__":
# check_tag()
