from PTAT import PTATServidor
import os
import sys
from datetime import datetime
from time import ctime, strftime



serverSocket = PTATServidor.cria_servidor()

while True:
    valor, connectionSocket = PTATServidor.conexao_aceita(serverSocket)
    print("COMANDO ENVIADO COM SUCESSO!")
    comandos = valor.split("+")

    OP = comandos[0]
    LENGTH = comandos[1]
    PATH = comandos[2]
    FILENAME = comandos[3]
    if OP == 1:
        BODY = comandos[4]

    print(comandos)
    if len(FILENAME.encode('utf-8')) > 32:
        connectionSocket.send(f"{FILENAME} Nome do arquivo maior do que o permitido")
    if len(PATH.encode('utf-8')) > 128:
        connectionSocket.send(f"{PATH} Caminho do arquivo maior do que o permitido")
    if len(LENGTH.encode('utf-8')) > 4:
        connectionSocket.send(f"{LENGTH} Tamanho maior do que o permitido")

    if(OP == '0' or OP == '2'):
        #print(comandos[0])
        if os.path.exists(PATH):
            destino = os.path.join(PATH, FILENAME)
           #print(PATH)
            if os.path.exists(destino):
                #print(destino)
                #print(len(LENGTH.encode('utf-8')))
                #print(int(LENGTH))
                LENGTH = str(os.path.getsize(destino))
                if len(LENGTH.encode('utf-8')) <= int(LENGTH):
                    if(OP == '0'):
                        #print("read")
                        destino = os.path.join(PATH, FILENAME)
                        arquivo = open(destino, "r")
                        linhas = arquivo.readlines()
                        arquivo.close()
                        BODY = "".join(linhas)
                        #print(len(BODY.encode()))
                        if int(LENGTH) == len(BODY.encode()):
                            #print("SUCESSO")
                            CODE = 'CODE=100'
                            connectionSocket.send((f"{OP} {LENGTH} {FILENAME} {PATH} CODE=100\n Arquivo lido com sucesso {BODY}").encode())
                    if(OP == '2'):
                        #print("del")
                        destino = os.path.join(PATH, FILENAME)
                        arquivo = open(destino, "r")
                        linhas = arquivo.readlines()
                        arquivo.close()
                        BODY = "".join(linhas)
                        #print(len(BODY.encode()))
                        if int(LENGTH) == len(BODY.encode()):
                            #print("SUCESSO")
                            os.remove(destino)
                            CODE = 'CODE=100'
                            connectionSocket.send((f"{OP} {LENGTH} {FILENAME} {PATH} CODE=100\n Arquivo deletado com sucesso {BODY}").encode())
                else:
                    CODE = 'CODE=98'
                    connectionSocket.send(f'{OP} {LENGTH} {FILENAME} {PATH} CODE=98\nTamanho do arquivo para ser escrito maior que tamanho máximo permitido'.encode())
            else:
                CODE = 'CODE=97'
                connectionSocket.send(f'{OP} {LENGTH} {FILENAME} {PATH} CODE=97\nNome de arquivo nao existente no servidor!'.encode())
        else:
            CODE = 'CODE=96'
            connectionSocket.send('CODE=96\nCaminho nao existente no servidor!'.encode())

    elif (OP == '1'):
        #print(OP)
        BODY = comandos[4]
        #print(BODY)
        if int(LENGTH) >= len(BODY.encode('utf-8')):
            if os.path.exists(PATH):
                destino = os.path.join(PATH, FILENAME)
                arquivo = open(destino, "w")
                arquivo.write(BODY)
                arquivo.close()
                CODE = 'CODE=100'
                connectionSocket.send((f"{OP} {LENGTH} {FILENAME} {PATH} CODE=100\nArquivo escrito com sucesso {BODY}").encode())
            else:
                CODE = 'CODE=96'
                connectionSocket.send('CODE=96\nCaminho nao existente no servidor!'.encode())
        else:
            CODE = 'CODE=98'
            connectionSocket.send(f'{OP} {LENGTH} {FILENAME} {PATH} CODE=98\ntamanho do arquivo para ser escrito maior que tamanho máximo permitido'.encode())

    elif (OP == '3'):
        CODE = 'CODE=99'
        connectionSocket.send(f'{OP} {LENGTH} {FILENAME} {PATH} CODE=99\nOperação inválida!'.encode())
    else:
        print('Não entrei em nenhum lugar')
    
    HORA = datetime.now()

    HORA = HORA.strftime("%H:%M:%S")
    LOG = str(HORA)+','+OP+','+PATH+','+CODE
    print(LOG)