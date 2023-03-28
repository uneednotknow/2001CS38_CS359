#Khushi Prasad, 2001CS38
#for each type of packet, the query has to be individually pasted to the terminal

import socket
import scapy.all as scapy

#Start the given website 
#stores current ip of the website
# or use dns query 
host = socket.gethostbyname("booking.com")
#TCP open handshake
#applying filters
capture = sniff(iface = "Wi-fi", filter = "tcp and host", count = 3)
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_TCP_open_handshake", capture)
#########

#Close the given website
#stores current ip of the website
# or use dns query
host = socket.gethostbyname("booking.com")
#TCP closing handshake
#applying filters
capture = sniff(iface = "Wi-fi", filter = "tcp and host and tcp[tcpflags] & tcp-fin != 0", count = 4)
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_TCP_close_handshake", capture)
#########

#FTP connection start packets
#applying filters
#ftp uses port 20 and 21
#selecting both ports so as to capture sending of file as well
capture = sniff(iface="Wi-fi", filter = "port 20 or 21", count = 20)
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_FTP_connection_start", capture)
#########

#FTP connection close packets
#applying filters
#ftp uses port 20 and 21
capture = sniff(iface="Wi-fi", filter = "port 20 or 21", count = 20)
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_FTP_connection_end", capture)
#########

#DNS packets
#applying filters
//DNS protocol uses port53
capture = sniff(filter = "port 53")
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_DNS_query_response", capture)
#########

#Ping packets
#applying filters
capture = sniff(filter = "icmp")
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_Ping_query_response", capture)
#########

#ARP packets
#applying filters
capture = sniff(count = 5)
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_ARP_query_response", capture)
#########

#ARP_request_response packets
#Ping to any localhost
#In local host, we have DHCP packets instead of ARP packets
#applying filters
capture = sniff(count = 5)
#displaying results
capture.summary()
#storing it in a pcap file
wrpcap("2001CS38_ARP_query_response", capture)
#########
