
# This script was proudly coded by wxrayut (https://github.com/wxrayut).

import os
import re
from module import replace_slash, dump

def modifyline(line, start, end, empty):
    line = line.replace(start, empty)
    line = line.replace(end, empty)
    linelist = line.strip()
    return linelist.split('/')

def skilleffect(line, start, end, empty, heroid, skinid, resourceName = ['hero_skill_effects', 'Hero_Skill_Effects']):
    linelist1 = modifyline(line, start, end, empty)
    linelist2 = []
    con = ''
    isindex = 0
    for i, tmp in enumerate(linelist1):
        if tmp in resourceName:
            tmpidx = i + 1
            if linelist1[tmpidx][0:3] == str(heroid)[0:3]:
                con += linelist1[tmpidx] + '/' + str(skinid)
                isindex += tmpidx
            elif len(linelist1) == 3 and linelist1[1] in resourceName:
                con += linelist1[i] + '/' + str(skinid)
                isindex += i
            else:
                con += linelist1[0]
    for i, tmp in enumerate(linelist1):
        if i == isindex:
            linelist2.append(con)
        else:
            linelist2.append(tmp)
    return '/'.join(linelist2)

# set configs
current_directory = 'Skill/INP'
output_directory = 'Skill/OUT'

encoding = 'ISO-8859-1'
starts = ['<String name="resourceName" value="', '<String name="resourceName2" value="', '<String name="resourceName3" value="', '<String name="prefab" value="']
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

heroid = 13000
skinid = 13015

for file in os.listdir(current_directory):
    filepath = replace_slash(os.path.join(current_directory, file))
    header = dump(filepath, encoding, __size=4)
    if header == '\x22\x4A\x00\xEF':
        continue
    else:
        newlists = []
        lines = dump(filepath, encoding, mode=1)
        for i, line in enumerate(lines):
            for start in starts:
                if re.search(start, line) and str(heroid)[0:3] in line:
                    modified_content = skilleffect(line, start, end, empty, heroid, skinid)
                    newlists.append((i, modified_content))
        if newlists:
            content = dump(filepath, encoding, mode=1)
            for i in range(len(newlists)):
                content_index, modified_content = newlists[i]
                for start in starts:
                    try:
                        if re.search(start, content[content_index]):
                            indent = content[content_index].find(start)
                            content[content_index] = (' ' * indent) + start + modified_content + end + '\n'
                    except IndexError:
                        continue
            output_path = os.path.join(output_directory, file)
            with open(output_path, 'w', -1, encoding) as w:
                for line in content:
                    w.write(line)

