import socket
import os
import threading
import time

## Informações do servidor: Host e porta para conexao
Host = '127.0.0.1'
Port = 5050

## Criacao do socket TCP para comunicacao
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.bind((Host, Port))
socket_tcp.listen(5)

#################################################################
# Funcao para atender cada cliente que chega. A cada cliente,  ##
# uma nova thread é criada para executar esta funcao.          ##
#################################################################

lista = []

def atendeCliente(conexao, cliente):
    while True:
        #recebe a mensagem do cliente
        message = conexao.recv(1024)# Tamanho do buffer eh 1024 bytes
        result = message.decode()
        
        if result == "EXIT":
            mensagem = str("Cliente " + cliente + " desconectou")
            print(mensagem)
            break
        # recebe a mensagem e retorna para o cliente
        elif result:
            message = str(cliente) + ' ' + str(result)
            print(message, '\n')
            #devolver mensagem ao cliente
            conexao.send(message.encode())
    return

#########################
## Programa principal ###
#########################
print ('Bem vindo ao Chat 0.3!!')

while True:
    #recebe novas conexoes
    conn, client_host = socket_tcp.accept()
    #thread para tratar cada cliente que entra
    t1 = threading.Thread(target=atendeCliente, args=(conn, client_host,))
    t1.start()
    lista.append((conn, client_host))

    def broadcast(message, sender_conn):
        for client_conn, _ in lista:
            if client_conn != sender_conn:
                try:
                    client_conn.send(message.encode())
                except:
                    client_conn.close()
                    lista.remove((client_conn, _))

    def handle_client(conn, client_host):
        while True:
            try:
                message = conn.recv(1024).decode()
                if message:
                    if message == "EXIT":
                        print(f"Cliente {client_host} desconectou")
                        lista.remove((conn, client_host))
                        conn.close()
                        break
                    else:
                        print(f"{client_host}: {message}")
                        broadcast(f"{client_host}: {message}", conn)
            except:
                continue

    t1 = threading.Thread(target=handle_client, args=(conn, client_host))
    t1.start()