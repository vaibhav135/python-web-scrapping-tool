def all_html_tags():
    """gets all the html tags from the text file"""
    with open("html_tags_list.txt") as f:
        read_data = f.read()
    return read_data.splitlines(True)


def default_tag_conversion(attr):
    """this removes the angled bracets and slash"""
    """<hr> => hr || </hr> => hr"""
    len_attr = len(attr)
    start_tag = attr.find("<") + attr.find("/") + (attr.find(">") - (len_attr - 1)) + 1
    end_tag = attr.find("<") + (attr.find("/") - 1) + (attr.find(">") - (len_attr - 1))
    return (start_tag, end_tag)


def check_tag(attr):
    """checks the tags and tells if the tags is valid"""
    start_tag, end_tag = default_tag_conversion(attr)
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
        if attr == value:
            return True
    return False


