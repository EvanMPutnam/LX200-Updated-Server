import socket
#Here we would import pyserial

HOST = 'localhost'
PORT = 5000

COMMAND_SET = {
    '#left': ['Left slew started.', "SOME_FUNCTION_POINTER"],
}

def createSerialConnection():
    return []

def serverHandler(serialConnection):
    s = socket.socket()
    s.settimeout(5)
    s.bind((HOST, PORT))
    s.listen(1)

    client, addr = s.accept()
    print("Connection from: "+str(addr))

    while True:
        data = client.recv(1024).decode('utf-8')
        if data:
            print("Command: "+data)
            if data in COMMAND_SET:
                print(COMMAND_SET[data][0])
                client.send(COMMAND_SET[data][0].encode('utf-8'))
            else:
                print("Invalid command above")
                client.send("Error: Invalid command\n".encode('utf-8'))


def main():
    print("Starting connection")
    serialConnection = createSerialConnection()
    while True:
        try:
            serverHandler(serialConnection)
        except socket.error as e:
            print(e)
            print("Server is now open for connection again")



if __name__ == '__main__':
    main()
