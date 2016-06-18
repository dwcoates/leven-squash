def normalize_from_file(string):
    """
    If string is a filename, return the content of the file
    """
    with open(string, 'r') as textfile:
        try:
            string = textfile.read()
        except IOError:
            pass

    return string
