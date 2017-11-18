# encoding: utf-8
# -*- coding: cp1252 -*-.
#!/usr/bin/python

import socket
from multiprocessing import Process
from threading import Thread


class Usuario:
    def __init__(self, nome="", senha="", email=""):
        self.nome = nome
        self.senha = senha
        self.email = email
    def fazercadastro(self):
        u.nome = raw_input("Digite o nome do usuario.\n")
        u.senha = raw_input("Digite a senha.\n")
        u.email = raw_input("Digite o e-mail.\n")
        dados = []
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
        except Exception:
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
            except Exception :
                print ('opcao inválida, você voltou para o menu principal.\n')
                u.menu1()
    def fazerlogin(self):
        u.nome = raw_input("Digite seu nome.\n")
        u.senha = raw_input("Digite sua senha.\n")
        dados = []
        dados.append(u.nome)
        dados.append(u.senha)
        sep = ';'
        dados2 = sep.join(dados[1:2])
        s.sendall(str(dados2))
        confirmacao = s.recv(1024)
        if confirmacao == 'ok':
            u.menu2()
        if confirmacao != 'ok':
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
    def criargrupo(self):
        nomegrupo = raw_input("Digite o nome do grupo que deseja criar.\n")
        u.criargrupoprincipal(nomegrupo)

    def criargrupoprincipal(nomegrupo):
        l = []
        l.append(nomegrupo)
        print ("Atencao! Você só pode adicionar amigos que estão na sua agenda de contatos.\n")
        n = raw_input("Digite o numero de amigos que deseja adicionar ao grupo.\n")
        while i < n:
            emailamigo = raw_input("Digite o email de um amigo que deseja adicionar.\n")
            l.append(emailamigo)
            i = i +1
        sep = ';'
        dados = sep.join(l)
        s.send(str(dados))
        confirmacao = s.recv(1024)
        if confirmacao == 'ok':
            print ('Grupo criado com sucesso')
        if confirmacao == 'erro' :
            print('Já existe um grupo com esse nome, tente novamente')
            u.criargrupo()

    def adicionarcontato(self):
        add = raw_input("Qual o email adicionar a sua lista de contatos?\n")
        s.sendall(add)
        confirmacao = s.recv(1024)
        if confirmacao == 'ok':
            print ("Contato adicionado com sucesso.\n")
            try:
                print ("Digite 1 para adicionar outro contato.\n")
                print ("Digite outra coisa para voltar ao menu principal.\n")
                decisao = raw_input("\n")
                if int(decisao) != 1:
                    raise
                if decisao == 1:
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
        if confirmacao == 'jaadcionada':
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
        cont = raw_input("Digite o email do amigo que quer mandar uma mensagem.\n")
        s.sendall(cont)
        confirmacao = s.recv(1024)
        if confirmacao == 1:
            msg = []
            msg.append('consulta')
            msg.append(cont)
            mensagem = raw_input("Digite sua mensagem\n")
            msg.append(mensagem)
            sep = ';'
            dados = sep.join(msg)
            s.send(str(dados))
        else:
            try:
                print ("Nao foi encontrado esse contato na sua agenda.\n")
                print ("Digite 1 para fazer tentar novamente")
                print ("Digite 2 para adicionar um contato na sua agenda\n")
                print ("Digite outro valor para voltar ao menu principal.\n")
                decisao = raw_input("\n")
                if (int(decisao) != 1) and (int(decisao) != 2):
                    raise
                if int(decisao) == 1:
                    u.mensagemamigo()
                if int(decisao) == 2:
                    u.adicionarcontato()
            except Exception:
                u.menu2()
    def mensagemgrupo(self):
        cont = raw_input("Para qual grupo deseja mandar mensagem?\n")
        s.sendall(cont)
        confirmacao = s.recv(1024)
        if confirmacao == 1:
            msg = raw_input("Digite sua mensagem para o grupo\n")  #como botar o nome do grupo dentro do print?
            s.sendall(msg)
            try:
                print ("Digite 1 para mandar outra mensagem para o grupo.\n")
                print ("Digite outro valor para voltar ao menu principal.\n")
                decisao = raw_input("\n")
                if int(decisao) != 1:
                    raise
                if int(decisao) == 1:
                    u.mensagemgrupo()
            except Exception:
                u.menu2()
        else:
            try:
                print ("Esse grupo nao existe.\n")
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

def menu1(self):
    try:
        print ("Digite:\n")
        print ("1 para fazer login.\n")
        print ("2 para se cadastrar.\n")
        decisao = raw_input("\n")
        if (int(decisao) != 1) and (int(decisao) != 2):
            raise
        if int(decisao) == 1:
            s.sendall("fazerlogin")
            u.fazerlogin()
        if int(decisao) == 2:
            s.sendall("cadastrar")
            u.fazercadastro()
    except Exception:
        print ("opcao invalida, tente novamente.\n")
        u.menu1()

def menu2(self):
    try:
        print ("Digite:\n")
        print ("1 para adicionar um contato\n")
        print ("2 para conversar com um amigo\n")
        print ("3 para criar um grupo de amigos\n")
        print ("4 para conversar com um grupo de amigos")
        decisao = raw_input("\n")
        if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3) and (input(decisao) != 4):
            raise
        if int(decisao) == 1:
            s.sendall("adicionarcontato")
            u.adicionarcontato()
        if int(decisao) == 2:
            s.sendall("mensagemamigo")
            u.mensagemamigo()
        if int(decisao) == 3:
            s.sendall("criargrupo")
            u.criargrupo()
        if int(decisao) == 4:
            s.sendall("mensagemgrupo")
            u.mensagemgrupo()
    except Exception:
        print ("opcao invalida, tente novamente")
        u.menu2()

if __name__ == '__main__':
    HOST = '127.0.0.1'  # The remote host
    PORT = 50999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))  #
    u.usuario()
    menu1()
