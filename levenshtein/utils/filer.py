def normalize_from_file(string):
    """
    If string is a filename, return the content of the file
    """
    try:
        with open(string, 'r') as textfile:
            string = textfile.read()
    except IOError:
        pass

    return string
