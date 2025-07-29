import json
import os


def load_test_data(filename):
    path = os.path.join("testdata", filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)