from ast import Delete
from email import header, headerregistry
import socket
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
from xml.etree.ElementTree import tostring

import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    titulo: str = None
    detalhes: str = ''

class ConnDatabase():
    def __init__(self, bd):
        self.conn = sqlite3.connect(f'{bd}.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS notas ( id INTEGER PRIMARY KEY UNIQUE, titulo STRING , detalhes STRING NOT NULL)");

    def add(self, note):
        self.conn.execute(f"INSERT INTO notas (titulo, detalhes) VALUES ('{note.titulo}', '{note.detalhes}')");
        self.conn.commit();
    
    def loadAll(self):
        data = self.conn.execute("SELECT * FROM notas");
        list = []
        for linha in data:
            note = Note(linha[0],linha[1],linha[2])
            list.append(note)
        return list

    def update(self, data):
        self.conn.execute(f"UPDATE notas SET titulo = '{data.titulo}', detalhes = '{data.detalhes}' WHERE id = '{data.id}'");
        self.conn.commit();

    def delete(self,id):
        self.conn.execute(f"DELETE FROM notas WHERE id = '{id}'");
        self.conn.commit()

db = ConnDatabase('banco')

def extract_route(req):
    req = req.splitlines()
    path = req[0]
    path = path.split(" ")
    path = path[1].replace("/","",1)
    return path

def load_data():
    data = db.loadAll()
    print(data)
    return data  

def load_template(index):
    with open('templates/' + index, 'r', encoding="UTF-8") as f:
        data = f.read()
        return data

def addDB(dict):
    db.add(Note(titulo= dict.get('titulo'), detalhes=dict.get('detalhes')))
  
def updateDB(dict):
    updater = Note(id = dict.get('id'), titulo = dict.get('titulo'), detalhes = dict.get('detalhes'))
    db.update(updater)

def delDB(id):
    db.delete(id)

def read_file(file, buffer_size=2**10*8):
    with open(file,mode='rb') as f:
        while (byte := f.read()):
            return byte

def build_response(body='', code=200, reason='OK', headers=''):
    if headers == '':
        response = f'HTTP/1.1 {code} {reason}\n\n{body}'
    else:
        response = f'HTTP/1.1 {code} {reason}\n{headers}\n\n{body}'
    return response.encode()