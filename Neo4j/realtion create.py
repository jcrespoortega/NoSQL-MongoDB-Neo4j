import csv
import json

list_csv_2 = []
index = ["nombre",
         "autor"
         ]

list_csv_2.append(index)

with open('publicaciones.json', 'r') as file:
    f = json.load(file)
    for i in f:

        nombre = i['title']
        autor = i['author']

        if type(autor) != list:
            values_2 = [nombre,
                        autor
                        ]

            list_csv_2.append(values_2)
            print(values_2)

        else:

            for j in autor:

                values_2 = [nombre,
                            j
                            ]

                list_csv_2.append(values_2)
                print(values_2)


comprobacion_csv = open('publicaciones2' + '.csv', 'w', encoding= 'utf-8')

with comprobacion_csv:
    writer = csv.writer(comprobacion_csv)
    writer.writerows(list_csv_2)

comprobacion_csv.close()

