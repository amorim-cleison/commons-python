def remove_special_chars(text):
    """
    Remove the special characters in the `text`.
    """
    return replace_special_chars(text, '')


def replace_special_chars(text, char='_'):
    """
    Replace the special characters in the `text` by the informed `char`.
    """
    import string
    import re
    special_chars = re.escape(string.punctuation + string.whitespace)
    return re.sub(r'[' + special_chars + ']', char, text)


def is_empty(text):
    """
    Validate if the `text` is empty, whitespace or `None`.
    """
    return (not text) or text.isspace()
