import threading
import socket

def recieve(socket):
    while True:
        try:
            message = socket.recv(1024).decode("ascii")
            print(message)
        except:
            print("An error occured!")
            socket.close()
            quit()

def write(chat_id, socket):
    while True:
        message = "{}: {}".format(chat_id, input(""))
        socket.send(message.encode("ascii"))

class Chat:
    def __init__(self, port, chat_id):
        self.port = port
        self.chatId = chat_id
        self.socket = socket.socket()


    def create_chat(self):
        self.socket.bind(("", self.port))
        self.socket.listen()
        host_name = socket.gethostname()
        s_ip = socket.gethostbyname(host_name)
        print("This is your IP: ", s_ip)
        client, address = self.socket.accept()
        print("Connected with {}".format(str(address)))
        nickname = client.recv(1024).decode("ascii")
        print("Nickname is {}".format(nickname))
        client.send(self.chatId.encode("ascii"))
        receive_thread = threading.Thread(target=recieve, args=(client,))
        receive_thread.start()
        write_thread = threading.Thread(target=write, args=(self.chatId, client,))
        write_thread.start()

    def use_chat(self):
        ip = input("Informe o endereço IP do chat: ")
        self.socket.connect((ip, self.port))
        self.socket.send(self.chatId.encode("ascii"))
        print("Connected with {}".format(ip))
        nickname = self.socket.recv(1024).decode("ascii")
        print("Nickname is {}".format(nickname))
        receive_thread = threading.Thread(target=recieve, args=(self.socket,))
        receive_thread.start()
        write_thread = threading.Thread(target=write, args=(self.chatId, self.socket))
        write_thread.start()

def main():
    port = int(input("Insira a porta: "))
    chat_id = input("Escolha um nome: ")
    chat = Chat(port, chat_id)
    print("Escolha uma opção: ")
    aux = input("1 - Começar novo chat\n2 - Entrar em chat\n")
    if aux == "1":
        chat.create_chat()
    elif aux == "2":
        chat.use_chat()


if __name__ == '__main__':
    main()
