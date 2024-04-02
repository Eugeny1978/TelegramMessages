
data = '3456.dd'

num = data.split('.')[0]
print(num.isnumeric())
print(num.isdigit())
print(num.isdecimal())
print(float(data).isdecimal())



