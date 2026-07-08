def validate_input(code):

    if code is None:
        return False

    if len(code.strip()) == 0:
        return False

    return True