import json
from collections import OrderedDict
from translation import baidu, google, youdao, iciba, bing, set_default_translation, set_default_language, get
import copy

keys = set()

files = []
files.append('output/output-bern.json')
files.append('output/output-neuch.json')
files.append('output/output-fribourg.json')

for file in files:
    courses = json.load(open(file))
    for course in courses:
        for key in course:
            keys.add(key) #attributeset.add(key)

table = [[key, "TRANSLATION"] for key in keys]
all_keys = json.dumps(OrderedDict(table), sort_keys=True, indent=4)
attr_file = open('mapping_keys_fresh.json', 'w')
attr_file.write(all_keys)
attr_file.close()
print (table)




# not very performant yet
#with open('output-bern-translated.json', 'w') as file:
#    print('writing file ...')
#    file.write(json.dumps(courses_translated))
