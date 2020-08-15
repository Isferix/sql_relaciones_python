'''
SQL Relaciones [Python]
Modulo
---------------------------
Autor: Ishef Glatzel
Version: 1.0

Descripcion:
Modulo SQLite
'''

__author__ = "Ishef Glatzel"
__email__ = "Ishefglatzel@gmail.com"
__version__ = "1.0"


import os
import sqlite3 

class consulta():
    """
    Objeto que provee funciones para ejecutar consultas a una base de datos determinada
    """

    def __init__(self):
        """
        Declara la variable directorio y la variable file\n
        directory: Guardara la ubicacion del path que usan las funciones unique y multiple\n
        file: Guarda el nombre del archivo en el que se trabaja
        """
        self.directory = None
        #La utilidad de File proviene del caso en donde se va a trabajar en un archivo fijo, 
        #podria declararse y luego no habria que especificarlo cada vez que se llame a las funciones de consulta
        self.file = None


    def unique(self, sentence, expresion=None, file='', returns=None, script=False):
        """
        Ejecuta `UNA` Sentencia SQL en el archivo pasado como parametro\n
        @param sentence: `str` Sentecia escrita SQL escrita en texto\n
        @param file: `str` Archivo en el que sera ejecutado la sentencia\n
        @expresion: En caso de necesitar interactuar con la query antes de cerrar la conexion,
        es posible introducir lineas de comando para este fin\n
        POR DEFECTO `@expresion` UTILIZA LA SENTENCIA `eval()` PARA DEFINIR `@returns`, POR LO QUE SE DEBERA INTRODUCIR
        LINEAS SIMPLES COMO POR EJEMPLO: [row for row in query]\n

        @returns: Variable donde se almacenara los datos extras de @expresion, por defecto este valor es None\n

        @script: En caso de necesitar agregarse una gran cantidad de codigo para interactuar con la query puede marcar como True
        esta opcion y en el `@param expresion` pasar un conjunto de lineas mas complejas\n
        AL ACTIVAR ESTA OPCION, `@expresion` EJECUTARA EL TEXTO PASADO COMO SCRIPT CON LA FUNCION `exec()`

        Return: Retorna `None` en caso de no estar definido returns, caso contrario devuelve `@returns`
        """
        
        if self.file is not None:
            file=self.file

        conn = sqlite3.connect('{}\{}'.format(self.directory, file))
        c = conn.cursor()

        #Se guarda los resultados de la query en una variable objeto para su posterior interaccion
        query = c.execute(sentence)
        
        if expresion is not None:
            if script:
                    exec(expresion, globals(), locals())
                                
                    if not returns:
                        returns = None

            else: 
                returns = eval(expresion)
                if len(returns) == 0:
                    returns = None

        conn.commit()
        conn.close()
        return returns


    def multiple(self, sentence, group, expresion=None, file='', script=None, returns=None):
        """
        Ejecuta `VARIAS` Sentencias SQL en el archivo pasado como parametro\n
        @param sentence: `str` Sentecia escrita SQL escrita en texto\n
        @param group: `list` Conjunto de Datos que seran utilizados para ejecutar la sentencia\n
        @param file: `str` Archivo en el que sera ejecutado la sentencia\n
        @expresion: En caso de necesitar interactuar con la query antes de cerrar la conexion,
        es posible introducir lineas de comando para este fin\n
        POR DEFECTO `@expresion` UTILIZA LA SENTENCIA `eval()` PARA DEFINIR `@returns`, POR LO QUE SE DEBERA INTRODUCIR
        LINEAS SIMPLES COMO POR EJEMPLO: [row for row in query]\n

        @returns: Variable donde se almacenara los datos extras de @expresion, por defecto este valor es None\n

        @script: En caso de necesitar agregarse una gran cantidad de codigo para interactuar con la query puede marcar como True
        esta opcion y en el `@param expresion` pasar un conjunto de lineas mas complejas

        Return: Retorna `None` en caso de no estar definido returns, caso contrario devuelve `@returns`
        """

        if self.file is not None:
            file=self.file

        conn = sqlite3.connect('{}\{}'.format(self.directory, file))
        c = conn.cursor()

        #Se guarda los resultados de la query en una variable objeto para su posterior interaccion
        query = c.executemany(sentence, group)

        
        if expresion is not None:
            if script:

                exec(expresion, globals(), locals())
                                
                if not returns:
                    returns = None

            else: 
                returns = eval(expresion)
                if not returns:
                    returns = None

            
        conn.commit()
        conn.close()
        return returns
    

    def script(self, script, file=''):
        """
        Ejecuta un `SCRIPT` de SQL en el archivo pasado como parametro\n
        @param script: `str` Ubicacion del script SQL\n
        @param file: `str` Archivo en el que sera ejecutado la sentencia\n
        """
        if self.file is not None:
            file=self.file

        conn = sqlite3.connect('{}\{}'.format(self.directory, file))
        c = conn.cursor()

        query = c.executescript(open(script, "r").read())

        conn.commit()
        conn.close()



consulta = consulta()


