#importing all the required modules
import socket 
import sys

#taking server ip and server port input from command line
Host = sys.argv[1]
port = int(sys.argv[2])

#making a  server socket instance
#first parameter indicates that underlying network is using IPv4
#second parameter indicates that the socket is a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    #connecting to the server
    server.bind((Host, port))
    print ("Socket binded to %s." %(port))

    #server is listening for TCP server requests from client
    server.listen(0)
    print ("Socket is listening.")
except socket.error as err1: 
    
    #if there's already a client connceted to the server, send an error message
    print ("Port is engaged right now: ",str(err1))
    exit(0)

#running an infinte loop
while 1:

    #server accepts the client's TCP socket connection request
    #client server then completes the handshake
    clientConnection, clientAddress = server.accept()
    print ("Connected to client: ",clientAddress)
    
    #initialising string
    msg = ''

    #running an infinite loop
    while 1:

        #receiving data from the client server
        data = clientConnection.recv(1024)
        
        #if nothing received, exit the loop
        if not data:
            break
        
        #decoding and printing the message received    
        msg = data.decode()
        print ("Client sent: ",msg)

         #initialising variable to store the result of the expression
        result = 0
        
        #split the string for further operations
        operation_list = msg.split()
        #if there are not three chars, send error message
        if len(operation_list) != 3:
            err2 = "Incorrect syntax."
            print ("Sending: ",err2)
            clientConnection.send(err2.encode())
            continue

        #storing operands and operation
        oprnd1 = operation_list[0]
        operation = operation_list[1]
        oprnd2 = operation_list[2]

        #converting the character to integer
        num1 = int(oprnd1)
        num2 = int(oprnd2)

        #performing operation
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            result = num1/num2
        else:
            err3 = "Invalid operator."
            print ("Sending: ",err3)
            clientConnection.send(err3.encode())
            continue
	
        print ("Sending: ",result)
        
        #converting the output to string and sending it to client
        output = str(result)
        clientConnection.send(output.encode())

    #closing the connection
    clientConnection.close()
    print ("Connection closed by client.")