from dotenv import load_dotenv

def load_config():
    load_dotenv()

def load_universe():
    with open('cryscript/universe.txt', 'r') as fp:
        universe = fp.read().split('\n')
    return universe