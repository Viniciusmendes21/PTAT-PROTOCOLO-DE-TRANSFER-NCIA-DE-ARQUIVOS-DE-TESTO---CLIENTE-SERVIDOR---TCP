import socket
import os


class PTATServidor():
    """PTAT Do Servidor"""
    def cria_servidor():
        """Cria o socket do servidor."""
        host = "127.0.0.1"
        porta = 12000
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind((host, porta))
        serverSocket.listen(1)
        print("Aguardando conexão. . .")
        return serverSocket

    def conexao_aceita(serverSocket):
        """Conexão é aceita."""
        connectionSocket, addr = serverSocket.accept()
        print("CONEXÃO ESTABELECIDA AGUARDANDO INSERÇÃO DE DADOS!")
        valor = str(connectionSocket.recv(1024).decode())
        return valor, connectionSocket


class PTATCliente():
    """PTAT Do Cliente"""
    def conexao_criada():
        """Cria o socket do cliente."""
        host = "127.0.0.1"
        porta = 12000
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((host,porta))
        return clientSocket

    def mensagem_enviada(clientSocket):
        """O cliente envia os dados para o servidor."""
        valor = input("Digite o comando, o diretorio e o nome: ")
        comandos = valor.split(" ")

        if len(comandos)<4:
            print('Número insuficiente de parametros')

        OP = comandos[0]
        LENGTH = comandos[1]
        PATH = comandos[2]
        FILENAME = comandos[3]

        if OP == "read":
           OP=0
           valor = f"{OP}+{LENGTH}+{PATH}+{FILENAME}"
        elif OP == 'write':
           BODY = comandos[4]
           OP=1
           valor = f"{OP}+{LENGTH}+{PATH}+{FILENAME}+{BODY}"
        elif OP == 'del':
           OP=2
           valor = f"{OP}+{LENGTH}+{PATH}+{FILENAME}"
        else:
           OP=3
           valor = f"{OP}+{LENGTH}+{PATH}+{FILENAME}"

        clientSocket.send(valor.encode())
        resultado = clientSocket.recv(1024)
        print("Servidor: " +  resultado.decode())
        clientSocket.close()

