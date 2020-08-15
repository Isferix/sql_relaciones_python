'''
SQL Relaciones [Python]
Ejemplos de clase
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Resolucion del ejercicio planteado en el archivo ejercicio_practica.md
'''

__author__ = "Ishef Glatzel"
__email__ = "Ishefglatzel@gmail.com"
__version__ = "1.0"

import os
import csv

from config import config
from mySqlModule import consulta

#Declaraciones de Path
script_path = os.path.dirname(os.path.realpath(__file__))

config_path_name = os.path.join(script_path, 'config.ini')
db = config('db', config_path_name)
dataset = config('dataset', config_path_name)
schema_path_name = os.path.join(script_path, db['schema3'])

#Declaracion del directorio y archivo de trabajo
consulta.directory = script_path = os.path.dirname(os.path.realpath(__file__))
consulta.file = db['database_ejercicio']

#Declaracion de PRAGMAS
consulta.unique("""PRAGMA foreign_keys = 1""")


def create_schema():
    consulta.script(schema_path_name)


def fill():
    """
    Rellena el archivo `libreria.db` con los datos de los
    archivos `libreria_autor.csv` y `libreria_libro.csv`
    """
    def fetch_data(file, format):
        """
        Recorre un archivo csv y recolecta datos\n
        Return: Devuelve una lista con tuplas
        """
        with open(file) as csvfile:
            data = list(csv.DictReader(csvfile))
            return [tuple([e[i] for i in format]) for e in data]
            

    def insert_autor(data):
        """
        Inserta un conjunto de autores en la tabla autor
        """
        consulta.multiple("""
        INSERT INTO autor(author)
        VALUES(?);""", data)


    def insert_group(group):
        """
        Inserta un libro en la tabla libro
        """
        consulta.multiple("""
        INSERT INTO libro (title, pags, fk_author_id)
        SELECT ?,?, a.id
        FROM autor as a
        WHERE a.author = ?""", group)
        
    
    data_1 = dataset['libreria_autor']
    data_2 = dataset['libreria_libro']

    dataset_1 = fetch_data(data_1, ('autor',))
    dataset_2 = fetch_data(data_2, ('titulo', 'cantidad_paginas', 'autor'))
    
    insert_autor(dataset_1)
    insert_group(dataset_2)


def fetch(id=0):
    if id == 0:
        fetch = consulta.unique("""
        SELECT l.id, l.title, l.pags, a.author
        FROM libro AS l
        INNER JOIN autor AS a ON l.fk_author_id = a.id;""", '[row for row in query]')
        for datos in fetch:
            print('ID: {row[0]} | TITULO: {row[1]} | PAGS: {row[2]} | AUTOR: {row[3]}\n'.format(row=datos))
    elif id > 0:
        fetch = consulta.unique("""
        SELECT l.title, l.pags, a.author
        FROM libro AS l
        INNER JOIN autor AS a ON l.fk_author_id = a.id
        WHERE l.id = '{}';""".format(id), '[row for row in query]')
        if fetch == None:
            print('La ID buscada no existe\n')
        elif fetch:
            for datos in fetch:
                print('TITULO: {row[0]} | PAGS: {row[1]} | AUTOR: {row[2]}\n'.format(row=datos))
    
    elif id < 0 or type(id) !=int:
        return None


def search_author(book_title):
    """
    Retorna en pantalla el autor de hacer una query a la tabla `libro` del archivo `libreria.db`\n
    @param book_title: `str` nombre del libro del que sera buscado su autor:\n
    """
    autor = consulta.unique("""
    SELECT a.author
    FROM libro AS l
    INNER JOIN autor AS a ON l.fk_author_id = a.id
    WHERE l.title = '{}'""".format(book_title), '[row[0] for row in query]')
    print('LIBRO: {} | AUTOR: {}'.format(book_title, autor[0]))


if __name__ == "__main__":
    # Crear DB
    create_schema()

    # Completar la DB con el CSV
    fill()

    # Leer filas
    fetch()  # Ver todo el contenido de la DB
    fetch(3)  # Ver la fila 3
    fetch(20)  # Ver la fila 20

    # Buscar autor
    search_author('Relato de un naufrago')