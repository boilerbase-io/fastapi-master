import json


def read_json_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as err:
        print(str(err))
        return False
    return data


def write_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as err:
        print(str(err))
        return False
    return data
