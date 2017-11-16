import json
from collections import OrderedDict
from translation import baidu, google, youdao, iciba, bing, set_default_translation, set_default_language, get
import copy

set_default_translation('bing')
set_default_language('auto', 'en')

courses = json.load(open('output-bern.json'))
courses_translated = copy.deepcopy(courses)
fields_to_translate = ['Titel', 'Ort', 'Tag']

for x in range(0, len(courses)):
    print('translating ...')
    for field in fields_to_translate:
        try:
            courses_translated[x][field] = get(courses[x][field])
        except Exception as e:
            print(e)

# not very performant yet
with open('output-bern-translated.json', 'w') as file:
    print('writing file ...')
    file.write(json.dumps(courses_translated))
