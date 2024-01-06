from yaml import safe_load


def load_config(path: str) -> dict:
    with open(path) as f:
        config = safe_load(f)

    return config