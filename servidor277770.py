# encoding: utf-8
# -*- coding: cp1252 -*-.
#!/usr/bin/python

import socket
from threading import Thread, Semaphore
import os
from time import sleep



def adicionarcontato(conn, data, identificador2) :
    global lock
    a = 0
    bancodedados2 = open('usuarios.txt', 'r')           #procura se quem quer add é cadastrada
    for linha in bancodedados2:
        linha = linha.strip('\n')
        nome, senha, email, connenviar = linha.split(';')
        if email == data[1]:
            a = a + 1
    bancodedados2.close()
    if a == 0:
        conn.sendall('naocadastrada')
    else:
        try:
            i = 0                                #procura se ja esta na agenda
            lock.acquire()
            bancodedados = open('agenda.txt', 'r')
            for linha2 in bancodedados:
                linha2 = linha2.strip('\n')
                emailusuario, emailamigo = linha2.split(';')
                if data[1] == emailamigo and identificador2 == emailusuario:
                    i = i + 1
                    conn.sendall('jaadicionada')
            bancodedados.close()
            lock.release()
            if i == 0:
                lock.acquire()
                add = open('agenda.txt', 'a')
                l = []
                l.append(str(identificador2))
                l.append(data[1])
                sep = ';'
                dados = sep.join(l)
                add.write(dados)
                add.write('\n')                              #adiciona a agenda
                add.close()
                conn.sendall('ok')
                lock.release()
        except Exception :
            print 'erro'

def fazercadastro(conn, data):
    global lock
    try:
        i = 0
        lock.acquire()
        bancodedados = open("usuarios.txt","r")
        for linha in bancodedados:
            linha = linha.strip("\n")                                     #procura se existe um usuario com os dados fornecidos
            nome, senha, email, connenviar = linha.split(";")
            if email == data[2]:
                i = i+1
                raise
        bancodedados.close()
        lock.release()
        if i == 0:                                        #cadastra o usuario
            lock.acquire()
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
            lock.release()
            listaoffline.append(data[2])
            conn.sendall('ok')
    except Exception :
        conn.sendall('erro')


def mensagemamigo(conn, data, identificador2, connparamensagem):
    global lock
    try:
        j = 0
        lock.acquire()
        bancodedados = open("usuarios.txt", 'r')
        for linha1 in bancodedados:
            linha1 = linha1.strip("\n")
            nome, senha, email, connenviar = linha1.split(";")               #verifica se o amigo esta cadastrado
            if (email == data[1]):
                j = j + 1
        bancodedados.close()
        lock.release()
        if j == 0:
            conn.sendall('naocadastrado')
        if j != 0:
            i = 0
            lock.acquire()
            bancodedados2 = open("agenda.txt", "r")
            for linha in bancodedados2:
                linha= linha.strip("\n")
                emailusuario, emailamigo = linha.split(";")
                if emailusuario == identificador2 and emailamigo == data[1]:            #verifica se esta na agenda
                    i = i + 1
            if i == 0 :
                conn.sendall('naoagenda')
            bancodedados2.close()
            lock.release()
            if i != 0 :
                if connparamensagem.has_key(data[1]):
                    c = connparamensagem[data[1]]
                    msg = []
                    msg.append('mensagemamigo')               #manda msg
                    msg.append(identificador2)
                    msg.append(data[2])
                    sep = ';'
                    mensagem = sep.join(msg)
                    c.sendall(str(mensagem))
                    conn.sendall('ok')
                if not connparamensagem.has_key(data[1]):
                    h = []
                    h.append('amigooffline')
                    h.append(identificador2)
                    h.append(data[1])                 #avisa pra guardar caso off
                    sep = ';'
                    info = sep.join(h)
                    conn.sendall(str(info))
    except Exception :
        print ('erro')

