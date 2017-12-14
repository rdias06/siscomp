# encoding: utf-8
# -*- coding: cp1252 -*-.
#!/usr/bin/python

import socket

from multiprocessing import Process
from threading import Thread
from time import  sleep
import os
import sys

def thread4():
    class mensagem:
        def __init__(self, nome="", senha="", login="", email=""):
            self.nome = nome
            self.senha = senha
            self.email = email
            self.login = login

        def mensagemgrupo(self):
            global enviogrupo, nomegrupo
            s.sendall(str(enviogrupo))
            confirmacao2 = s.recv(1024)
            if confirmacao2 == 'ok':
                print('Sua mensagem para o grupo'+nomegrupo+' foi enviada.\n')

        def recebermensagem(self):
            todosoffline= {}
            i = 1
            global nome, senha, login, email, enviogrupo, nomegrupo
            login = 0
            while i > 0:
                if login == 1:
                    l = []
                    l.append('recebequemestaoffline')
                    l.append(nome)
                    l.append(senha)
                    sep = ';'
                    info = sep.join(l)
                    s.sendall(str(info))
                    confirmacao = s.recv(1024)
                    if confirmacao == 'ok':
                        while 1 < 10 :
                            try:
                                dados = s.recv(1024)
                                mensagem = []
                                mensagem[:] = dados.split(';')
                                if mensagem[0] == 'contatooffline':
                                    todosoffline[mensagem[1]] = 'sim'
                                    bancodedados = open("mensagensofflinegrupo.txt", 'r')
                                    bancodedados3 = open('mensagensofflinegrupo2.txt', 'w')
                                    bancodedados3.close()
                                    contador3 = 0
                                    for linha in bancodedados:
                                        linha = linha.strip("\n")
                                        emailusuario, identificador, grupo, msg = linha.split(';')
                                        numerodeusuarios = len(grupo) - 4
                                        contador = 4
                                        contador2 = 0
                                        while contador < len(grupo):
                                            if todosoffline.has_key(grupo[contador]):
                                                contador2 = contador2 + 1
                                        if contador2 == 0:
                                            info = []
                                            info.append(identificador)  # identificador de mensagem offline
                                            info.append(grupo)  # emailamigo
                                            info.append(msg)  # mensagem
                                            sep = ';'
                                            enviogrupo = sep.join(info)
                                            nomegrupo = grupo
                                            u.mensagemgrupo()
                                        if contador2 == numerodeusuarios:
                                            contador3 = contador3 + 1
                                            bancodedados2 = open("mensagensofflinegrupo2.txt", 'a')
                                            info = []
                                            info.append(grupo[0])  # emailusuario
                                            info.append(grupo[1])  # emailcontato
                                            info.append(grupo[3])  # mensagem
                                            sep = ';'
                                            enviogrupo = sep.join(info)
                                            bancodedados2.write(enviogrupo)
                                            bancodedados2.write('\n')
                                            bancodedados2.close()
                                    bancodedados.close()
                                    if contador3 != 0 :
                                        try:
                                            os.remove('mensagensofflinegrupo.txt')
                                            os.rename('mensagensofflinegrupo2.txt', 'mensagensofflinegrupo.txt')
                                        except Exception:
                                            print('nao atualizou o txt')
                                    if contador3 == 0:
                                        os.remove('mensagensofflinegrupo2.txt')
                                if not dados: break
                            except Exception:
                                print('erro enviar mensagem grupo off')
                            sleep(1)
                            i = 0
                        i = i + 1
                    if not confirmacao: break
                i = i + 1
    global enviogrupo, nomegrupo
    HOST = '127.0.0.1'
    PORT = 50999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    u = mensagem()
    u.recebermensagem()

