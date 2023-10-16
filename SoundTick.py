
# This script was proudly coded by wxrayut (https://github.com/wxrayut).

import os
from module import replace_slash, dump

def get_sound_tick_id(skinid: int):
    return str(int(str(skinid), base=10) % 100)

def playherosoundtick(line: str, start: str, end: str, empty: str, sound_tick_id: str):
    line = line.replace(start, empty)
    line = line.replace(end, empty)
    line = line.strip()
    return line + '_Skin' + sound_tick_id

# set configs
current_directory = 'Skill/INP'
output_directory = 'Skill/OUT'

encoding = 'ISO-8859-1'
start = '<String name="eventName" value="'
end = '" refParamName="" useRefParam="false" />'
empty = ''

#   +-------- test with --------+
# +--------------------------------+
# |                                |
# |     Airi Dimension Breaker     |
# |                                |
# |     heroid = 13000             |
# |     skinid = 13015             |
# |     skinpos = 13016 (model id) |
# |     soundick id = 15           |
# |                                |
# +--------------------------------+

skinid = 13015
sound_tick_id = get_sound_tick_id(skinid)

for file in os.listdir(current_directory):
    filepath = replace_slash(os.path.join(current_directory, file))
    header = dump(filepath, encoding, __size=4)
    if header == '\x22\x4A\x00\xEF':
        continue
    else:
        newlists = []
        lines = dump(filepath, encoding, mode=1)
        for i, line in enumerate(lines):
            if start in line:
                modified_content = playherosoundtick(line, start, end, empty, sound_tick_id)
                newlists.append((i, modified_content))
        if newlists:
            content = dump(filepath, encoding, mode=1)
            for i in range(len(newlists)):
                content_index, modified_content = newlists[i]
                print('pos -> {}, value -> {}'.format(content_index, modified_content))
                indent = content[content_index].find(start)
                content[content_index] = (' ' * indent) + start + modified_content + end + '\n'
            output_path = os.path.join(output_directory, file)
            with open(output_path, 'w', -1, encoding) as w:
                for line in content:
                    w.write(line)