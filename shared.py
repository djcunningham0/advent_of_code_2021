def read_text_file(path: str, dtype: type) -> list:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return [dtype(x) for x in data]