def mensagemgrupo(conn, data, identificador1, identificador2, connparamensagem):
    global lock
    try:
        l = []
        l.append(data[0])
        l.append(data[1])
        l.append(identificador1)
        l.append(data[2])
        sep = ';'
        mensagem = sep.join(l)
        controle2 = 0
        lock.acquire()
        bancodedados = open('grupos.txt', 'r')
        for linha in bancodedados:
            linha = linha.strip("\n")
            grupo = []
            grupo[:] = linha.split(";")                              #verifica se o usuario esta no grupo
            if grupo[0] == data[1]:
                controle2 = 1
                t = 0
                while t < len(grupo):
                    if grupo[t] == identificador2:
                        controle1 = 1
                    t = t + 1
                if controle1 == 0:
                    conn.sendall('naoestanogrupo')
                if controle1 == 1:
                    r = 1
                    cont = 0
                    while r < len(grupo):
                        if not connparamensagem.has_key(grupo[r]) :
                            cont = cont + 1
                        r = r + 1
                    if cont == 0 :
                        j = 1
                        while j < len(grupo):
                            c = connparamensagem[grupo[j]]
                            c.sendall(mensagem)                              #manda mensagem para todos
                            j = j + 1
                        conn.sendall('ok')
                    if cont != 0:
                        cont2 = []
                        cont2.append('naotodosonline')                           #manda guardar pq nao sao todos online
                        cont2.append(data[0])
                        cont2.append(data[1])
                        cont2.append(identificador1)
                        cont2.append(data[2])
                        w = 1
                        while w < len(grupo) :
                            if not connparamensagem.has_key(grupo[w]):
                                cont2.append(grupo[w])
                            if connparamensagem.has_key(grupo[w]):
                                cont2.append(grupo[w])
                            w = w + 1
                        sep = ';'
                        z = sep.join(cont2)
                        conn.sendall(str(z))
        bancodedados.close()
        lock.release()
        if controle2 == 0:
            conn.sendall('naoexiste')
    except Exception :
        print ('erro')

def criargrupo(conn, data, identificador2):
    global lock
    try:
        i = 0
        lock.acquire()
        bancodedados = open('grupos.txt', 'r')
        for linha in bancodedados:
            linha = linha.strip('\n')
            grupo = []                  #ve se o nome ja existe
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
                    if emailusuario == identificador2 and emailamigo == data[cont]:         #verifica se todos os usuarios estao na agenda do cliente
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
                add.write('\n')                        #salva o grupo
                add.close()
                conn.sendall('ok')
        bancodedados.close()
        lock.release()
    except Exception :
        print('erro')

def excluirgrupo(conn, data, identificador2):
    global lock, lock3
    try:
        lock.acquire()
        bancodedados = open('grupos.txt', 'r')
        lock3.acquire()
        bancodedados2 = open('grupos2.txt', 'w')                    #exclui grupo que o cliente fez
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
                lock3.release()
        bancodedados.close()
        lock.release()
        os.remove('grupos.txt')
        os.rename('grupos2.txt', 'grupos.txt')
        try:
            os.remove('grupos2.txt')
        except Exception :
            print('grupos2 ja deletado')
        conn.sendall('ok')
    except Exception :
        print('erro')


def addaogrupo(conn, data, identificador2):
    global lock, lock3
    try:
        i = 0
        t = 0
        lock.acquire()
        bancodedados = open("usuarios.txt", 'r')
        for linha1 in bancodedados:
            linha1 = linha1.strip("\n")
            nome, senha, email, connenviar = linha1.split(";")          #verifica se amigo existe
            if (email == data[2]):
                i = i +1
        bancodedados.close()
        lock.release()
        if i != 0:
            lock.acquire()
            bancodedados4 = open("agenda.txt", 'r')
            for linha2 in bancodedados4:
                linha2 = linha2.strip("\n")
                emailusurario, emailamigo = linha2.split(";")
                if emailusurario == identificador2 and emailamigo == data[2]:        #verifica se esta na agenda
                    t = t + 1
            bancodedados4.close()
            lock.release()
            if t == 0:
                conn.sendall('naoagenda')
        if i == 0:
            conn.sendall('naocadastrado')
        if i !=0 and t != 0:
            try:
                c = 1
                h = 0
                y = 0
                p = 0
                r = 0
                lock.acquire()
                bancodedados2 = open('grupos.txt', 'r')
                for linha3 in bancodedados2:
                    linha3 = linha3.strip('\n')
                    grupo = []
                    grupo[:] = linha3.split(';')
                    if grupo[0] == data[1]:
                        while h < len(grupo):
                            if grupo[h] == identificador2:
                                y = y + 1                                          #verifica se amigo e usuario estao no grupo
                            h = h + 1
                    if y != 0:
                        while c < len(grupo):
                            if grupo[c] == data[2]:
                                conn.sendall('jaesta')
                                r = r + 1
                            c = c +1
                    if y == 0:
                        conn.sendall('naoestanogrupo')
                bancodedados2.close()
                lock.release()
                if r == 0 :
                    lock.acquire()
                    grupos = open('grupos.txt', 'r')
                    lock3.acquire()
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
                        if grupo2[0] != data[1]:                                                  #adiciona ao grupo
                            grupos3 = open('grupos2.txt', 'a')
                            grupos3.write(linha4)
                            grupos3.write('\n')
                            grupos3.close()
                    lock3.release()
                    grupos.close()
                    lock.release()
                    lock.acquire()
                    os.remove('grupos.txt')
                    os.rename('grupos2.txt', 'grupos.txt')
                    lock.release()
                    if p != 0 :
                        lock.acquire()
                        bancodedados3 = open('grupos.txt', 'a')
                        bancodedados3.write(g)
                        bancodedados3.write('\n')
                        bancodedados3.close()
                        lock.release()
                        conn.sendall('ok')
            except Exception :
                print('erro dentro')          #####ta imprimindo erro mesmo com o programa funcionando
    except Exception :
        print ('erro fora')