def thread3():
    class mensagem:
        def __init__(self, nome="", senha="", login="", email=""):
            self.nome = nome
            self.senha = senha
            self.email = email
            self.login = login

        def mensagemamigo(self):
            global envio
            msg = sep.join(info)
            s.sendall(str(envio))
            confirmacao2 = s.recv(1024)
            if confirmacao2 == 'ok':
                print('seu amigo ' + mensagem[1] + ' está online e sua mesagem foi encaminhada à ele.\n')

        def recebermensagem(self):
            i = 1
            global nome, senha, login, email, envio
            login = 0
            while i > 0:
                if login == 1:
                    l = []
                    l.append('recebequemestaonline')
                    l.append(nome)
                    l.append(senha)
                    sep = ';'
                    info = sep.join(l)
                    s.sendall(str(info))
                    confirmacao = s.recv(1024)
                    if confirmacao == 'ok':
                        while 1 < 10 :
                            try:
                                dados = s.recv(1024)
                                mensagem = []
                                mensagem[:] = dados.split(';')
                                if mensagem[0] == 'contatoonline':
                                    j = 0
                                    bancodedados = open("mensagensoffline.txt", 'r')
                                    bancodedados3 = open('mensagensoffline2.txt', 'w')
                                    bancodedados3.close()
                                    for linha in bancodedados:
                                        linha = linha.strip("\n")
                                        emailusuario, identificador, emailamigo, msg = linha.split(';')
                                        print 'procutando por email do amigo'
                                        if mensagem[1] == emailamigo and email == emailusuario:
                                            print 'achei email do amigo'
                                            j = j + 1
                                            info = []
                                            info.append(identificador)  # identificador de mensagem offline
                                            info.append(emailamigo)  # emailamigo
                                            info.append(msg)          # mensagem
                                            sep = ';'
                                            envio = sep.join(info)
                                            u.mensagemamigo()
                                        else:
                                            bancodedados2 = open("mensagensoffline2.txt", 'a')
                                            info = []
                                            info.append(identificador)
                                            info.append(emailamigo)  # emailcontato
                                            info.append(msg)  # mensagem
                                            sep = ';'
                                            envio = sep.join(info)
                                            bancodedados2.write(envio)
                                            bancodedados2.write('\n')
                                            bancodedados2.close()
                                    bancodedados.close()
                                    if j != 0:
                                        try:
                                            os.remove('mensagensoffline.txt')
                                            os.rename('mensagensoffline2.txt', 'mensagensoffline.txt')
                                        except Exception:
                                            print('nao atualizou o txt')
                                    if j == 0:
                                        os.remove('mensagensoffline2.txt')
                                if not dados: break
                            except Exception:
                                print('erro enviar mensagem off')
                        if i == 9:
                            i = 0
                        i = i + 1
                    if not confirmacao: break
                i = i + 1

    global envio
    HOST =
    PORT = 50999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    u = mensagem()
    u.recebermensagem()


def thread2():
    class mensagem:
        def __init__(self, nome="", senha="", login="", email=""):
            self.nome = nome
            self.senha = senha
            self.email = email
            self.login = login

        def recebermensagem(self):
            i = 1
            global nome, senha, login, email
            login = 0
            while i > 0:
                if login == 1:
                    l = []
                    l.append('recebemensagem')
                    l.append(nome)
                    l.append(senha)
                    sep = ';'
                    info = sep.join(l)
                    s.sendall(str(info))
                    confirmacao = s.recv(1024)
                    if confirmacao == 'ok':
                        while True:
                            try:
                                dados = s.recv(1024)
                                mensagem = []
                                mensagem[:] = dados.split(';')
                                if mensagem[0] == 'mensagemamigo':
                                    print (mensagem[1] + ' disse: ' + mensagem[2] + '\n')
                                if mensagem[0] == 'mensagemgrupo':
                                    print('No grupo' + mensagem[1] + ', ' + mensagem[2] + ' disse: ' + mensagem[3])
                            except Exception:
                                print('erro')
                else:
                    i = i + 1
    HOST = '127.0.0.1'
    PORT = 50999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    u = mensagem()
    u.recebermensagem()

