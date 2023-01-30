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


def commented_line(line: str) -> bool:
    trimmed_line = line.strip()
    line = trimmed_line.startswith("//")
    asterix_line = trimmed_line.startswith("/*") and trimmed_line.endswith("*/")
    return line or asterix_line


def start_multi_line_comment(line: str) -> bool:
    return line.strip().startswith("/*")


def ends_multi_line_comment(line: str) -> bool:
    return line.strip().__contains__("*/")