def excluirconta(conn, data, identificador1, identificador2, connparamsg) :
    global lock, lock3
    try:
        i = 0
        q = 0
        lock.acquire()
        bancodedados = open("usuarios.txt", 'r')
        for linha in bancodedados:
            linha = linha.strip("\n")
            nome, senha, email, connenviar = linha.split(";")
            if (nome == identificador1 == data[1]) and (senha != data[2]):            #verifica se os dados passados batem com o banco de dados
                q = q + 1
            if (nome == identificador1) and (senha == data[2]):
                i = 2
        bancodedados.close()
        lock.release()
        if q != 0 :
            conn.sendall('senhaerrada')
        if i == 2 :
            try:
                try:
                    lock.acquire()
                    usuarios = open('usuarios.txt', 'r')
                    lock3.acquire()
                    usuarios2 = open('usuarios2.txt', 'w')
                    usuarios2.close()                                              #exclui o usuario da lista de cadastrados, a agenda dele e
                    for linha2 in usuarios:                                        #ele da agenda de quem o tem e exclui todos os grupos que o ucuario participa
                        linha2 = linha2.strip('\n')
                        nome, senha, email, connenviar = linha2.split(';')
                        if email != data[1]:
                            usuarios3 = open('usuarios2.txt', 'a')
                            usuarios3.write(linha2)
                            usuarios3.write('\n')
                            usuarios3.close()
                            lock3.release()
                    lock3.release()
                    usuarios.close()
                    lock.release()
                    lock.acquire()
                    os.remove('usuarios.txt')
                    os.rename('usuarios2.txt', 'usuarios.txt')
                    lock.release()
                except Exception :
                    lock3.acquire()
                    print('erro excluindo de usuarios')
                    lock3.release()
                try:
                    lock.acquire()
                    agenda = open('agenda.txt', 'r')
                    lock3.acquire()
                    agenda2 = open('agenda2.txt', 'w')
                    agenda2.close()
                    for linha3 in agenda :
                        linha3 = linha3.strip('\n')
                        emailusuario, emailamigo = linha3.split(';')
                        if data[1] != emailusuario and data[1] != emailamigo :
                            agenda3 = open('agenda2.txt', 'a')
                            agenda3.write(linha3)
                            agenda3.write('\n')
                            agenda3.close()
                            lock3.release()
                    agenda.close()
                    lock.release()
                except Exception :
                    lock.acquire()
                    print('erro excluindo agenda')
                    lock.release()
                lock.acquire()
                os.remove('agenda.txt')
                os.rename('agenda2.txt', 'agenda.txt')
                lock.release()
                try:
                    cont = 0
                    lock.acquire()
                    grupos = open('grupos.txt', 'r')
                    lock3.acquire()
                    grupos2 = open('grupos2.txt', 'w')
                    for linha4 in grupos:
                        linha4 = linha4.strip('\n')
                        grupo = []
                        grupo[:] = linha4.split(';')
                        i = 0
                        while i < len(grupo):
                            if grupo[i] == identificador2:
                                cont = cont + 1
                            i = i + 1
                        if cont == 0:
                            grupos2.close()
                            grupos3 = open('grupos2.txt', 'a')
                            grupos3.write(linha4)
                            grupos3.write('\n')
                            grupos3.close()
                            lock3.release()
                            grupos.close()
                            lock.release()
                    grupos2.close()
                    lock3.release()
                    if cont != 0 :
                        grupos.close()
                        lock.release()
                        lock.acquire()
                        os.remove('grupos.txt')
                        os.rename('grupos2.txt', 'grupos.txt')
                        lock.release()
                except Exception :
                    lock.acquire()
                    print('erro excluindo grupo')
                    lock.release()
            except Exception :
                lock.acquire()
                print ('erro')
                lock.release()
        conn.sendall('ok')
    except Exception:
        lock.acquire()
        print ('erro')
        lock.release()

