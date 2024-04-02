import json

cenz_worlds = []

path_file_txt = 'cenz_txt.txt'
path_file_json = 'cenz.json'

with open(path_file_txt, encoding='utf-8') as cenzored_txt:

    # Все в одну строку. Слова разъеденены либо пробелом, либо запятой
    for string_words in cenzored_txt:
        cenz_worlds_with_garbage_str = string_words.lower().replace(' ', ',')
        cenz_worlds_with_garbage = cenz_worlds_with_garbage_str.split(',')

    cenz_worlds_set = set(cenz_worlds_with_garbage)
    cenz_worlds = sorted(list(cenz_worlds_set))
    try:
        cenz_worlds.remove('')
    except:
        pass
    print(cenz_worlds)

with open(path_file_json, 'w', encoding='utf-8') as cenzored_json:
    json.dump(cenz_worlds, cenzored_json, indent=2)


    # Каждое слово на новой строке
    # for string_word in cenzored_txt:
        # word = string_word.lower().split('\n')[0]
        # if word not in ['', ' ']:
        #     cenz_worlds.append(word)