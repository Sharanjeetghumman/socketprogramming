import socket, threading, sys, time,tkinter


def on_my_msg_click(event):
    """function that gets called whenever my_msg is clicked"""
    if my_msg.get() == 'Enter your message...':
       my_msg.delete(0, "end") # delete all the text in the my_msg
       my_msg.insert(0, '') #Insert blank for user input
       my_msg.config(fg = 'black')
def on_focusout(event):
    if my_msg.get() == '':
        my_msg.insert(0, 'Enter your message...')
        my_msg.config(fg = 'grey')

#Allows user to send a message to the server
def sendmessage():
    message=my_msg.get()
    message=name+message
    if message=="{quit}":
        sys.exit()
    msg_list.insert(tkinter.END, message)
    packet.sendall(message.encode('utf-8'))

#Allows the user to recieve messages from the server
def receivemessage():
    while True:
        try:
            name = packet.recv(1000)
            data = packet.recv(1000)
            if data.decode("utf-8")=="{userjoinedchat}":
                msg=name.decode("utf-8")+" has joined the chat room."
                print("\n"+msg)
                msg_list.insert(tkinter.END, msg)
            elif data.decode("utf-8")=="{userleftchat}":
                msg=name.decode("utf-8") + " has left the chat room."
                print("\n"+msg)
                msg_list.insert(tkinter.END, msg)
            else:
                msg=str(name.decode("utf-8")) + ': ' + str(data.decode("utf-8"))
                print("\n"+msg)
                msg_list.insert(tkinter.END, msg)
        except:
            break
            msg="Server has disconnected please try again later"
            print(msg)
            msg_list.insert(tkinter.END, msg)
            time.sleep(5000)
            sys.exit()


#Main function that creates the socket and connects them and starts the two threads to send and recieve messages concurrently
if __name__ == "__main__":

    top = tkinter.Tk()
    top.title("Chatter")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()
    my_msg.set('')
    my_msg.bind('<FocusIn>', on_my_msg_click)
    my_msg.bind('<FocusOut>', on_focusout)
    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    my_msg_field = tkinter.my_msg(top, textvariable=my_msg)
    my_msg_field.bind("<Return>", sendmessage)
    my_msg_field.pack()
    send_button = tkinter.Button(top, text="Send", command=sendmessage)
    send_button.pack()

 #   msg_list.insert(tkinter.END, "Please Enter a Username.")

    # socket creation
    packet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST =sys.argv[1]
    #Ip addr of server
    PORT =int(sys.argv[2])
    #PORT = 5023
    packet.connect((HOST, PORT))

    username = sys.argv[3]


    thread_send = threading.Thread(target = sendmessage)
    thread_send.start()

    thread_receive = threading.Thread(target = receivemessage)
    thread_receive.start()
    tkinter.mainloop()