def sairdegrupo(conn, data, identificador2):
    global lock, lock3
    print 'to na funcao'
    p = 0
    try:
        h = 0
        y = 0
        d = 0
        lock.acquire()
        bancodedados5 = open('grupos3.txt', 'w')
        bancodedados5.close()
        lock3.acquire()
        bancodedados2 = open('grupos.txt', 'r')
        for linha3 in bancodedados2:
            linha3 = linha3.strip('\n')
            grupo = []
            grupo[:] = linha3.split(';')
            if grupo[0] == data[1]:
                temp = []
                while h < len(grupo):
                    if grupo[h] == identificador2:
                        y = y + 1
                        print 'achei o usuario     '# verifica se amigo e usuario estao no grupo
                    if grupo[h] != identificador2:
                        d = 1
                        temp.append(grupo[h])
                    h = h + 1
            if grupo[0] != data[1]:
                bancodedados6 = open('grupos3.txt', 'a')
                bancodedados6.write(linha3)
                bancodedados6.write('\n')
                bancodedados6.close()
            if d == 1:
                print 'salvando o grupo sem o usuario'
                p = 1
                sep = ';'
                temp2 = sep.join(temp)
                print temp2
                bancodedados4 = open('grupos3.txt', 'a')
                bancodedados4.write(temp2)
                bancodedados4.write('\n')
                bancodedados4.close()
                conn.sendall('saiudogrupo')
            if y == 0:
                conn.sendall('naosaiudogrupo')
        lock.release()
        bancodedados2.close()
        lock3.release()
        if p == 1:
            os.remove('grupos.txt')
            os.rename('grupos3.txt', 'grupos.txt')
    except Exception:
        print 'erro sair grupo'


def numeroparametros(info):
    global lock
    i = 1
    for separador in info:
        if separador == ';' :                  #contador de numero de dados que o cliente enviou
                i = i + 1
    return i

