import csv
import json

list_csv_2 = []
index = ["nombre",
         "tipo",
         "year"
         ]

list_csv_2.append(index)

#En publicaciones json pones el nombre del json de autores:

with open('publicaciones.json', 'r') as file:
    f = json.load(file)

    for i in f:
        nombre = i['title']
        tipo = i['type']
        year  = i['year']

        values_2 = [nombre,
                    tipo,
                    year,
                    ]

        list_csv_2.append(values_2)
        print(values_2)

comprobacion_csv = open('publ' + '.csv', 'w', encoding= 'utf-8')

with comprobacion_csv:
    writer = csv.writer(comprobacion_csv)
    writer.writerows(list_csv_2)

comprobacion_csv.close()