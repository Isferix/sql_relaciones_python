#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de clase
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import os
import csv

from config import config
from mySqlModule import consulta

# https://extendsclass.com/sqlite-browser.html

#Declaraciones de Path
script_path = os.path.dirname(os.path.realpath(__file__))

config_path_name = os.path.join(script_path, 'config.ini')
db = config('db', config_path_name)
dataset = config('dataset', config_path_name)
schema_path_name = os.path.join(script_path, db['schema2'])

#Declaracion del directorio y archivo de trabajo
consulta.directory = script_path = os.path.dirname(os.path.realpath(__file__))
consulta.file = db['database_secundaria']

#Declaracion de PRAGMAS
consulta.unique("""PRAGMA foreign_keys = 1""")



def create_schema():
    consulta.script(schema_path_name)

    
def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # fk_tutor_id --> id de su tutor

    # Se debe utilizar la sentencia INSERT.
    # Observar que todos los campos son obligatorios
    # Cuando se insert los los estudiantes sería recomendable
    # que utilice el INSERT + SELECT para que sea más legible
    # el INSERT del estudiante con el nombre del tutor

    # No olvidarse que antes de poder insertar un estudiante debe haberse
    # primero insertado el tutor.
    # No olvidar activar las foreign_keys!

    # columnas que deben aparecer en el print:
    # id / name / age / grade / tutor_nombre

    tutores = [('Celeste',),
            ('Federico',)]

    consulta.multiple("""
    INSERT INTO tutor(name)
    VALUES(?);""", tutores)


    estudiantes = [('Franco', '15', '4', 'Celeste'),
                ('Damian', '16', '5', 'Federico'),
                ('Cecilia', '15', '5', 'Federico'),
                ('Fatima', '14', '3', 'Celeste'),
                ('Thiago', '15', '5', 'Federico')]

    consulta.multiple("""
    INSERT INTO estudiante(name, age, grade, fk_tutor_id)
    SELECT ?, ?, ?, t.id
    FROM tutor as t WHERE t.name = ?;
    """, estudiantes)
    

def fetch():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas de la tabla estudiante.
    # No debe imprimir el id del tutor, debe reemplazar el id por el nombre
    # del tutor en la query, utilizando el concepto de INNER JOIN,
    # se puede usar el WHERE en vez del INNER JOIN.
    # Utilizar fetchone para imprimir de una fila a la vez
    consulta.unique("""
        SELECT e.id, e.name, e.age, t.name
        FROM estudiante AS e
        INNER JOIN tutor AS t ON e.fk_tutor_id = t.id;""", 
"""
while True: 
    row = c.fetchone()
    if row is None:
        break
    print(row)""", script=True)


def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age / tutor_nombre
    consulta.unique("""
    SELECT e.id, e.name, e.age, t.name 
    FROM estudiante AS e
    INNER JOIN tutor AS t ON e.fk_tutor_id = t.id
    WHERE t.name = '{}';""".format(tutor), '[print(row) for row in query]')


def modify(id, name):
    print('Modificando la tabla')
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar el tutor asignado (fk_tutor_id --> id) por aquel que coincida
    # con el nombre del tutor pasado como parámetro
    consulta.unique("""
    UPDATE estudiante
    SET fk_tutor_id = (SELECT t.id FROM tutor as t WHERE t.name = '{}')
    WHERE id = {};""".format(name, id))


def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado
    resultado = consulta.unique("""SELECT COUNT(e.grade) FROM estudiante AS e
    WHERE e.grade = {}""".format(grade), '[row for row in query]')
    print(resultado[0][0])
    


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    tutor = 'Federico'
    search_by_tutor(tutor)

    nuevo_tutor = 'Celeste'
    id = 2
    modify(id, nuevo_tutor)

    grade = 5
    count_grade(grade)
