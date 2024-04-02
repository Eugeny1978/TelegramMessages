import json
#
# data = '3456.dd'
#
# num = data.split('.')[0]
# print(num.isnumeric())
# print(num.isdigit())
# print(num.isdecimal())
# print(float(data).isdecimal())

path_file_cenz = r'common/cenz.json'
# cenzored_words = set(json.load(open(path_file_cenz)))
cenzored_words = set(json.load(open(path_file_cenz))).intersection()
print(cenzored_words)



