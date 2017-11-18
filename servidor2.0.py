# encoding: utf-8
# -*- coding: cp1252 -*-.
#!/usr/bin/python

import socket
from multiprocessing import Process
from threading import Thread

def adicionarcontato(conn, data) :
    a = 0
    c = 0
    bancodedados2 = open('usuarios.txt', 'r')
    for linha in bancodedados2:
        linha = linha.strip('\n')
        emailusuario = linha.split(';')
        c = c + 1
        if emailusuario != data[1]:
            a = a + 1
    bancodedados2.close()
    if a != c :
        try:
            i = 0
            bancodedados = open('agenda.txt', 'r')
            for linha in bancodedados:
                linha = linha.strip('\n')
                emailusuario, emaiamigo = linha.split(';')
                if usuariosonline.get(conn) != emailusuario:
                    pass
                else:
                    if data[1] == emailamigo:
                        i = i + 1
                        conn.sendall('jaadicionada')
                        break
            bancodedados.close()
            if i == 0:
                add = open('agenda.txt', 'a')
                contato = []
                contato.append(data[1])
                contato.append(data[2])
                sep = ';'
                dados = sep.join(contato[0:1])
                add.write(dados)
                add.write('\n')
                add.close()
                conn.sendall('ok')
    else :
        conn.sendall('naocadastrada')

def fazercadastro(conn, data):
    try:
        i = 0
        bancodedados = open("usuarios.txt","r")
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email = linha.split(";")
            if email == data[2]:
                i = i+1
                conn.sendall('erro')
                break
        bancodedados.close()
        if i == 0:
            bancodedados = open('usuarios.txt', 'a')
            dados = []
            dados.append(data[1])
            dados.append(data[2])
            dados.append(data[3])
            sep = (";")
            dadoscliente = sep.join(dados[1:3])
            bancodedados.write(str(dadoscliente))
            bancodedados.write("\n")
            bancodedados.close()
            conn.sendall('ok')

def fazerlogin(conn, data):
    global identificador1, identificador2
    try:
        i = 0
        bancodedados = open("usuarios.txt", 'r')
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email = linha.split(";")
            if (nome != data[1]) and (senha != data[2]):
                pass
            if (nome == data[1]) and (senha == data[2]):
                teste = usuariosonlinemsg.has_key(data[3])
                if teste == 0 :
                    identificador1 = nome
                    identificador2 = email
                    usuariosonlineadd[conn] = email
                    usuariosonlineamsg[email] = conn
                    conn.sendall('ok')
                else :
                    conn.sendall('emuso')
        bancodedados.close()


def mensagemamigo(conn, data, identificador1):
    try:
        bancodedados = open("agenda.txt", "r")
        i = 0
        for linha in bancodedados:
            linha = linha.strip("\n")
            emailusuario, emailamigo = linha.split(";")
            if emailusuario != usuariosonlineadd.get(conn) :
                pass
            if emailamigo != data[2]:
                i = i +1
        bancodedados.close()
        if i != 0 :
            c = usuariosonlineamsg.get(data[2])
            if c != 0 :
                msg = []
                msg.append(identificador1)
                msg.append(data[2])
                sep = ';'
                mensagem = sep.join(msg[0:1])
                c.sendall(strg(mensagem))
            else :
                l = []
                l.append(identificador1)
                l.append(data[2])
                sep = ';'
                offline = sep.join(l[0:1])
                bancodedados2 = open('mensagensoffline.txt', 'a')
                bancodedados2.write(str(offline))

def mensagemgrupo(conn, data , identificador1):
    global v
    try:
        bancodedados = open("grupos.txt", "r")
        i = 1
        c = 1
        for linha in bancodedados:
            linha = linha.strip("\n")
            grupo = []
            grupo = linha.split(";")
            if grupo[0] != data[1]:
                pass
            if grupo[0] == data[1]:
                while c < len(grupo) :
                if usuariosonlineadd.get(conn) == grupo[c] :
                    while i < len(grupo) :
                        msg = usuariosonlineamsg.get(grupo[i])
                        if msg != 0 :
                            v.append(identificador1)
                            v.append(data[2])
                            sep = ';'
                            mensagem = sep.join(v[0:1])
                            msg.sendall(strg(mensagem))
                        else:
                            l = []
                            l.append(identificador1)
                            l.append(usuariosonlineamsg.get(grupo[i]))
                            l.append(data[2])
                            sep = ';'
                            offline = sep.join(l[0:2])
                            bancodedados2 = open('mensagensoffline.txt', 'a')
                            bancodedados2.write(str(offline))
                else :
                    c = c + 1


def criargrupo(conn, data):
    try:
        i = 0
        bancodedados = open('grupos.txt', 'r')
        for linha in bancodedados:
            linha = linha.strip('\n')
            grupo = []
            grupo[:] = linha.split(';')
            if grupo[0] == data[1]:
                i = i +1
                conn.send('erro')
                break
            bancodedados.close()
        if i == 0 :
            add = open('grupos.txt', 'a')
            lista = []
            lista.append(data[0])
            cont = 1
            while cont < len(data):
                lista.append(data[cont])
                cont = cont + 1
            sep = ';'
            dados = sep.join(lista[0:(cont-1)])
            add.write(str(dados))
            add.write('\n')
            add.close()
            conn.sendall('ok')

def sair(conn):
    x = usuariosonlineadd.get(conn)
    usuariosonlineadd.pop(conn)
    usuariosonlineamsg.pop(x)
    conn.sendall('ok')

def numeroparametros(msg):

    i = 1
    for separador in msg:
        if (separador == ';'):
                i = i + 1
    return i

def aceitar(conn):
    while True:
        dadoscliente = conn.recv(1024)
        numeros = numeroparametros(dadoscliente)
        dados = []
        dados[:] = dadoscliente.split(';')
        if int(numeros == 1):
            if dados[0] == "sair":
                sair(conn)
        if int(numeros == 2):
            if data[0] == "adicionarcontato":
                adicionarcontato(conn, dados)
        if int(numeros) > 3:
            if data[0] == 'criar grupo':
                criargrupo(conn, dados)
            else:
                fazercadastro(conn, dados)
        if int(numeros == 3):
            if dados[0] == "fazerlogin":
                fazerlogin(conn, dados)
            if dados[0] == "mensagemgrupo":
                mensagemgrupo(conn, dados, identificador1)
            if dados[0] == "mensagemamigo":
                mensagemamigo(conn, dados, identificador1)
        if not data: break
    conn.close()

if __name__ == '__main__':
    global identificador1 , identificador2,
   HOST = ''
   PORT = 50999
   s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind((HOST, PORT))
   f.open("usuarios.txt", 'w')
   f.close()
   f.open("mensagensoffline.txt", 'w')
   f.close()
   f.open("agenda.txt", 'w')
   f.close()
   f.open("grupos.txt", 'w')
   f.close()
   usuariosonlineadd = {}
   usuariosonlineamsg = {}
   v = []

   while True:
       s.listen(1)
       conn, addr = s.accept()
       t = Thread(target=aceitar, args=(conn))
       t.start()