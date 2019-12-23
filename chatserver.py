import socket
import select
import sys
import _thread

def main():
    #Sets the server domain and socket type
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #Sets the socket options
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #This checks to see if the IP and the port were provided in the arguements
    if len(sys.argv) != 3: 
        print("Need args (in order): IP address, port number")
        exit()
    #Sets the arguements to IP and port, then binds them to the socket/server
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    server.bind((IP_address, Port))
    
    #Max number of connections allowed
    server.listen(100)
    #Used for keeping track of clients for certain reasons such as broadcasting
    list_of_clients = []
    clientNames = {}


    def clientthread(conn, addr): 
  
        # sends a message to the client whose user object is conn 
        conn.send(b"Welcome to this chatroom!")
        

        #This spoofs versions numbers for nmap
        #conn.send(b"HTTP/1.1 200 OK" +b'\r\n'+ b"Server: Netscape-Enterprise/6.1" +b'\r\n'+ b"Date: Fri, 19 Aug 2016 10:28:43 GMT" +b'\r\n'+ b"Content-Type: text/html; charset=UTF-8" +b'\r\n'+ b"Connection: close" +b'\r\n'+ b"Vary: Accept-Encoding" +b'\r\n'+ b"Content-Length: 32092" +b'\r\n\n\n')

    
        while True: 
                try: 
                    message = conn.recv(2048) 
                    if message: 
    
                        #Attempt at using custom name
                        if(message.split()[0] == '!setname'):
                            clientNames[addr[0]] = message.split()[1]
                            #For testing custom names
                            #print(str(clientNames))
                        else:
                            #Logs text from users
                            #Seems to not work...?
                            print(addr[0] + ": " + message)
                            #Creates message and sends to all connections 
                            message_to_send = clientNames[addr[0]] + ": " + message 
                            broadcast(message_to_send, conn) 
    
                    else: 
                        #remove connection if connection is broken
                        remove(conn) 
    
                except: 
                    continue
    
    #Considering the structure of a chatroom, every message is broadcasted to all connections
    def broadcast(message, connection): 
        for clients in list_of_clients: 
            if clients!=connection: 
                try: 
                    clients.send(message) 
                except: 
                    clients.close() 
    
                    #if the link is broken, remove client 
                    remove(clients)
    
    #Used for terminating broken connections
    def remove(connection): 
        if connection in list_of_clients: 
            list_of_clients.remove(connection)
    

    #Tis always true
    #Looks for active conncetions and accepts
    while True:
        conn, addr = server.accept() 

        list_of_clients.append(conn) 
    
        #prints the addr of user that connected 
        print(addr[0] + " connected")
        clientNames[addr[0]] = str(addr[0])
        #creates individual thread for every unique user  
        _thread.start_new_thread(clientthread,(conn,addr))     

    #if loop breaks my guy, close that stuff down
    conn.close() 
    server.close()

if(__name__ == '__main__'):
    main()