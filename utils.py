def filter_dict(dict_obj, callback):
    new_dict = dict()
    for (key, value) in dict_obj.items():
        if callback((key, value)):
            new_dict[key] = value
    return new_dict


def get_between(s, first, last) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def stand(s) -> str:
    return str(s).lower().replace('\"', '\'').replace(".", ":")
