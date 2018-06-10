import csv
import json

list_csv_2 = []
index = ["nombre",
         "numero_publicaciones",
         "edad"
         ]

list_csv_2.append(index)

#autores introducces tu nombre de archivo.

with open('autores.json', 'r') as file:
    f = json.load(file)
    for i in f:

        nombre = i['nombre']
        num = i['num_publicaciones']
        antiguedad = i['edad']

        values_2 = [nombre,
                    num,
                    antiguedad,
                    ]

        list_csv_2.append(values_2)
        print(values_2)

comprobacion_csv = open('autores' + '.csv', 'w')

with comprobacion_csv:
    writer = csv.writer(comprobacion_csv)
    writer.writerows(list_csv_2)

comprobacion_csv.close()
