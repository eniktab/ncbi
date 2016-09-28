# -*- coding: utf-8 -*-
"""Parsing and downloading taxon data for BLAST result out put format 6"""
try:
   from urllib.error import HTTPError
except ImportError:
   from urllib2 import HTTPError
from socket import error as SocketError
import urllib.request as IncompleteRead
import numpy as np
import time
import xml.etree.cElementTree as ETree
from Bio import Entrez 
import random 
Entrez.email = "mane360@yahoo.com" # Always tell NCBI who you are
start_time = time.time()
""" Function downloading file from Efetch """
def myfunct(inputnumber):
        id_list = inputnumber # feed the ID here 
        print (id_list)
        handle = Entrez.efetch(db="nucleotide", id=id_list, rettype="gb", retmode="xml") # or retmode="text"
        #print(handle.read())                                                            #try to save the xml file 
         
        """Find/sort/print the tags, content, and attributes of the hits """
        
        
        tree = ETree.parse(handle )
        root = tree.getroot()
        organism          = root.getiterator('GBSeq_organism')
        definition        = root.getiterator('GBSeq_definition')
        primaryaccession  = root.getiterator('GBSeq_primary-accession')
        taxonomy          = root.getiterator('GBSeq_taxonomy')
        while True:
            try:
                org    = next(organism).text
                defi   = next(definition).text
                priacc = next(primaryaccession).text
                taxon  = next(taxonomy).text
                print (priacc,",",org,",",defi,",",taxon,",", "T")
                output.write(inputnumber+'\t'+priacc+'\t'+org+'\t'+defi+'\t'+taxon+"\n")
                break
            except:
                output.write(str(id_list)+" error-happenned\n")            
                #print ("error happened")
                break
 
def sendemail():
    import smtplib

    TO = 'mane360@yahoo.com'
    SUBJECT = 'Report of ERROR'
    TEXT = 'Here is a message from python. Your Programm is fucked'
    
    # Gmail Sign In
    gmail_sender = 'eliatan.err.ntf@gmail.com'
    gmail_passwd = '123456789abcde'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    
    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')
    
    server.quit()  
    
   # for element in tree.getiterator():
   #     tags.add(element.tag)
    #counts = {}   
   # for element in tree.getiterator():
    #    counts[element.tag] = 1 + counts.get(element.tag, 0)
    #sortedtags = sorted(counts.items(), key=lambda item: item[1],reverse=True)
    #print(sortedtags)
    
    #for element in tree.getiterator():
     #       print(element.tag, ":::>", element.text)
          
            


"""Read The input file """ 

  
t=np.loadtxt("/home/chemgen/Desktop/Over Again/SSU-97per-BLASTout.csv",dtype=str,delimiter='|',skiprows=0,usecols=(1,))
output=open("/home/chemgen/Desktop/Over Again/Endo18-97per-PYTHONout.csv", "a")
counter = 0
for line in t:
    counter +=1    
    print (line)
    print ("counter:",counter)
    print("Running time:","--- %s Seconds" % (time.time() - start_time))    
    line=line[2:-1]    
    line=line.strip()
    try: 
        myfunct(line)
        timetosleep= random.randrange(2,6)
        time.sleep(timetosleep) 
    except HTTPError as err:
        print("Received error from server %s"% err)
        time.sleep(60)
        myfunct(line)
    except SocketError as err:
        print("Received error from server %s"% err)
        time.sleep(60)
        myfunct(line)
        sendemail()
    except IncompleteRead as err:      
        print("Received error from server %s"% err)
        time.sleep(60)
        myfunct(line)
output.close()

                             
    
   


