
# This script was proudly coded by wxrayut (https://github.com/wxrayut).

def replace_slash(path):
    return path.replace('\\', '/')

def dump(filepath, encoding: str = 'utf-8', *, __size: int = None, mode: int = None, read_modes = ['read', 'readlines']):
    with open(filepath, 'r', -1, encoding) as f:
        if __size:
            data = f.read(__size)
        else:
            if read_modes[mode] == 'read':
                data = f.read()
            elif read_modes[mode] == 'readlines':
                data = f.readlines()
    return data
