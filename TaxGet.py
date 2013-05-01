''' 

Extract a subset of the nt database for a certain taxon using its ncbi taxonomy id.

For example to extract all fungal sequences from nt run:

python TaxGet.py 4751 

To extract sequences for a list of taonomy id's use:

numbers=(id1 id2 id3 ...); for i in "${numbers[@]}"; do python TaxGet.py $i; done &

'''

import hat_trie
import sys
import gzip
import urllib
from subprocess import call 
from Bio import Entrez 
import datetime

#get the taxonomy ids
Entrez.email = "youremail@email.com"
if not Entrez.email:
    print "you must add your email address"
    sys.exit(2)

taxid = sys.argv[1]
#change retmax if yo uexpect more than 92000 hits
handle = Entrez.esearch(db="taxonomy",term="txid%s[Subtree]" %taxid,retmax=92000)
record = Entrez.read(handle)
                         
TaxIDs = frozenset(record["IdList"])

#if not present download the latest nt database
DBFile = "nt.gz"
try: 
    with gzip.open(DBFile): pass
except IOError: 
    url1 = "ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz"
    call(['wget',url1])

#if not present download ID to gi mapping 
IDtoGI = "gi_taxid_nucl.dmp.gz"
try: 
    with gzip.open(IDtoGI): pass
except IOError:
    url2 = "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/gi_taxid_nucl.dmp.gz"
    call(['wget',url2])

#create a trie object associating gi's to taxid's
print "\nAssiciating Gi's and Taxonomy id's in memory. This may take a while."
with gzip.open(IDtoGI, 'rb') as inFile:
    IdGi = hat_trie.Trie()
    i = 0
    for line in inFile:
        i+=1
        line = line.split()
        IdGi[line[0].decode('unicode-escape')]= int(line[1].strip('\n'))

#loop over nucleotide database and extract all entries for your taxa
now = datetime.datetime.now()
DBOut = "%s_%s-%s-%s.fasta" %(taxid, now.month, now.day, now.year)
print '\nBuilding sequnece database for Taxonomy id %s. The database will be save in %s.' %(taxid, DBOut)

with open(DBOut, 'w') as outfile:
    with gzip.open(DBFile, 'rb') as InFile:
        line = True
        Test = 0
        while line:
            line = InFile.readline()
            if '>gi' in line:
                header = line
                gi = header.split('|')[1]
                try:
                    ID = IdGi[gi.decode('unicode-escape')]
                    if str(ID) in TaxIDs:
                        outfile.write(header)
                        Test = 1
                    else:
                        Test = 0
                        continue
                except KeyError:
                    continue 
            else:
                if Test == 1:
                    outfile.write(line) 
                else:
                    continue

