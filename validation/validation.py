import re


def validate_string(data, min_):
    if len(data) < min_:
        return False

    return True


def validate_student_id(data, min_):
    if not str.isdecimal(data):
        return False

    if len(data) < min_:
        return False

    return True


def compare_passwords(p1, p2):
    if p1 == p2:
        return True
    else:
        return False


def strip_tags(data):
    strip = re.compile('<.*?>')
    return re.sub(strip, "", data)
