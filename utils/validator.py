MAX_INPUT_LENGTH = 12000  # keep in sync with explanation_service.MAX_CODE_LENGTH


def validate_input(code):

    if code is None:
        return False

    if not isinstance(code, str):
        return False

    if len(code.strip()) == 0:
        return False

    if len(code) > MAX_INPUT_LENGTH:
        return False

    return True