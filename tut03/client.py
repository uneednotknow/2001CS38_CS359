#importing socket and sys module
import socket
import sys

#defining Main function
def Main():

        #taking server ip and server port input from command line
        serverIP = sys.argv[1]
        serverPort = int(sys.argv[2])

        #creating a testclient instance
        testclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #making a  client socket instance
        #first parameter indicates that underlying network is using IPv4
        #second parameter indicates that the socket is a TCP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
                #trying to connect to testclient
                testclient.connect((serverIP, serverPort))
                #closing the connection
                testclient.close()

                #connecting to the server
                clientSocket.connect((serverIP, serverPort))
                print ("Connected to server.")

        #if more than one clients try to connect to the server, throwing error
        except socket.error as err:
                print ("Can't connect to server right now: ",str(err))
                exit(0)

        #Running an infinite loop
        while 1:
        
                #getting user input
                sentence = input("Input :")
                
                #if user wants to quit
                if sentence == "N":
                        print ("Session Over.")
                        break
                
                #send the input to the server
                clientSocket.send(sentence.encode())
                
                #receive the message sent by the server
                answer = clientSocket.recv(1024)
                print ("Server replied: ",answer.decode())

                print ("Type the expression if you still want to continue. Type N to exit.")
                
        #closing the socket
        clientSocket.close()

if __name__ == '__main__':
        Main()