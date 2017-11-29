# encoding: utf-8
# -*- coding: cp1252 -*-.
#!/usr/bin/python

import socket
from multiprocessing import Process
from threading import Thread
import os
import sys



def adicionarcontato(conn, data, identificador2) :
    a = 0
    bancodedados2 = open('usuarios.txt', 'r')
    for linha in bancodedados2:
        linha = linha.strip('\n')
        nome, senha, email, connenviar = linha.split(';')
        if email == data[1]:
            a = a + 1
    bancodedados2.close()
    if a == 0:
        print('nao cadastrada')
        conn.sendall('naocadastrada')
    else:
        try:
            i = 0
            bancodedados = open('agenda.txt', 'r')
            for linha2 in bancodedados:
                linha2 = linha2.strip('\n')
                emailusuario, emailamigo = linha2.split(';')
                if data[1] == emailamigo and identificador2 == emailusuario:
                    i = i + 1
                    print('ja esta na agenda')
                    conn.sendall('jaadicionada')
            bancodedados.close()
            if i == 0:
                add = open('agenda.txt', 'a')
                l = []
                l.append(str(identificador2))
                l.append(data[1])
                sep = ';'
                dados = sep.join(l)
                add.write(dados)
                add.write('\n')
                add.close()
                print('contato adicionado')
                conn.sendall('ok')
        except Exception :
            print 'erro'

def fazercadastro(conn, data):
    try:
        i = 0
        bancodedados = open("usuarios.txt","r")
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email, connenviar = linha.split(";")
            if email == data[2]:
                i = i+1
                raise
        bancodedados.close()
        if i == 0:
            bancodedados2 = open('usuarios.txt', 'a')
            dados = []
            dados.append(data[1])
            dados.append(data[2])
            dados.append(data[3])
            dados.append('a')
            sep = ';'
            dadoscliente = sep.join(dados)
            bancodedados2.write(str(dadoscliente))
            bancodedados2.write("\n")
            bancodedados2.close()
            print ('cadastro feito')
            conn.sendall('ok')
    except Exception :
        conn.sendall('erro')

def mensagemamigo(conn, data, identificador1, identificador2, connparamensagem):
    try:
        bancodedados = open("agenda.txt", "r")
        i = 0
        for linha in bancodedados:
            linha = linha.strip("\n")
            emailusuario, emailamigo = linha.split(";")
            if emailusuario == identificador2 and emailamigo == data[1]:
                i = i + 1
        if i == 0 :
            conn.sendall('naoagenda')
        bancodedados.close()
        if i != 0 :
            if connparamensagem.has_key(data[1]):
                print (connparamensagem[data[1]])
                c = connparamensagem[data[1]]
                msg = []
                msg.append('mensagemamigo')
                msg.append(identificador2)
                msg.append(data[2])
                sep = ';'
                mensagem = sep.join(msg)
                c.sendall(str(mensagem))
                print('mensagem enviada de')
                print(identificador2)
                print('para')
                print(data[1])
                conn.sendall('ok')
            else :
                l = []
                l.append(data[1])
                l.append('mensagemamigo')
                l.append(identificador1)
                l.append(data[2])
                sep = ';'
                offline = sep.join(l)
                bancodedados2 = open('mensagensoffline.txt', 'a')
                bancodedados2.write(str(offline))
                conn.sendall('amigooffline')
    except Exception :
        print ('erro')

def mensagemgrupo(conn, data, identificador2, connparamensagem):
    try:
        bancodedados = open("grupos.txt", "r")
        i = 1
        c = 1
        for linha in bancodedados:
            linha = linha.strip("\n")
            grupo = []
            grupo[:] = linha.split(";")
            if grupo[0] == data[1]:
                while c < len(grupo) :
                    if identificador2 == grupo[c] :
                        while i < len(grupo) :
                            if connparamensagem.has_key(grupo[i]):
                                msg = connparamensagem[grupo[i]]
                                identificadorgrupo = grupo[0]
                                l = []
                                l.append('mensagemgrupo')
                                l.append(identificadorgrupo)
                                l.append(identificador2)
                                l.append(data[2])
                                sep = ';'
                                mensagem = sep.join(l)
                                msg.sendall(str(mensagem))
                                conn.sendall('ok')
                            else:
                                l = []
                                l.append(grupo[i])
                                l.append('mensagemgrupo')
                                l.append(grupo[0])
                                l.append(identificador2)
                                l.append(data[2])
                                sep = ';'
                                mensagem = sep.join(l)
                                bancodedados2 = open('mensagensoffline.txt', 'a')
                                bancodedados2.write(str(mensagem))
                                conn.sendal('ok')
                    else :
                        c = c + 1
                if c == len(grupo) -1 :
                    conn.sendall('naoestanogrupo')
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
                conn.send('grupojaexiste')
                bancodedados.close()
                break
        if i == 0 :
            a = 0
            add = open('grupos.txt', 'a')
            lista = []
            lista.append(data[1])
            lista.append(identificador2)
            cont = 2
            while cont < len(data):
                bancodedados2 = open('agenda.txt', 'r')
                for linha in bancodedados2:
                    linha = linha.strip('\n')
                    emailusuario, emailamigo = linha.split(';')
                    if emailusuario == identificador2 and emailamigo == data[cont]:
                        lista.append(data[cont])
                        a = a + 1
                bancodedados2.close()
                cont = cont + 1
            if a != len(data) - 2 :
                conn.sendall('erro')
            if a == len(data) - 2 :
                sep = ';'
                dados = sep.join(lista)
                add.write(str(dados))
                add.write('\n')
                add.close()
                conn.sendall('ok')
    except Exception :
        print('erro')

