import xmltodict, json
from time import time
from datetime import datetime
import fileinput

class Utils():

    def __init__(self):
        #Variable para almacenar los datos de los autores
        self.autores = {}
        #Variable para almacenar el número de elementos de cada tipo de publicacion
        self.num_elements = {}
        #Variable para cargar los elementos del dblp que queremos procesar
        self.elements_to_proccess = ['article', 'inproceedings', 'incollection', 'phdthesis', 'mastersthesis', 'www']
        #Variable con los campos que podemos prescindir de cada tipo de publicacion
        self.fields_to_delete = {"article":['ee', 'journal', 'number', 'pages', 'url', 'volume'],
            "inproceedings": ['pages', 'url', 'year', 'booktitle', 'ee'],
            "incollection": ['pages', 'url', 'year', 'booktitle', 'ee'],
            "phdthesis": ['school', 'year', 'pages'],
            "mastersthesis": ['school', 'year', 'pages', 'ee', 'url'],
            "www": ['year', 'pages', 'url']}

    #Vamos guardando o actualizando los datos de los autores
    def carga_autores (self, element, nombre_autor, tipo):
        #Si el autor ya estaba en el diccionario, cogemos sus datos y los actualizamos
        if nombre_autor in self.autores:
            data = self.autores[nombre_autor]
            #Le asignamos una nueva publicacion
            publicacion = {}
            publicacion['pub_id'] = element['@key']
            publicacion['fecha_pub'] = element['@mdate']
            publicacion['tipo'] = tipo
            data['publicaciones'].append(publicacion)
            #aumentamos el numero de publicaciones que tiene
            data['num_publicaciones'] += 1
            data['edad'] = self.calcula_edad_autor(data['publicaciones'])
        #Si no existe se crea con su nombre como clave y sus datos recogidos del xml
        else:
            # Voy guardando los datos del autor
            author_data = {}
            author_data['nombre'] = nombre_autor
            publicacion = {}
            publicacion['pub_id'] = element['@key']
            publicacion['fecha_pub'] = element['@mdate']
            publicacion['tipo']= tipo
            author_data['publicaciones'] = []
            author_data['publicaciones'].append(publicacion)
            author_data['num_publicaciones'] = 1
            self.autores[nombre_autor] = author_data

    #Método para calcular la edad del autor
    #Se considera la Edad de un autor al número de años transcurridos desde la fecha de su primera publicación
    # hasta la última registrada
    def calcula_edad_autor (self, publicaciones):
        min_date = datetime.strptime(publicaciones[0]['fecha_pub'], '%Y-%m-%d')
        max_date = min_date
        for publicacion in publicaciones:
            str_fecha_pub = publicacion['fecha_pub']
            #COnvertimos el string a objeto Date
            datetime_object = datetime.strptime(str_fecha_pub, '%Y-%m-%d')
            if (datetime_object>max_date):
                max_date = datetime_object
            elif(datetime_object<min_date):
                min_date = datetime_object

        diferencia = max_date-min_date
        edad = str(diferencia)

        #Diferencia: 0:00:00 cuando el valor es identico
        #Diferencia: 2557 days, 0: 00:00 cuando hay días de diferencia
        if (edad== '0:00:00'):
            edad = 0
        else:
            dias = edad[:edad.find(' ')]
            edad = int(dias)/365

        return int(edad)

    #El nombre del autor puede llegar como dict en vez de como str
    # en ese caso nos quedamos con el texto
    def get_nombre_autor (self, autor):
        if isinstance(autor, dict):
           return autor["#text"]
        else:
           return autor

    #Metodo para borrar los campos no necesarios de las publicaciones
    def delete_fields (self, element, fields):
        for field in fields:
            if field in element:
                del element[field]

    #Método que lee el xml original y por cada tipo para generar los ficheros json resultantes
    def genera_ficheros_json (self, fichero_xml):
        # Creamos colección donde la clave es el nombre del autor y su valor los datos para buscarlo rápido por el id
        print("Procesando fichero: "+ fichero_xml.name)
        start_time = time()
        doc = xmltodict.parse(fichero_xml.read())
        elapsed_time = time() - start_time
        print("Procesado. Elapsed time: %0.10f seconds." % elapsed_time)

        dblp = doc['dblp']

        #Recorro los distintos tipos
        for tipo in self.elements_to_proccess:
            start_time = time()
            #Obtengo la información que me interesa de cada tipo
            publicaciones = self.procesa_publicacion(dblp,tipo)
            # self.num_elements[tipo] = len(publicaciones)

            # Con el resultado obtenido lo pasamos a fichero
            self.escribe_ficheros(publicaciones)
            publicaciones.clear()

            elapsed_time = time() - start_time
            print("Tiempo total procesando publicaciones de tipo " + tipo + ": %0.10f minutes." % (elapsed_time / 60))
            publicaciones = None

        print("Escribiendo datos en fichero de autores")
        with open('autores.json', 'a') as authors_file:
            json.dump(list(self.autores.values()), authors_file, sort_keys=True, indent=4, separators=(',', ': '))

        # Vaciamos colección para liberar memoria
        self.autores.clear()

        # Escribe datos de num de publicaciones en fichero
        # print("Escribiendo numero de elementos en fichero num_pubs")
        # with open('num_pubs.json', 'w') as data_file:
        #     json.dump(self.num_elements, data_file, sort_keys=True, indent=4, separators=(',', ': '))


        print("Finalizado genera_ficheros_json")

    def escribe_ficheros (self, publicaciones):
        start_time = time()
        print("Escribiendo datos en fichero de publicaciones")
        with open("publicaciones.json", 'a') as fp:
            json.dump(publicaciones, fp, sort_keys=True, indent=4, )


        # # Escribe datos de num de publicaciones en fichero
        # with open('num_pubs.json', 'w') as data_file:
        #     json.dump(self.num_elements, data_file, sort_keys=True, indent=4, separators=(',', ': '))

        elapsed_time = time() - start_time
        print("Elapsed time writing files: %0.10f seconds." % elapsed_time)



    def procesa_publicacion (self, dblp, tipo):
        print("Procesando " + tipo + " de dblp")
        start_time = time()
        r = json.dumps(dblp[tipo])
        elements = json.loads(r)
        for element in elements:
            # Agregamos el tipo para poder filtrar por el tipo de publicacion
            element['type'] = tipo

            #obtenemos los campos que no queremos de cada tipo de publicacion
            article_fields_to_delete = self.fields_to_delete.get(tipo)
            # Elimimamos los campos no necesarios de la publicacion
            self.delete_fields(element, article_fields_to_delete)

            # recogemos el nomre del autor, en principio todos los campos que recogemos tienen author
            if 'author' in element:
                nombre_autor = element['author']
                # Puede venir un nombre solo o un listado de nombres
                if isinstance(nombre_autor, str):
                    self.carga_autores(element, self.get_nombre_autor(nombre_autor),tipo)
                elif isinstance(nombre_autor, list):
                    for autor in nombre_autor:
                        self.carga_autores(element, self.get_nombre_autor(autor),tipo)

        elapsed_time = time() - start_time
        print("Tiempo total procesando publicación de tipo " + tipo + ": %0.10f minutes." % (elapsed_time / 60))

        return elements


    def reemplaza_caracteres (self, file_name, old_text, new_text):
        with fileinput.FileInput(file_name, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(old_text, new_text), end='')
                # print(line.replace('][', ','), end='')
