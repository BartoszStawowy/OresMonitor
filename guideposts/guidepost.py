from os.path import realpath, join, dirname, abspath
from json import load

WD = dirname(__file__)

def json_package_path(package_name):
    return join(abspath(realpath(join(WD, f'../json_data/{package_name}.json'))))

def result_path():
    return join(abspath(realpath(join(WD, f'../results.txt'))))

def load_json_package(package_name):
        td = json_package_path(package_name)
        with open(td) as f:
            data = load(f)
        return data