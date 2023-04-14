# Importing the required models
import queue  
import threading  
import time 
from os.path import exists 

#Definng an object class for Router
class Router: 

    INF = 1e18  

    #Initialising router object
    def __init__(R, router_id):  
        R.id = router_id  # Assigning the router ID
        # Creating an empty set to store the changes done in the routing table
        R.changes = set()
        # Creating an empty dictionary to store the neighbours and edge costs -> dict[Router, int]
        R.neighbours_list = {}
        # Creating an empty list to store the routing table entries -> list[list[Router, Router, int]]
        R.routing_table = []
        # Creating a queue object to store the incoming routing tables.
        R.queue = queue.Queue()

    # Adding a neighbour to the router
    def add_neighbours(R, neighbour, edge_cost):

        #Checking if the neighbor node is actually self and exiting
        if R == neighbour:  

            print("Loop is not allowed.")  
            exit(0) 
        #Else, adding the neighbour and edge cost to the neighbours dictionary
        R.neighbours_list[neighbour] = edge_cost

    # Initializing the routing table of the router
    def initialise_routing_table(R, routers):

        #For all router instances, do:
        for router in routers:  

            # Check if the router is in the neighbour list of the current router
            if R.neighbours_list.get(router):

                # If yes, add the entry
                # Using the edge dist from the neighbour list
                R.routing_table.append([router, router, R.neighbours_list.get(router)])
            elif router == R:  

                # Add a routing table entry
                # Using distance 0, as self 
                R.routing_table.append([router, router, 0])
            else:

                # Add a routing table entry for all other routers in the network
                # Because not approachable, using distance Inf.
                R.routing_table.append([router, None, R.INF])

    # Method to print the routing table of a router
    def print_routing_table(R, lock):
        # Acquire the lock before executing so as to prevent simultaneous read-write
        lock.acquire()

        print("Printing the router table from router: ", R.id)
        print("Dest. Router  | Cost       | Via Router  |")

        # Iterate through each element of the routing table
        for element in R.routing_table:

            # Extract the destination router ID 
            dest_router = element[0].id

            # If the destination router is in the set of recently changed routers, do
            if element[0].id in R.changes:
                R.changes.remove(element[0].id)
            
            # Print the routing table entry, with proper spacing and alignment
            print(f" {dest_router:<13} "
                + f" {element[2] if element[2] != R.INF else 'INF' :<16} "
                + f" {(element[1].id if element[1] else '--'):<15} ")

        print("\n")
        # Release the lock
        lock.release()

    def forward_routing_table(R):

        # For each neighbor in the router's list of neighbors
        for neighbour in R.neighbours_list.keys():

            # Add this router's instance to the neighbor's message queue
            neighbour.queue.put(R)

    def update_routing_table(R):
        # Set a flag to false indicating that no changes have been made to the routing table
        is_there_a_change = False

        # Loop forever until a break statement is reached
        while True:
            try:
                # Get the next item in the router's message queue
                neighbour = R.queue.get(block=False)

                # Determine the cost to the neighbor and its routing table
                cost_to_neighbour = R.neighbours[neighbour]
                routing_table_of_neighbour = neighbour.routing_table

                # Loop through the router's routing table and update entries as necessary
                for index, entry in enumerate(R.routing_table):
                    # New cost is the cost to the neighbour (say X) plus the cost from X to any other router (say Y)
                    new_cost = cost_to_neighbour + \
                        routing_table_of_neighbour[index][2]
                    # If new cost is less than the cost from the current router to Y, use B-F equation
                    if new_cost < entry[2]:
                        is_there_a_change = True
                        R.changes.add(entry[0].id)
                        R.routing_table[index] = [
                            entry[0], neighbour, new_cost]
            except:
                # If the router's message queue is empty, break out of the loop
                break

        # Return the flag indicating whether a change was made to the routing table
        return is_there_a_change


def parse_input():
    number_of_routers = 0               # Initialize the number of routers to zero
    routers = []                        # Create an empty list for routers
    # Create an empty dictionary for mapping router IDs to their index in the routers list
    routers_map = {}

    with open('topology.txt') as f:        # Open the file for reading

        # Read the first file
        # Converting the string to an integer
        number_of_routers = int(f.readline().strip())
        #Printing the number of routers
        print ("Number of routers connected are: ",number_of_routers)

        #Reading the second file 
        #Printing the mapping
        print("The mapping is: ")
        for index, router_id in enumerate(f.readline().strip().split(" ")):
            
            # Create a Router object for each router ID and add it to the routers list
            routers.append(Router(router_id))

            # Add the router ID and its index in a map
            routers_map[router_id] = index

            #Print the mapping
            print(router_id, ",", index)
        print("\n")

        for line in f.readlines():       
            
            # Iterate through the remaining files of the file
            # Remove any white space from the file
            line = line.strip()

            # If the current edge reads, EOF, do
            if line == "EOF": 
                break;                      

            # Split the file for further operations
            line = line.split(" ")

            # Getting the index of the first node 
            first_node = routers_map[line[0]]
            # Getting the index of the second node 
            second_node = routers_map[line[1]]
            # Converting the third string to an integer
            dist = int(line[2])

            # Adding the routers as each other's neighbours
            routers[first_node].add_neighbours(routers[second_node], dist)
            routers[second_node].add_neighbours(routers[first_node], dist)

    # Returning the number of routers and the routers list as a tuple
    return number_of_routers, routers


# Initializing the routing table for each router object
def initialise_routers(routers):

    # For all router instances in routers, do
    for r in routers:
        r.initialise_routing_table(routers)


# Printing the routing table for all routers
def print_tables(routers, lock):

    print("## New iteration. ##")
    # For all routers, do
    for router in routers:
        router.print_routing_table(lock)
    print("\n")


# Defining all the function a thread needs to perform to facilitate information exchange
def thread_function(router, lock, routers):

    # Setting the waiting time between each iteration to 2 seconds
    waiting_time = 2

    # Setting the flag to True indicating that a change is initially present in the routing table
    is_there_a_change = True

    # Setting the flag to True indicating that the function can continue
    can_continue = True

    # Continue the simulation while the flag can_continue is True
    while can_continue:

        # If there is a change in the routing table, forward the routing table
        if is_there_a_change:
            router.forward_routing_table()

        # Update the routing table and check if there is a change
        is_there_a_change = router.update_routing_table()

        # If there is a change in the routing table, print the routing table
        if is_there_a_change:
            router.print_routing_table(lock)

        # Wait for the specified time before the next iteration
        time.sleep(waiting_time)

        # Set the flag can_continue to False
        can_continue = False

        # Check if any router has any incoming routing table in its queue, if so, set the can_continue flag to True
        for each_router in routers:
            can_continue |= not each_router.queue.empty()


def Main():

    # Creating a threading lock
    #for proper resource allocation
    lock = threading.Lock()

    # Calling function to read input from file
    number_of_routers, routers = parse_input()

    # Calling function to initialise each router's routing table
    initialise_routers(routers)

    # Printing the initial routing table for all routers
    print_tables(routers, lock)

    # Create a list threads
    #holds all the threads
    threads = []

    # For all routers, do
    for router in routers:

        # Creating a new thread for each router and passing suuitable arguments
        thread = threading.Thread(target=thread_function, args=(router, lock, routers))
        # Start the function
        thread.start()
        # Adding the newly formed thread to the list
        threads.append(thread)

    # For all threads
    for thread in threads:

        # Wait for each thread to finish executing
        thread.join()

    # Again calling the function to print the final routing table for all routers
    print_tables(routers, lock)


if __name__ == "__main__":
    Main()

