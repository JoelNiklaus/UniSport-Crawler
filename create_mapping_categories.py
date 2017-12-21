import json
from collections import OrderedDict
from translation import baidu, google, youdao, iciba, bing, set_default_translation, set_default_language, get
import copy

sports = set()

files = []
files.append('output/output-bern.json')
files.append('output/output-neuch.json')
files.append('output/output-fribourg.json')

for file in files:
    courses = json.load(open(file))
    for course in courses:
        sports.add(course['sport']) #attributeset.add(key)

table = [[sport, "TRANSLATION"] for sport in sports]
all_sports = json.dumps(OrderedDict(table), sort_keys=True, indent=4)
attr_file = open('mapping_sports.json', 'w')
attr_file.write(all_sports)
attr_file.close()
print (table)
