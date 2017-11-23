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
        dados.append('fazerlogin')
        dados.append(u.nome)
        dados.append(u.senha)
        sep = ';'
        dados2 = sep.join(dados[1:3])
        s.sendall(str(dados2))
        confirmacao = s.recv(1024)
        if confirmacao == 'emuso':
            print('Conta já está online em outro computador.\n')
            print ("Você voltou para o menu principal.\n")
            u.menu1()
        if confirmacao == 'naoexiste' :
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
        if confirmacao == 'semmsg' :
            print('Você está logado.\n')
            print('Você não recebeu mensagens enquanto esteve offline.\n')
            u.menu2()
        else :
            mensagem = []
            mensagem[:] = confirmacao.split(';')
            print ('Enquanto você esteve offline,\n')
            print(mensagem[1]' disse 'mensagem[2]'\n')                                 ###################nao sei o que ta errado

    def criargrupoprincipal(nomegrupo):
        l = []
        l.append(nomegrupo)
        print ("Atencao! Você só pode adicionar amigos que estão na sua agenda de contatos.\n")
        n = raw_input("Digite o numero de amigos que deseja adicionar ao grupo.\n")
        while i < n:
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
        if confirmacao == 'erro':
            print('Já existe um grupo com esse nome, tente novamente')
            u.criargrupo()

    def criargrupo(self):
        nomegrupo = raw_input("Digite o nome do grupo que deseja criar.\n")
        u.criargrupoprincipal(nomegrupo)

    def menuaddaogrupo2(self):
        try:
            print ('Você nao possui esse email na sua agenda de contatos.\n')
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
         except Exception :
            print ("opcao invalida, tente novamente.\n")
            u.menuaddaogrupo()

    def addaogrupo(self):
        try:
            cont = raw_input('Qual o email do amigo que deseja adiconar?')
            grupo = raw_input('Para qual grupo desefa adiciona-lo?')
            identificador = 'addaogrupo'
            l = []
            l.append(identificador)
            l.append(cont)
            l.append(grupo)
            sep = ';'
            info = sep.join(l)
            s.sendall(str(info))
            confirmacao = s.recv(1024)
            if confirmacao == 'jaesta':
                u.menuaddaogrupo()
            if confirmacao == 'ok':
                print ('Seu amigo foi adicionado com sucesso.\n')
            if confirmacao == 'naoagenda':
                u.menuaddaogrupo2()
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
        print ('ATENÇÂO, VOCÊ SÒ PODE EXCLUIR UM GRUPO QUE VOCE CRIOU!!')
        info = raw_input('Qual grupo você deseja excluir?')
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
        emailamigo = raw_input("Digite o email do amigo que quer mandar uma mensagem.\n")
        mensagem = raw_input("Digite sua mensagem\n")
        identificador = 'mensagemamigo'
        l = []
        l.append(identificador)
        l.append(emailamigo)
        l.append(mensagem)
        sep = ';'
        info = sep.join(l)
        s.sendall(str(info))
        confirmacao = s.recv(1024)
        if confirmacao == 'naoagenda':
            try:
                print ('Você não possui esse email na sua agenda.\n')
                print ("Digite 1 tentar novamente.\n")
                print ('Digite 2 para adicionar esse email a sua agenda.\n')
                print ("Digite outra coisa para voltar ao menu principal.\n")
                decisao2 = raw_input("\n")
                if int(decisao2) != 1 and int(decisao2) != 2 :
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
        if confirmacao == 'amigooffline':
            print ('Amigo offline, quando ele entrar ele reseberá sua mensagem.\n')
            u.menu2()


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
        if confirmacao == 'ok' :
            print ('Todos os membros do grupo que estão online receberam e quem está offline irá ver quando entrar na conta.\n')
            u.menu2()

    def sair(self):
        try:
            print ('Tem certeza que deseja sair da sua conta?')
            print ("Digite sim sair.\n")
            print ("Digite não para voltar ao menu principal.\n")
            decisao2 = raw_input("\n")
            if (int(decisao2) != 'sim') and (int(decisao2) != 'não'):
                raise
            if int(decisao2) == 'sim':
                identificador = 'sair'
                s.sendall(str(identificador))
                confirmacao = s.recv(1024)
                if confirmacao == 'ok'
                    print ('Você saiu da sua conta.\n')
                    u.menu1()
            if int(decisao2) == 'não':
                u.menu2()
        except Exception:
            u.menu2()
def fecharsocket(self):                                        ############isso ta errado???
    s.close()


def menu1(self):
    try:
        print ("Digite:\n")
        print ("1 para fazer login.\n")
        print ("2 para se cadastrar.\n")
        print ('3 para fecha a conexão.\n')
        decisao = raw_input("\n")
        if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3):
            raise
        if int(decisao) == 1:
            u.fazerlogin()
        if int(decisao) == 2:
            u.fazercadastro()
        if int(decisao) == 3:
            fecharsocket()
    except Exception:
        print ("opcao invalida, tente novamente.\n")
        u.menu1()

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
        decisao = raw_input("\n")
        if (int(decisao) != 1) and (int(decisao) != 2) and (int(decisao) != 3) and (input(decisao) != 4) and (input(decisao) != 5) and (input(decisao) != 6) and (input(decisao) != 7):
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
            u.excluirgrupo()
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