def excluirgrupo(conn, data, identificador2):
    try:
        bancodedados = open('grupos.txt', 'r')
        bancodedados2 = open('grupos2.txt', 'w')
        bancodedados2.close()
        for linha in bancodedados:
            linha = linha.strip('\n')
            grupo = []
            grupo[:] = linha.split(';')
            if grupo[0] == data[1] and grupo[1] != identificador2 :
                conn.sendall('naocriou')
                bancodedados.close()
            if grupo[0] != data[1] :
                bancodedados3 = open('grupos2.txt', 'a')
                bancodedados3.write(linha)
                bancodedados3.write('\n')
                bancodedados3.close()
        bancodedados.close()
        os.remove('grupos.txt')
        os.rename('grupos2.txt', 'grupos.txt')
        conn.sendall('ok')
    except Exception :
        print('erro')


def addaogrupo(conn, data, identificador2):
    try:
        i = 0
        t = 0
        bancodedados = open("usuarios.txt", 'r')
        for linha1 in bancodedados:
            linha1 = linha1.strip("\n")
            nome, senha, email, connenviar = linha1.split(";")
            if (email != data[2]):
                pass
            if (email == data[2]):
                i = i +1
        bancodedados.close()
        if i != 0:
            bancodedados4 = open("agenda.txt", 'r')
            for linha2 in bancodedados4:
                linha2 = linha2.strip("\n")
                emailusurario, emailamigo, connenviar = linha2.split(";")
                if emailusurario == identificador2 and emailamigo == data[2]:
                    print('achou na agenda')
                    t = t + 1
            bancodedados4.close()
            if t == 0:
                print('nao agenda')
                conn.sendall('naoagenda')
        if i == 0:
            print('nao cadastrado')
            conn.sendall('naocadastrado')
        if i !=0 and t != 0:
            try:
                c = 1
                h = 0
                y = 0
                p = 0
                r = 0
                bancodedados2 = open('grupos.txt', 'r')
                for linha3 in bancodedados2:
                    linha3 = linha3.strip('\n')
                    grupo = []
                    grupo[:] = linha3.split(';')
                    if grupo[0] == data[1]:
                        while h < len(grupo):
                            if grupo[h] == identificador2:
                                y = y + 1
                            h = h + 1
                    if y != 0:
                        while c < len(grupo):
                            if grupo[c] == data[2]:
                                print ('ja esta no grupo')
                                conn.sendall('jaesta')
                                r = r + 1
                            c = c +1
                    if y == 0:
                        print ('usuario nao está no grupo')
                        conn.sendall('naoestanogrupo')
                    bancodedados2.close()
                    if r == 0 :
                        grupos = open('grupos.txt', 'r')
                        grupos2 = open('grupos2.txt', 'w')
                        grupos2.close()
                        for linha4 in grupos:
                            linha4 = linha4.strip('\n')
                            grupo2 = []
                            grupo2[:] = linha4.split(';')
                            if grupo2[0] == data[1]:
                                grupo2.append(data[2])
                                sep = ';'
                                g = sep.join(grupo2)
                                print('usuario guardado na lista nova')
                                p = p + 1
                            else:
                                grupos3 = open('grupos2.txt', 'a')
                                grupos3.write(linha)
                                grupos3.write('\n')
                                grupos3.close()
                        grupos.close()
                        if p != 0:
                            bancodedados3 = open('grupos.txt', 'a')
                            bancodedados3.write(g)
                            bancodedados3.write('\n')
                            bancodedados3.close()
                            conn.sendall('ok')
                            os.remove('grupos.txt')
                            os.rename('grupos2.txt', 'grupos.txt')
                        if p == 0:
                            os.remove('grupos2.txt')
            except Exception :
                print('erro')
    except Exception :
        print ('erro')

