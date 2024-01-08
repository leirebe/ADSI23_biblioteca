import json

f = open('temas.json')

data = json.load(f)

for i in data['temas']:
    print(i)
    
f.close()