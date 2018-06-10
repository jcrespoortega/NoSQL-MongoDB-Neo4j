from Utils import Utils
from MongoUtils import MongoUtils
from time import time


file_name= 'dblp'
extension = '.xml'
final_extension ='.json'


if __name__ == "__main__":

    start_time = time()
    #Generamos los ficheros json a partir del xml
    print("Generando ficheros json")
    with open(file_name + extension) as fd:
        Utils().genera_ficheros_json(fd)

    elapsed_time = time() - start_time
    print("Tiempo total en leer xml y generar jsons: %0.10f minutes." % (elapsed_time / 60))

    #Como se genera el fichero de publicaciones por partes para ahorrar memoria después tenemos que eliminar los arrays
    start_time = time()
    Utils().reemplaza_caracteres('publicaciones.json', '][', ',')
    elapsed_time = time() - start_time
    print("Tiempo total regenerando ficheros %0.10f minutes." % (elapsed_time / 60))

    #A partir de los json generados cargamos las colecciones en mongo
    print("Almacenando datos en MongoDB")
    start_time = time()
    MongoUtils().importa_ficheros()
    elapsed_time = time() - start_time
    print("Tiempo total cargar la bbdd: %0.10f minutes." % (elapsed_time / 60))


