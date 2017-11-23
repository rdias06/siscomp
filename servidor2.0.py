# encoding: utf-8
# -*- coding: cp1252 -*-.
#!/usr/bin/python

import socket
from multiprocessing import Process
from threading import Thread

def adicionarcontato(conn, data, identificador2) :
    a = 0
    bancodedados2 = open('usuarios.txt', 'r')
    for linha in bancodedados2:
        linha = linha.strip('\n')
        emailusuario = linha.split(';')
        if emailusuario == data[2]:
            a = a + 1
    bancodedados2.close()
    if a == 0:
        conn.sendall('naocadastrada')
    else:
        try:
            i = 0
            bancodedados = open('agenda.txt', 'r')
            for linha in bancodedados:
                linha = linha.strip('\n')
                emailusuario, emaiamigo = linha.split(';')
                if identificador2 != emailusuario:
                    pass
                if data[1] == emailamigo and identificador2 == emailusuario:
                    i = i + 1
                    conn.sendall('jaadicionada')
                    break
            bancodedados.close()
            if i == 0:
                add = open('agenda.txt', 'a')
                contato = []
                contato.append(identificador2)
                contato.append(data[2])
                sep = ';'
                dados = sep.join(contato)
                add.write(dados)
                add.write('\n')
                add.close()
                conn.sendall('ok')
        except Exception :
            print 'erro'

def fazercadastro(conn, data):
    try:
        i = 0
        bancodedados = open("usuarios.txt","r")
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email = linha.split(";")
            if email == data[2]:
                i = i+1
                raise
        bancodedados.close()
        if i == 0:
            bancodedados = open('usuarios.txt', 'a')
            dados = []
            dados.append(data[1])
            dados.append(data[2])
            dados.append(data[3])
            sep = ';'
            dadoscliente = sep.join(dados[1:3])
            bancodedados.write(str(dadoscliente))
            bancodedados.write("\n")
            bancodedados.close()
            conn.sendall('ok')
    except Exception :
        conn.sendall('erro')

def mensagensoffline(identificador2):
    i = 0
    msg = open('mensagensoffline.txt', 'r')
    msg2 = open('mensagensoffline2.txt', 'w')
    for linha in msg:
        linha = linha.strip('\n')
        email, contato,  mensagem = linha.split(';')
        if email != identificador2:
            pass
        else:
            i = i + 1
            l = []
            l.append(contato)
            l.append(mensagem)
            sep = ';'
            envio = sep.join(l)
            conn.sendall(str(envio))
            msg2.write(linha)
            msg2.write('\n')
            msg2.close()
            msg.close()
            os.remove('mensagensoffline.txt')
            os.rename('mensagensoffline2.txt', 'mensagensoffline.txt')
        if i == 0 :
            conn.sendall('semmsg')


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
            if (nome == data[1]) or (senha == data[2]):
                i = i + 1
            if (nome == data[1]) and (senha == data[2]):
                usuariosonlinemsg.has_key(data[3])
                if False :
                    identificador1 = nome
                    identificador2 = email
                    usuariosonlineadd[conn] = email
                    usuariosonlineamsg[email] = conn
                    mensagensoffline(identificador2)
                else :
                    conn.sendall('emuso')
        bancodedados.close()
        if i == 0 :
            conn.sendall('naoexiste')
    except Exception :
        print ('erro')


def mensagemamigo(conn, data, identificador2):
    try:
        bancodedados = open("agenda.txt", "r")
        i = 0
        for linha in bancodedados:
            linha = linha.strip("\n")
            emailusuario, emailamigo = linha.split(";")
            if emailusuario != identificador2 :
                pass
            else:
                if emailamigo != data[2]:
                    i = i +1
        bancodedados.close()
        if i == 0 :
            conn.sendall('naoagenda')
        if i != 0 :
            c = usuariosonlineamsg.get(data[2])
            if c != 0 :
                msg = []
                msg.append(usuariosonlineadd.get(conn))
                msg.append(data[3])
                sep = ';'
                mensagem = sep.join(msg)
                c.sendall(strg(mensagem))
                conn.sendall('ok')
            else :
                l = []
                l.append(data[2])
                l.append('mensagemamigo')
                l.append(identificador1)
                l.append(data[3])
                sep = ';'
                offline = sep.join(l)
                bancodedados2 = open('mensagensoffline.txt', 'a')
                bancodedados2.write(str(offline))
                conn.sendall('amigooffline')
    except Exception :
        print ('erro')

def mensagemgrupo(conn, data , identificador1):
    try:
        bancodedados = open("grupos.txt", "r")
        i = 1
        c = 1
        for linha in bancodedados:
            linha = linha.strip("\n")
            grupo = []
            grupo[:] = linha.split(";")
            if grupo[0] != data[2]:
                pass
            if grupo[0] == data[2]:
                while c < len(grupo) :
                    if usuariosonlineadd.get(conn) == grupo[c] :
                        while i < len(grupo) :
                            msg = usuariosonlineamsg.get(grupo[i])
                            if msg != 0 :
                                identificadorgrupo = grupo[0]
                                identificador = usuariosonlineadd.get(conn)
                                l = []
                                l.append('mensagemgrupo')
                                l.append(identificadorgrupo)
                                l.append(identificador)
                                l.append(data[3])
                                sep = ';'
                                mensagem = sep.join(l)
                                msg.sendall(strg(mensagem))
                            else:
                                identificadorgrupo = grupo[0]
                                identificador = usuariosonlineadd.get(conn)
                                l = []
                                l.append(grupo[i])
                                l.append('mensagemgrupo')
                                l.append(identificadorgrupo)
                                l.append(identificador)
                                l.append(data[3])
                                sep = ';'
                                mensagem = sep.join(l)
                                bancodedados2 = open('mensagensoffline.txt', 'a')
                                bancodedados2.write(str(mensagem))
                    else :
                        c = c + 1
                if c == len(grupo) -1 :
                    conn.sendall('naoestanogrupo')
                else :
                    conn.sendall('ok')
    except Exception :
        print ('erro')


