import select
import socket
import sys
import queue

#making a  client socket instance
#first parameter indicates that underlying network is using IPv4
#second parameter indicates that the socket is a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

#taking server ip and server port input from command line
Host = sys.argv[1]
port = int(sys.argv[2])

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

#List of sockets from which we expect to receive data
inputs = [ server ]

#List of sockets to which we are expected to send data
outputs = [ ]

#queue containing outgoing messages
message_queue = {}

request_address = {}

def math(msg):
                               
        #split the string for further operations
        operation_list = msg.split()
        	
        #if there are not three chars, send error message
        if len(operation_list) != 3:
                err2 = "Incorrect syntax."
                #print ("Sending : ",err2)
                return err2 
	
 
        #storing operands and operation
        oprnd1 = operation_list[0]
        operation = operation_list[1]
        oprnd2 = operation_list[2]
        
        if (operation not in ['+', '*', '-', '/']):
                err3 = "Invalid operator."
                #print ("Sending :",err3)
                return err3
                                
        #converting the character to integer
        num1 = int(oprnd1)
        num2 = int(oprnd2)
        
        #initialising variable to store the result of the expression
        result = 0

        #performing operation
        if operation == "+":
                result = num1 + num2
        elif operation == "-":
                result = num1 - num2
        elif operation == "*":
                result = num1 * num2
        elif operation == "/":
                result = num1/num2
                
        return result                              

#######

#Iterating over all the servers in the input queue
while inputs:

	#initialising and declaring variables
        read, write, err = select.select(inputs, outputs, inputs)

	#For all readable client sockets, perform:
        for s in read:
		
		#if a socket in read ready to connect
                if s is server:

                        #server accepts the readable client's TCP socket connection request
                        #client server then completes the handshake
                        clientConnection, clientAddress = server.accept()
                        print ("Connected to client: ",clientAddress)
                        
                        #storing address with ip as key
                        request_address[clientConnection] = clientAddress
                        
                        #setting the connection to be a non blocking command
                        clientConnection.setblocking(0)
                        
                        #adding the new connection to input queue
                        inputs.append(clientConnection)

		        #allocating a queue to store all the data to send
                        message_queue[clientConnection] = queue.Queue()
              
                else:
               	#receiving data from the client server
                       data = s.recv(1024)
        
        		#if nothing received
                       if not data:
                		
                               address = request_address[s]
                               s.close()
                               print ("Connection closed with server by client: ", address)
                		
                               if s in outputs:
                                       outputs.remove(s)
                			
                               inputs.remove(s)
                               del request_address[s]
                               del message_queue[s]
           
                       #if data received
                       else:
                               #initialising string
                               msg = ''
                               
                		#decoding and printing the message received    
                               msg = data.decode()
                               
                               print ("Message received from client: ", request_address[s])
                               print ("Client sent: ",msg)
                               result = math(msg)
        
        			#converting the output to string and sending it to client
                               output = str(result)
                               message_queue[s].put(output)
                               if s not in outputs:
                                       outputs.append(s)
        				
	#for all writeable client sockets, do:
        for s in write:
	         #getting message from the message queue
                try:
                        next_in_queue = message_queue[s].get_nowait()
			
		 #if the queue is empty:
                except queue.Empty:
			
			#remove the server from output queue
                       outputs.remove(s)
                else:
                       s.send(next_in_queue.encode())
                       print ("Sending: ",result)
                       print ("Result sent to client", request_address[s])	
			
	#for any socket with any error, do:
        for s in err:
		
                address = request_address[s]
                s.close()
                print ("Connection closed with server by client: ", address)
                inputs.remove(s)
                if s in outputs:
                        outputs.remove(s)
                del request_address[s]
                del message_queue[s]
                		
	
        		