def thread1():
    class usuario:
        def __init__(self, nome="", senha="", email=""):
            self.nome = nome
            self.senha = senha
            self.email = email


        def fazercadastro(self):
            global nome, senha
            u.nome = raw_input("Digite o nome do usuario.\n")
            u.senha = raw_input("Digite a senha.\n")
            u.email = raw_input("Digite o e-mail.\n")
            nome = u.nome
            senha = u.senha
            dados = []
            dados.append('cadastro')
            dados.append(u.nome)
            dados.append(u.senha)
            dados.append(u.email)
            sep = ';'
            msg = sep.join(dados)
            s.sendall(str(msg))
            try:
                confirmacao = s.recv(1024)
                if confirmacao == 'erro':
                    raise
                if confirmacao == 'ok':
                    print ("Cadastro finalizado")
                    print ("Agora voce ja pode falar com seus amigos.\n")
                    print ('Primeiro faça seu login.\n')
                    u.fazerlogin()
                if confirmacao == 'emuso':
                    try:
                        print ("E-mail ja está em uso.\n")
                        print ("Digite:\n")
                        print ("1 para tentar se cadastrar novamente.\n")
                        print ("2 para entrar na sua conta.\n")
                        decisao = raw_input("\n")
                        if (int(decisao) != 1) and (int(decisao) != 2):
                            raise
                        if int(decisao) == 1:
                            u.fazercadastro()
                        if int(decisao) == 2:
                            u.fazerlogin()
                    except Exception:
                        print ('opcao inválida, você voltou para o menu principal.\n')
                        u.menu1()
            except Exception :
                print('erro')
        def fazerlogin(self):
            global nome, senha, login, email
            u.nome = raw_input("Digite seu nome.\n")
            u.senha = raw_input("Digite sua senha.\n")
            nome = u.nome
            senha = u.senha
            dados = []
            dados.append('fazerlogin')
            dados.append(u.nome)
            dados.append(u.senha)
            sep = ';'
            dados2 = sep.join(dados)
            s.sendall(str(dados2))
            confirmacao = s.recv(1024)
            if confirmacao == 'emuso':
                print('Conta já está online em outro computador.\n')
                print ("Você voltou para o menu principal.\n")
                u.menu1()
            if confirmacao == 'naoexiste':
                try:
                    print ("Nome ou senha errados.\n")
                    print ("Digite:\n")
                    print ("1 para tentar logar na sua conta de novo.\n")
                    print ("2 para voltar ao menu principal.\n")
                    decisao = raw_input("\n")
                    if (int(decisao) != 1) and (int(decisao) != 2):
                        raise
                    if int(decisao) == 1:
                        u.fazerlogin()
                    if int(decisao) == 2:
                        u.menu1()
                except Exception:
                    print ("opcao invalida, voce voltou para o menu principal.\n")
                    u.menu1()
            else:
                retorno = []
                retorno[:] = confirmacao.split(';')
                if retorno[0] == 'ok':
                    email = retorno[1]
                    login = 1
                    print('Você está logado.\n')
                    u.menu2()

        def criargrupo(self):
            nomegrupo = raw_input("Digite o nome do grupo que deseja criar.\n")
            i = 0
            l = []
            l.append('criargrupo')
            l.append(nomegrupo)
            print ("Atencao! Você só pode adicionar amigos que estão na sua agenda de contatos.\n")
            n = raw_input("Digite o numero de amigos que deseja adicionar ao grupo.\n")
            while i < int(n):
                emailamigo = raw_input("Digite o email de um amigo que deseja adicionar.\n")
                l.append(emailamigo)
                i = i + 1
            sep = ';'
            dados = sep.join(l)
            s.send(str(dados))
            confirmacao = s.recv(1024)
            if confirmacao == 'ok':
                print ('Grupo criado com sucesso')
                u.menu2()
            if confirmacao == 'grupojaexiste':
                print('Já existe um grupo com esse nome, tente novamente')
                u.criargrupo()
            if confirmacao == 'erro':
                try:
                    print ('Você tentou adicionar alguem que não está na sua agenda.\n')
                    print ("Digite 1 para tentar de novo.\n")
                    print ("Digite 2 para adicionar um contato a sua agenda.\n")
                    print('Digite 3 para voltar ao menu principal.\n')
                    decisao = raw_input("\n")
                    if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3):
                        raise
                    if int(decisao) == 1:
                        u.criargrupo()
                    if int(decisao) == 2:
                        u.adicionarcontato()
                    if int(decisao) == 3:
                        u.menu2()
                except Exception:
                    print ("opcao invalida, você voltou ao menu principal.\n")
                    u.menu2()

        def menuaddaogrupo2(self):
            try:
                print ('Você nao possui esse email na sua agenda de contatos.\n')
                print ("Digite 1 para tentar de novo.\n")
                print ("Digite 2 para adicionar um contato a sua agenda.\n")
                print('Digite 3 para voltar ao menu principal.\n')
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3):
                    raise
                if int(decisao) == 1:
                    u.addaogrupo()
                if int(decisao) == 2:
                    u.adicionarcontato()
                if int(decisao) == 3:
                    u.menu2()
            except Exception:
                print ("opcao invalida, tente novamente.\n")
                u.menuexcluirgrupo()

        def menuaddaogrupo(self):
            try:
                print ('Esse usuario já está no grupo.\n')
                print ("Digite 1 para tentar de novo.\n")
                print ("Digite 2 para voltar ao menu principal.\n")
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2):
                    raise
                if int(decisao) == 1:
                    u.addaogrupo()
                if int(decisao) == 2:
                    u.menu2()
            except Exception:
                print ("opcao invalida, tente novamente.\n")
                u.menuaddaogrupo()

        def menuaddaogrupo3(self):
            try:
                print('Não existe ninguém com esse email cadastrado.')
                print ("Digite 1 para tentar de novo.\n")
                print ("Digite 2 para voltar ao menu principal.\n")
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2):
                    raise
                if int(decisao) == 1:
                    u.addaogrupo()
                if int(decisao) == 2:
                    u.menu2()
            except Exception:
                print ("opcao invalida, tente novamente.\n")
                u.menuaddaogrupo3()

        def addaogrupo(self):
            try:
                cont = raw_input('Qual o email do amigo que deseja adiconar?\n')
                grupo = raw_input('Para qual grupo deseja adiciona-lo?\n')
                identificador = 'addaogrupo'
                l = []
                l.append(identificador)
                l.append(grupo)
                l.append(cont)
                sep = ';'
                info = sep.join(l)
                s.sendall(str(info))
                confirmacao = s.recv(1024)
                if confirmacao == 'jaesta':
                    u.menuaddaogrupo()
                if confirmacao == 'ok':
                    print ('Seu amigo foi adicionado com sucesso.\n')
                    u.menu2()
                if confirmacao == 'naoagenda':
                    u.menuaddaogrupo2()
                if confirmacao == 'naocadastrado':
                    u.menuaddaogrupo3()
                if confirmacao == 'naoestanogrupo':
                    print('Você não está no grupo.\n')
                    print('Você voltou ao menu principal.\n')
                    u.menu2()
            except Exception:
                print ('erro')

        def menuexcluirgrupo(self):
            try:
                print ('Você não criou o grupo, logo você não pode excluir-lo.\n')
                print ("Digite 1 para tentar de novo.\n")
                print ("Digite 2 para voltar ao menu principal.\n")
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2):
                    raise
                if int(decisao) == 1:
                    u.excluirgrupo()
                if int(decisao) == 2:
                    u.menu2()
            except Exception:
                print ("opcao invalida, tente novamente.\n")
                u.menuexcluirgrupo()

        def excluirgrupo(self):
            print ('ATENÇÂO, VOCÊ SÒ PODE EXCLUIR UM GRUPO QUE VOCE CRIOU!!\n')
            info = raw_input('Qual grupo você deseja excluir?\n')
            identificador = 'excluirgrupo'
            l = []
            l.append(identificador)
            l.append(info)
            sep = ';'
            data = sep.join(l)
            s.sendall(str(data))
            confirmacao = s.recv(1024)
            if confirmacao == 'naocriou':
                u.menuexcluirgrupo()
            else:
                print ('Grupo excluido com sucesso.\n')
                u.menu2()

        def adicionarcontato(self):
            add = raw_input("Qual o email adicionar a agenda?\n")
            identificador = 'adicionarcontato'
            l = []
            l.append(identificador)
            l.append(add)
            sep = ';'
            info = sep.join(l)
            s.sendall(info)
            confirmacao = s.recv(1024)
            if confirmacao == 'ok':
                print ("Contato adicionado com sucesso.\n")
                try:
                    print ("Digite 1 para adicionar outro contato.\n")
                    print ("Digite outra coisa para voltar ao menu principal.\n")
                    decisao = raw_input("\n")
                    if int(decisao) != 1:
                        raise
                    if int(decisao) == 1:
                        u.adicionarcontato()
                except Exception:
                    u.menu2()
            if confirmacao == 'naocadastrada':
                try:
                    print ("Nao existe essa pessoa cadastrada no programa.\n")
                    print ("Digite 1 para fazer tentar novamente.\n")
                    print ("Digite outra coisa para voltar ao menu principal.\n")
                    decisao2 = raw_input("\n")
                    if int(decisao2) != 1:
                        raise
                    if int(decisao2) == 1:
                        u.adicionarcontato()
                except Exception:
                    u.menu2()
            if confirmacao == 'jaadicionada':
                try:
                    print ('Essa pessoa já está na sua agenda.\n')
                    print ("Digite 1 para adicionar outra pessoa.\n")
                    print ("Digite outra coisa para voltar ao menu principal.\n")
                    decisao2 = raw_input("\n")
                    if int(decisao2) != 1:
                        raise
                    if int(decisao2) == 1:
                        u.adicionarcontato()
                except Exception:
                    u.menu2()

        def mensagemamigo(self):
            emailamigo = raw_input("Digite o email do amigo que quer mandar uma mensagem.\n")
            mensagem = raw_input("Digite sua mensagem\n")
            identificador = 'mensagemamigo'
            info = []
            info.append(identificador)
            info.append(emailamigo)
            info.append(mensagem)
            sep = ';'
            msg = sep.join(info)
            s.sendall(str(msg))
            confirmacao = s.recv(1024)
            if confirmacao == 'naoagenda':
                try:
                    print ('Você não possui esse email na sua agenda.\n')
                    print ("Digite 1 tentar novamente.\n")
                    print ('Digite 2 para adicionar esse email a sua agenda.\n')
                    print ("Digite outra coisa para voltar ao menu principal.\n")
                    decisao2 = raw_input("\n")
                    if int(decisao2) != 1 and int(decisao2) != 2:
                        raise
                    if int(decisao2) == 1:
                        u.mensagemamigo()
                    if int(decisao2) == 2:
                        u.adicionarcontato()
                except Exception:
                    print ('opcao inválita, você voltou ao menu principal.\n')
                    u.menu2()
            if confirmacao == 'ok':
                print ('Mensagem enviada.\n')
                u.menu2()
            if confirmacao == 'naocadastrado':
                print('Não existe ninguém com esse email cadastrado no sistema.\n')
                u.menu2()
            else :
                retorno = []
                retorno[:] = confirmacao.split(';')
                if retorno[0] == 'amigooffline':
                    print ('Amigo offline, quando vocês dois estiverem online a mensagem será encaminha à ele.\n')
                    bancodedados = open('mensagensoffline.txt', 'a')
                    identificador = 'mensagemamigo'
                    info2 = []
                    info2.append(email)
                    info2.append(identificador)
                    info2.append(emailamigo)
                    info2.append(mensagem)
                    sep = ';'
                    msg2 = sep.join(info2)
                    bancodedados.write(msg2)
                    bancodedados.write('\n')
                    bancodedados.close()

        def mensagemgrupo(self):
            grupo = raw_input("Para qual grupo deseja mandar mensagem?\n")
            identificador = 'mensagemgrupo'
            mensagem = raw_input("Digite sua mensagem\n")
            l = []
            l.append(identificador)
            l.append(grupo)
            l.append(mensagem)
            sep = ';'
            info = sep.join(l)
            print  info
            s.sendall(str(info))
            confirmacao = s.recv(1024)
            if confirmacao == 'naoestanogrupo':
                try:
                    print ('Você não está no grupo.\n')
                    print ("Digite 1 para fazer tentar novamente.\n")
                    print ("Digite 2 para criar um grupo novo.\n")
                    print ("Digite outro valor para voltar ao menu principal.\n")
                    decisao2 = raw_input("\n")
                    if (int(decisao2) != 1) and (int(decisao2) != 2):
                        raise
                    if int(decisao2) == 1:
                        u.mensagemgrupo()
                    if int(decisao2) == 2:
                        u.criargrupo()
                except Exception:
                    u.menu2()
            if confirmacao == 'ok':
                print('Mensagem enviada.\n')
                u.menu2()
            if confirmacao == 'naoexiste':
                try:
                    print('Esse grupo não existe.\n')
                    print ("Digite 1 para fazer tentar novamente.\n")
                    print ("Digite 2 para criar um grupo novo.\n")
                    print ("Digite outro valor para voltar ao menu principal.\n")
                    decisao2 = raw_input("\n")
                    if (int(decisao2) != 1) and (int(decisao2) != 2):
                        raise
                    if int(decisao2) == 1:
                        u.mensagemgrupo()
                    if int(decisao2) == 2:
                        u.criargrupo()
                except Exception:
                    u.menu2()
            else :
                retorno = []
                retorno[:] = confirmacao.split(';')
                if retorno[0] == 'naotodosonline':
                    print ('Nem todos do grupo estão online., quando estiverem sua mensagem irá ser enviada.\n')
                    bancodedados = open('mensagensoffline.txt', 'a')
                    identificador = 'mensagemamigo'
                    info2 = []
                    info2.append(email)
                    info2.append(identificador)
                    info2.append(grupo)
                    info2.append(mensagem)
                    sep = ';'
                    msg2 = sep.join(info2)
                    bancodedados.write(msg2)
                    bancodedados.write('\n')
                    bancodedados.close()

        def excluirconta(self):
            global login
            try:
                print ('Tem certeza que deseja excluir sua conta?')
                print ("Digite sim sair.\n")
                print ("Digite não para voltar ao menu principal.\n")
                decisao2 = raw_input("\n")
                if str(decisao2) != 'sim' and str(decisao2) != 'não':
                    raise
                if str(decisao2) == 'sim':
                    identificador = 'excluirconta'
                    email = raw_input('Digite seu email para excluir sua conta.\n')
                    senha = raw_input('Digite sua senha para excluir sua conta.\n')
                    l = []
                    l.append(identificador)
                    l.append(email)
                    l.append(senha)
                    sep = ';'
                    info = sep.join(l)
                    s.sendall(str(info))
                    confirmacao = s.recv(1024)
                    if confirmacao == 'ok':
                        login = 0
                        print ('Você excluiu sua conta.\n')
                        u.menu1()
                if str(decisao2) == 'senhaerrada':
                    print ('Senha errada, tente novamente.\n')
                    u.excluirconta()
            except Exception:
                print ('Opção inválida, tente novamente.\n')
                u.excluirconta()

        def sair(self):
            global login
            try:
                print ('Tem certeza que deseja sair da sua conta?\n')
                print ("Digite sim sair.\n")
                print ("Digite não para voltar ao menu principal.\n")
                decisao2 = raw_input("\n")
                if str(decisao2) != 'sim' and str(decisao2) != 'não':
                    raise
                if str(decisao2) == 'sim':
                    identificador = 'sair'
                    s.sendall(str(identificador))
                    confirmacao = s.recv(1024)
                    if confirmacao == 'ok':
                        login = 0
                        print ('Você saiu da sua conta.\n')
                        u.menu1()
                if str(decisao2) == 'não':
                    print ('nao saiu da conta.\n')
                    u.menu2()
            except Exception:
                print('erro')
                u.menu2()

        def menu1(self):
            try:
                print ("Digite:\n")
                print ("1 para fazer login.\n")
                print ("2 para se cadastrar.\n")
                print ('3 para fechar a conexão.\n')
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3):
                    raise
                if int(decisao) == 1:
                    u.fazerlogin()
                if int(decisao) == 2:
                    u.fazercadastro()
                if int(decisao) == 3:
                    s.sendall('fecharsocket')
                    s.close()
                    print('Você fechou a conexão.\n')
            except Exception:
                print ("opcao invalida, tente novamente.\n")
                u.menu1()

        def adicionarvarioscontatos(self):
            s.sendall('adicionarcontatos')
            confirmacao = s.recv(1024)
            if confirmacao == 'ok':
                t = raw_input('Digite a quantidade de contatos.\n')
                cont = 1
                l = []
                while cont < int(t) + 1:
                    contato = raw_input('Digite o email do ' + str(cont) + ' contato.\n')
                    l.append(contato)
                    cont = cont + 1
                sep = ';'
                info = sep.join(l)
                bancodedados = open('adicionarcontatos.txt', 'w')
                bancodedados.close()
                bancodedados2 = open('adicionarcontatos.txt', 'a')
                bancodedados2.write(info)
                bancodedados2.write('\n')
                try:
                    f = open("adicionarcontatos.txt", "rb")
                    l = f.read(1024)
                    while (l):
                        s.send(l)
                        l = f.read(1024)
                except Exception:
                    print 'erro ao enviar lista de contatos para adicionar à agenda.\n'
                print 'Todos esses contatos agora estão na sua agenda.\n'
                u.menu2()

        def sairdegrupo(self):
            decisao = raw_input('Sair de qual grupo?\n')
            identificador = 'sairgrupo'
            info = []
            info.append(identificador)
            info.append(decisao)
            sep = ';'
            info2 = sep.join(info)
            s.sendall(str(info2))
            print info2
            try:
                confirmacao = s.recv(1024)
                if confirmacao == 'saiudogrupo':
                    print ('Você saiu da sua conta, a conexão foi fechada.\n')
                if confirmacao == 'naosaiudogrupo':
                    print ('Voce nao faz parte do grupo.\n')
                    u.menu2()
            except Exception:
                print('erro')
                u.menu2()

        def menu2(self):
            try:
                print ("Digite:\n")
                print ("1 para adicionar um contato.\n")
                print ("2 para conversar com um amigo.\n")
                print ("3 para criar um grupo.\n")
                print ("4 para conversar com um grupo.\n")
                print ('5 para adicionar um contato à um grupo.\n')
                print ('6 para excluir um grupo que você criou.\n')
                print ("7 para sair da sua conta.\n")
                print ("8 para mandar um arquivo para um amigo.\n")
                print ("9 para mandar um arquivo para um grupo.\n")
                print ("10 para excluir sua conta.\n")
                print ('11 para adiconar vários contatos à sua agenda.\n')
                print('12 para sair do grupo.\n')
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3) and (int(decisao) != 4) and (
                    int(decisao) != 5) and (int(decisao) != 6) and (int(decisao) != 7) and (int(decisao) != 8) and (
                    int(decisao) != 9) and (int(decisao) != 10) and (int(decisao) != 11) and (int(decisao) != 12):
                    raise
                if int(decisao) == 1:
                    u.adicionarcontato()
                if int(decisao) == 2:
                    u.mensagemamigo()
                if int(decisao) == 3:
                    u.criargrupo()
                if int(decisao) == 4:
                    u.mensagemgrupo()
                if int(decisao) == 5:
                    u.addaogrupo()
                if int(decisao) == 6:
                    u.excluirgrupo()
                if int(decisao) == 7:
                    u.sair()
                if int(decisao) == 8:
                    pass
                if int(decisao) == 9:
                    pass
                if int(decisao) == 10:
                    u.excluirconta()
                if int(decisao) == 11:
                    u.adicionarvarioscontatos()
                if int(decisao) == 12:
                    u.sairdegrupo()
            except Exception:
                print ("opcao invalida, tente novamente")
                u.menu2()
    HOST = '127.0.0.1'
    PORT = 50999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))
    u = usuario()
    u.menu1()


if __name__ == '__main__':
    global nome, senha, login, email
    a = open("mensagensoffline.txt", 'a')
    a.close()
    a = open("adicionarcontatos.txt", 'a')
    a.close()
    a = open("mensagensofflinegrupo.txt", 'a')
    a.close()
    t1 = Thread(target=thread1, args=())
    t1.start()
    t2 = Thread(target=thread2, args=())
    t2.start()
    t3 = Thread(target=thread3, args=())
    t3.start()
    t4 = Thread(target=thread4, args=())
    t4.start()

