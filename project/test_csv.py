import csv
import json
import pandas as pd

buah = [{'nama':'anggur','warna':'hijau, putih, merah dan ungu'},{'nama':'jeruk','warna':'kuning'},{'nama':'manggis','warna':'ungu'}]

data = []

for b in buah:
    nama = b.get('nama')
    warna = b.get('warna')

    data.append(
        dict(nama=nama,warna=warna)
    )

print(data)

# save as csv
keys = data[0].keys()
with open('warna_buah.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)

# save as json
item_data = dict(data=data)
with open('warna_buah.json', 'w') as outfile:
    json.dump(item_data, outfile)

# read json file
f = open('warna_buah.json')
data = json.load(f)

# save as excel xlsx
df = pd.DataFrame.from_dict(buah)
print(df)
df.to_excel('warna_buah.xlsx')


# print(data)
print('Done!')
