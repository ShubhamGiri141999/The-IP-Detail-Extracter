import math                     
import sys
import socket                    #modules imported
import ctypes
import os
import win32process
import PySimpleGUI as sg

#---------------------------------------------------------------------

inpt_f = open("IP_list.txt", "r")           #opening the file having the IP list
out_f = open("IP_Detail_list.txt","a")      #opening the IP detail file

thisdict = {"IP":"","NetRange":"","CIDR":"","NetName":"","RegDate":"","Updated":"","City":"","StateProv":"","PostalCode":"","Country":""}   #creating the dictionary

out_f.write("IP Address"+"\t"+"Net Range"+"\t"+"CIDR"+"\t"+"Net Name"+"\t"+"Reg. Date"+"\t"+"Updated Date"+"\t"+"City"+"\t"+"StateProve"+"\t"+"PostalCode"+"\t"+"Country\n\n\n")

#---------------------------------------------------------------------
statinfo = os.stat('IP_list.txt')
sz = math.floor(statinfo.st_size/16 )         #calculating the number of IP addresses

current_value=0
#---------------------------------------------------------------------

for IP in inpt_f:                   #fetching IP addresses
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #connecting the socket to the server
    s.connect(("whois.arin.net", 43))

    current_value+=1
    sg.OneLineProgressMeter('CDAMS IP Decode', current_value,sz,'key')  #showing the progressbar
    
    str=""
    s.send((IP.strip() + "\r\n").encode())          #fetching IP details
    
    temp = open("temp.txt","a")                     #opening the buffer file in write mode

    response = b""
    while True:
        data = s.recv(4096)
        response += data
        if not data:
            break
    
    d=(response.decode())
    temp.write(IP+'\n'+d)
     
    temp.close()                                    #closing the buffer file
    temp = open("temp.txt","r")                     #opening buffer file in read mode

    
    
    for i, line in enumerate(temp):
          data=line.split(':',1)
          
          if data[0] in thisdict.keys():  
                    thisdict[data[0]]=data[1]       #storing data in the dictionary
                    
    temp.close()                                   #closing the buffer file
    
    
    thisdict["IP"] = IP.strip()

    for val in thisdict.values():                    
                 buffer_string=val
                 str+=(buffer_string.strip()+"\t")
                
    out_f.write(str)                                #writing data in the output file
    out_f.write("\n")
   
    os.remove("temp.txt")
    s.close()                                       #socket closed
    
#---------------------------------------------------------------------

inpt_f.close()                                      #input file closed
out_f.close()                                       #output file closed