def excluirconta(conn, data, identificador1) :
    try:
        i = 0
        bancodedados = open("usuarios.txt", 'r')
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email, connenviar = linha.split(";")
            if (nome == identificador1) and (senha != data[2]):
                i = i + 1
            if (nome == identificador1) and (senha == data[2]):
                try:
                    usuarios = open('usuarios.txt', 'r')
                    usuarios2 = open('usuarios2.txt', 'w')
                    usuarios2.close()
                    for linha2 in usuarios:
                        linha2 = linha2.strip('\n')
                        nome, senha, email, connenviar = linha2.split(';')
                        if email != data[1]:
                            usuarios3 = open('usuarios2.txt', 'a')
                            usuarios3.write(linha2)
                            usuarios3.write('\n')
                            usuarios3.close()
                    usuarios.close()
                    agenda = open('agenda.txt', 'r')
                    agenda2 = open('agenda2.txt', 'w')
                    agenda2.close()
                    try:
                        for linha3 in agenda:
                            linha3 = linha3.strip('\n')
                            emailusuario, emailamigo, connenviar = linha3.split(';')
                            if email != emailusuario or email != emailamigo :
                                agenda3 = open('agenda2.txt', 'a')
                                agenda3.write(linha3)
                                agenda3.write('\n')
                                agenda3.close()
                    except Exception :
                        print('erro')
                    agenda.close()
                    os.remove('usuarios.txt')
                    os.rename('usuarios2.txt', 'usuarios.txt')
                    os.remove('agenda.txt')
                    os.rename('agenda2.txt', 'agenda.txt')
                    conn.sendall('ok')
                except Exception:
                    print ('erro')
        bancodedados.close()
        if i != 0:
            conn.sendall('senhaerrada')
    except Exception:
        print ('erro')

def numeroparametros(info):
    i = 1
    for separador in info:
        if separador == ';' :
                i = i + 1
    return i

def aceitar(conn):
    identificador1 = 0
    identificador2 = 0
    global usuariosonlineadd , usuariosonlineamsg , connparamensagem
    while True:
        dadoscliente = conn.recv(1024)
        numeros = numeroparametros(dadoscliente)
        dados = []
        dados[:] = dadoscliente.split(';')
        if int(numeros == 1):
            if dados[0] == "sair":
                print('saindo da conta')
                usuariosonlineadd.pop(conn)
                usuariosonlineamsg.pop(identificador2)
                connparamensagem.pop(identificador2)
                conn.sendall('ok')
        if int(numeros == 2):
            if dados[0] == "adicionarcontato":
                print ('adicionando contato')
                adicionarcontato(conn, dados, identificador2)
            else:
                print ('excluindo grupo')
                excluirgrupo(conn, dados, identificador2)
        if int(numeros) > 3:
            if dados[0] == 'criargrupo':
                print ('criando grupo')
                criargrupo(conn, dados, identificador2)
            else:
                print ('fazendo cadastro')
                fazercadastro(conn, dados)
        if int(numeros == 3):
            if dados[0] == "fazerlogin":
                print ('fazendo login')
                try:
                    i = 0
                    bancodedados = open("usuarios.txt", 'r')
                    for linha in bancodedados:
                        linha = linha.strip("\n")
                        nome, senha, email, connenviar = linha.split(";")
                        if (nome == dados[1]) and (senha == dados[2]):
                            i = i + 1
                            print('login efetuado')
                            if not usuariosonlineamsg.has_key(email):
                                identificador1 = nome
                                identificador2 = email
                                usuariosonlineadd[conn] = email
                                usuariosonlineamsg[email] = conn
                                conn.sendall('ok')
                            else:
                                print('conta em uso')
                                conn.sendall('emuso')
                    bancodedados.close()
                    if i == 0:
                        print('senha ou nome errado.')
                        conn.sendall('naoexiste')
                except Exception:
                    print ('erro')
            if dados[0] == "mensagemgrupo":
                print ('mensagem grupo')
                mensagemgrupo(conn, dados, identificador2, usuariosonlineadd, connparamensagem)
            if dados[0] == "mensagemamigo":
                print ('mensagem amigo')
                mensagemamigo(conn, dados, identificador1, identificador2, connparamensagem)
            if dados[0] == 'addaogrupo':
                print ('add ao grupo')
                addaogrupo(conn, dados, identificador2)
            if dados[0] == 'excluirconta' :
                print ('excluir conta')
                excluirconta(conn, dados, identificador1)
            if dados[0] == 'recebe':
                print('guardando conn para usuario receber mensagens')
                try:
                    c = 0
                    bancodedados = open("usuarios.txt", 'r')
                    bancodedados2 = open("usuarios2.txt", 'w')
                    bancodedados2.close()
                    for linha in bancodedados:
                        linha = linha.strip("\n")
                        nome, senha, email, connenviar = linha.split(";")
                        if (nome == dados[1]) and (senha == dados[2]):
                            connparamensagem[email] = conn
                            print('conn para receber mensagem guardado')
                            conn.sendall('ok')
                except Exception:
                    print('erro')
        if not dadoscliente: break
    conn.close()

if __name__ == '__main__':
    global usuariosonlineadd, usuariosonlineamsg , connparamensagem
    usuariosonlineamsg = {}
    usuariosonlineadd = {}
    connparamensagem = {}
    HOST = ''
    PORT = 50999
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    a = open("usuarios.txt", 'a')
    a.close()
    a = open("mensagensoffline.txt", 'a')
    a.close()
    a = open("agenda.txt", 'a')
    a.close()
    a = open("grupos.txt", 'a')
    a.close()
    while True:
        s.listen(1)
        conn, addr = s.accept()
        t = Thread(target=aceitar, args=(conn,))
        t.start()