def criargrupo(conn, data, identificador2):
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
                bancodedados.close()
                break
        if i == 0 :
            add = open('grupos.txt', 'a')
            lista = []
            lista.append(data[1])
            lista.append(identificador2)
            cont = 2
            while cont < len(data):
                lista.append(data[cont])
                cont = cont + 1
            sep = ';'
            dados = sep.join(lista[0:len(lista)])
            add.write(str(dados))
            add.write('\n')
            add.close()
            conn.sendall('ok')
    except Exception :
        print('erro')

def excluirgrupo(conn, data, identificador2):
    try:
        i = 0
        bancodedados = open('grupos.txt', 'r')
        bancodedados2 = open('grupos2.txt', 'w')
        for linha in bancodedados:
            linha = linha.strip('\n')
            grupo = []
            grupo[:] = linha.split(';')
            if grupo[0] == data[2] :
                if grupo[1] != identificador2 :
                    conn.sendall('naocriou')
                    i = i +1
                    bancodedados2.close()
                    bancodedados.close()
                if i == 0:
                    bancodedados2.write(linha)
                    bancodedados2.write('\n')
                    bancodedados2.close()
                    bancodedados.close()
                os.remove('bancodedados.txt')
                os.rename('bancodedados2.txt', 'bancodedados.txt')
                conn.sendall('ok')
    except Exception :
        print('erro')


def addaogrupo(conn, data, identificador2):
    try:
        i = 0
        t = 0
        bancodedados = open("usuarios.txt", 'r')
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email = linha.split(";")
            if (email != data[2]):
                pass
            if (email == data[2]):
                i = i +1
                break
        bancodedados.close()
        bancodedados4 = open("agenda.txt", 'r')
        for linha in bancodedados4:
            linha = linha.strip("\n")
            emailusurario, emailamigo = linha.split(";")
            if emailusurario != identificador2:
                pass
            if emailusurario == identificador2 and emailamigo == data[2]:
                t = t + 1
                break
        bancodedados4.close()
        if t == 0:
            conn.sendall('naoagenda')
        if i !=0 and t != 0:
            c = 0
            h = 0
            bancodedados2 = open('grupos.txt', 'r')
            for linha in bancodedados2:
                linha = linha.strip('\n')
                grupo = []
                grupo[:] = linha.split(';')
                if grupo[0] == data[1]:
                    while h < len(grupo):
                        if grupo[h] == identificador2:
                            h = h +1
                        else:
                            pass
                    if h != 0:
                        while c < len(grupo):
                            if grupo[c] == data[2]:
                                conn.sendall('jaesta')
                                break
                            else:
                                c = c +1
                        bancodedados2.close()
                if c != 0 :
                    grupos = open('grupos.txt', 'r')
                    grupos2 = open('grupos2.txt', 'w')
                    for linha in grupos:
                        linha = linha.strip('\n')
                        grupo2 = []
                        grupo2[:] = linha.split(';')
                        if grupo2[0] == data[1]:
                            g = grupo2
                            g.append(data[2])
                            pass
                        else:
                            grupos2.write(linha)
                            grupos2.write('\n')
                            grupos2.close()
                            grupos.close()
                        os.remove('grupos.txt')
                        os.rename('grupos2.txt', 'grupos.txt')
                    bancodedados3 = open('grupos', 'a')
                    bancodedados3.write(c)
                    bancodedados3.write('\n')
                    bancodedados3.close()
                    conn.sendall('ok')
    except Exception :
        print ('erro')

def sair(conn, identificador2):
    usuariosonlineadd.pop(conn)
    usuariosonlineamsg.pop(identificador2)
    conn.sendall('ok')

def numeroparametros(msg):

    i = 1
    for separador in msg:
        if separador == ';' :
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
                sair(conn, identificador2)
        if int(numeros == 2):
            if data[0] == "adicionarcontato":
                adicionarcontato(conn, dados, identificador2)
            else:
                excluirgrupo(conn, dados, identificador2)
        if int(numeros) > 3:
            if data[0] == 'criargrupo':
                criargrupo(conn, dados, identificador2)
            else:
                fazercadastro(conn, dados)
        if int(numeros == 3):
            if dados[0] == "fazerlogin":
                fazerlogin(conn, dados)
            if dados[0] == "mensagemgrupo":
                mensagemgrupo(conn, dados, identificador1)
            if dados[0] == "mensagemamigo":
                mensagemamigo(conn, dados, identificador2)
            if data[0] == 'addaogrupo':
                addaogrupo(conn, dados, identificador2)
        if not data: break
    conn.close()

if __name__ == '__main__':
    global str(identificador1) , str(identificador2)
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

    while True:
        s.listen(1)
        conn, addr = s.accept()
        t = Thread(target=aceitar, args=conn)
        t.start()