def aceitar(conn):
    identificador1 = 0
    identificador2 = 0
    global usuariosonlineadd , usuariosonlineamsg , connparamensagem, listaonline, emailparaonline, emailparaoffline, identificador4, lock
    while True:
        dadoscliente = conn.recv(1024)
        numeros = numeroparametros(dadoscliente)
        dados = []
        dados[:] = dadoscliente.split(';')
        if int(numeros == 1):                                                  #de acordo com o primeiro dado enviado pelo cliente, o servidor executa uma funcao designada
            if dados[0] == "sair":
                usuariosonlineadd.pop(conn)
                usuariosonlineamsg.pop(identificador2)
                connparamensagem.pop(identificador2)
                if connparamensagem.has_key(identificador2):              ###sai da conta liberando um lugar de acesso ao servidor e guardando/deletando as informacoes necessarias
                    try:
                        i = 0
                        while i < len(listaonline):
                            if listaonline[i] == identificador2:
                                del listaonline[i]
                                listaoffline.append(identificador2)
                            i = i + 1
                    except Exception:
                        lock.acquire()
                        print('erro excluindo da lista de online')
                        lock.release()
                conn.sendall('ok')
            if dados[0] == 'fecharsocket':
                conn.close()
            if dados[0] == 'adicionarcontatos':
                conn.sendall('ok')
                try:
                    f = open('adicionarcontatos de '+conn+ '.txt', 'wb')
                    while (True):
                        l = conn.recv(1024)
                        while (l):
                            f.write(l)
                            l = conn.recv(1024)
                    f.close()
                except Exception:
                    lock.acquire()
                    print 'erro ao receber a lista de contatos para cadastrar'
                    lock.release()
                try:
                    lock.acquire()
                    bancodedados2 = open('adicionarusuarios de '+conn+ '.txt', 'wb')
                    for linha in bancodedados2:
                        linha = linha.strip('\n')
                        contatoparaadd = linha.split(';')
                        a = 0
                        lock3.acquire()
                        bancodedados3 = open('usuarios.txt', 'r')
                        for linha2 in bancodedados3:
                            linha2 = linha2.strip('\n')
                            nome, senha, email, connenviar = linha2.split(';')
                            if email == contatoparaadd:
                                a = a + 1
                        bancodedados3.close()
                        lock3.release()
                        if a == 0:
                            print('nao cadastrada')
                        else:
                            try:
                                lock3.acquire(())
                                add = open('agenda.txt', 'a')
                                l = []
                                l.append(str(identificador2))
                                l.append(contatoparaadd)
                                sep = ';'
                                dados = sep.join(l)
                                add.write(dados)
                                add.write('\n')
                                add.close()
                                lock3.release()
                            except Exception:
                                lock3.acquire()
                                print 'erro ao adicionar contatos à agenda.'
                                lock3.release()
                    bancodedados2.close()
                    lock.release()
                    try:
                        lock.acquire()
                        os.remove('adicionarusuarios.txt')
                        lock.release()
                    except Exception:
                        lock.acquire()
                        print 'erro ao excluir o txt de adicionar usuarios'
                        lock.release()
                except Exception:
                    lock.acquire()
                    print 'erro ao entrar no txt adicionarcontatos.txt'
                    lock.release()
        if int(numeros == 2):
            if dados[0] == "adicionarcontato":
                adicionarcontato(conn, dados, identificador2)
            else:
                excluirgrupo(conn, dados, identificador2)
            if dados[0] == 'sairgrupo':
                sairdegrupo(conn, dados, identificador2)
        if int(numeros) > 3:
            if dados[0] == 'criargrupo':
                criargrupo(conn, dados, identificador2)
            else:
                fazercadastro(conn, dados)
        if int(numeros == 3):
            if dados[0] == "fazerlogin":
                try:
                    i = 0
                    lock.acquire()
                    bancodedados = open("usuarios.txt", 'r')
                    for linha in bancodedados:
                        linha = linha.strip("\n")
                        nome, senha, email, connenviar = linha.split(";")
                        if (nome == dados[1]) and (senha == dados[2]):
                            i = i + 1
                            if not usuariosonlineamsg.has_key(email):
                                identificador1 = nome
                                identificador2 = email
                                usuariosonlineadd[conn] = email
                                usuariosonlineamsg[email] = conn                   #guarda variaveis para uso em futuras funcoes
                                listaonline.append(identificador2)
                                listaoffline.remove(identificador2)
                                print('email salvo na lista de online')
                                e = []
                                e.append('ok')
                                e.append(identificador2)
                                sep = ';'
                                r = sep.join(e)
                                conn.sendall(str(r))
                            else:
                                conn.sendall('emuso')
                    bancodedados.close()
                    lock.release()
                    if i == 0:
                        conn.sendall('naoexiste')
                except Exception:
                    print ('erro')
            if dados[0] == "mensagemgrupo":
                mensagemgrupo(conn, dados, identificador1, identificador2, connparamensagem)
            if dados[0] == "mensagemamigo":
                mensagemamigo(conn, dados, identificador2, connparamensagem)
            if dados[0] == 'addaogrupo':
                addaogrupo(conn, dados, identificador2)
            if dados[0] == 'excluirconta' :
                excluirconta(conn, dados, identificador1, identificador2, connparamensagem)
            if dados[0] == 'recebemensagem':
                try:
                    lock.acquire()
                    bancodedados = open("usuarios.txt", 'r')                    #guarda o conn do socket que recebe mensagens
                    for linha in bancodedados:
                        linha = linha.strip("\n")
                        nome, senha, email, connenviar = linha.split(";")
                        if (nome == dados[1]) and (senha == dados[2]):
                            connparamensagem[email] = conn
                            print('conn para receber de ' + email + ' mensagem guardado')
                            conn.sendall('ok')
                    bancodedados.close()
                    lock.release()
                except Exception :
                    lock.acquire()
                    print('erro')
                    lock.release()
            if dados[0] == 'recebequemestaonline':
                try:
                    lock.acquire()
                    bancodedados = open("usuarios.txt", 'r')
                    for linha in bancodedados:
                        linha = linha.strip("\n")
                        nome, senha, email, connenviar = linha.split(";")
                        if (nome == dados[1]) and (senha == dados[2]):
                            emailparaonline[conn] = email
                            identificador3 = email
                            conn.sendall('ok')
                    bancodedados.close()
                    lock.release()
                    try:
                        tt = 0
                        while tt < 10:
                            i = 0
                            c = len(listaonline)
                            while i < c:
                                contato = listaonline[i]
                                print contato
                                l = []
                                l.append('contatoonline')
                                l.append(contato)
                                sep = ';'
                                envio = sep.join(l)
                                conn.sendall(str(envio))
                                if i == len(listaonline):
                                    i = 0
                                i = i + 1
                            if tt == 10:
                                tt = 0
                            tt = tt + 1
                    except Exception:
                        print('erro 2')
                except Exception:
                    print('erro 1')
            if dados[0] == 'recebequemestaoffline':
                try:
                    lock.acquire()
                    bancodedados = open("usuarios.txt", 'r')
                    for linha in bancodedados:
                        linha = linha.strip("\n")
                        nome, senha, email, connenviar = linha.split(";")
                        if (nome == dados[1]) and (senha == dados[2]):
                            emailparaoffline[conn] = email
                            identificador3 = email
                            identificador4 = nome
                            conn.sendall('ok')
                    bancodedados.close()
                    lock.release()
                    try:
                        j = 1
                        while j < 10 :
                            i = 0
                            c = len(listaoffline)
                            while i < c :
                                contato = listaoffline[i]
                                l = []
                                l.append('contatooffline')
                                l.append(contato)
                                sep = ';'
                                envio = sep.join(l)
                                conn.sendall(str(envio))
                                try:
                                    while True:
                                        dadoscliente2 = conn.recv(1024)
                                        q = []
                                        q[:] = dadoscliente2.split(';')
                                        if q[0] == "mensagemgrupo":
                                            identificador3 = emailparaoffline[conn]
                                            mensagemgrupo(conn, q, identificador4, identificador3, connparamensagem)
                                        if not dadoscliente2: break
                                except Exception:
                                    print 'erro'
                                i = i + 1
                            if j == 9:
                                f = 0
                                j = f
                            j = j + 1
                    except Exception:
                        print('erro 2')
                except Exception:
                    print('erro 1')
        if not dadoscliente: break
    conn.close()

