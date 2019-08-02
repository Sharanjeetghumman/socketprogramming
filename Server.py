import socket, threading

def accept_client():
    while True:
        #accept
        cli_sock, cli_add = ser_sock.accept()
        uname = cli_sock.recv(1000)
        CONNECTION_LIST.append((uname, cli_sock))
        print('%s is now connected' %uname.decode("utf-8"))
        data="{userjoinedchat}"
        b_usr(cli_sock, uname, data.encode('utf-8'))
        thread_client2 = threading.Thread(target = broadcast_usr, args=[uname, cli_sock])
        thread_client2.start()

def broadcast_usr(uname, cli_sock):
    while True:
        try:
            data = cli_sock.recv(1000)
            if data:
                print ("{0} spoke".format(uname.decode("utf-8")))
                b_usr(cli_sock, uname, data)
        except Exception as x:
            data="{userleftchat}"
            b_usr(cli_sock, uname, data.encode('utf-8'))
            CONNECTION_LIST.remove((uname, cli_sock))
            print(uname.decode("utf-8")+" has left the room")
            break

def b_usr(cs_sock, sen_name, msg):
    for client in CONNECTION_LIST:
        if client[1] != cs_sock:
            client[1].sendall(sen_name)
            client[1].sendall(msg)

def writelog(uname,msg):
    log=open("log.txt","a")
    log.write(uname+": "+msg+"\n")
    log.close()

def checkname(uname,cli_sock):
    while uname in CONNECTION_LIST:
        try:
            data = "True"
            cli_sock.sendall(data.encode('utf-8'))
            uname = cli_sock.recv(1000)
        except:
            break



if __name__ == "__main__":


    CONNECTION_LIST = []

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = '10.0.0.249'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen
    ser_sock.listen(1)
    print('Chat server started on ip address : ' + str(HOST))
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target = accept_client)
    thread_ac.start()

