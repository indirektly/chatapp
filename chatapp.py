import socket 
import select 
import sys


def main():
    #Even though this is the client portion, it is essentially a server of sorts
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    #Tests to see if the arguements containing the IP and port are there
    if len(sys.argv) != 3: 
        print("Need args (in order): IP address, port number")
        exit() 
    
    #Sets the arguements to the IP and port and then binds them to the socket/server
    IP_address = str(sys.argv[1]) 
    Port = int(sys.argv[2]) 
    server.connect((IP_address, Port))


    while True: 
  
        # maintains a list of possible input streams 
        sockets_list = [sys.stdin, server] 
    
        #From stackoverflow piece that I don't remember
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

        #Checks all sockets for messages
        for socks in read_sockets: 
            if socks == server: 
                message = socks.recv(2048) 
                print(message) 
            else: 
                message = sys.stdin.readline() 
                server.send(str.encode(message))
                sys.stdout.write("You: ") 
                sys.stdout.write(message) 
                sys.stdout.flush() 
    
    server.close()

if(__name__ == '__main__'):
    main()