if __name__ == '__main__':
    global usuariosonlineadd, usuariosonlineamsg , connparamensagem, listaonline, emailparaonline, emailparaoffline, listaoffline, identificador4, lock2, lock, lock3
    usuariosonlineamsg = {}
    usuariosonlineadd = {}
    connparamensagem = {}
    listaonline = []
    emailparaonline = {}
    emailparaoffline = {}
    listaoffline = []
    HOST = ''
    PORT = 50999
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    a = open("usuarios.txt", 'a')
    a.close()
    a = open("agenda.txt", 'a')
    a.close()
    a = open("grupos.txt", 'a')
    a.close()
    lock = Semaphore(1)
    lock3 = Semaphore(1)
    lock2 = Semaphore(20)
    bancodedados = open("usuarios.txt", 'r')
    for linha in bancodedados:
        linha = linha.strip("\n")                                 #guarda em uma lista todos que estão offline na hora que o servidor comeca a rodar
        nome, senha, email, connenviar = linha.split(";")
        listaoffline.append(email)
    bancodedados.close()
    while True:
        lock2.acquire()                                           #limita a 5 usuarios no servidor por vez
        s.listen(1)
        conn, addr = s.accept()
        t = Thread(target=aceitar, args=(conn,))                    #aceita um usuario
        t.start()