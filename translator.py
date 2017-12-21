import json
from collections import OrderedDict
from translation import baidu, google, youdao, iciba, bing, set_default_translation, set_default_language, get
import copy

set_default_translation('bing')
set_default_language('de', 'en')

courses = json.load(open('output/output-bern.json'))
courses_translated = copy.deepcopy(courses)
# fields_to_translate = ['times', 'date', 'description', 'material'] #Neuch
# fields_to_translate = ['notes', 'information', 'material', 'language'] #Fribourg
fields_to_translate = ['description', 'requirements', 'registration', 'material'] #Bern

for x in range(0, len(courses)):
    print('translating ...')
    for field in fields_to_translate:
        try:
            courses_translated[x][field] = get(courses[x][field])
        except Exception as e:
            print(e)
    #print (json.dumps(courses_translated[x]))

#courses_beautiful = json.dumps(OrderedDict(courses_translated), sort_keys=False, indent=4)

# not very performant yet
with open('output/translated/output-bern-translated.json', 'w') as file:
    print('writing file ...')
    file.write(json.dumps(courses_translated))
    print('done')