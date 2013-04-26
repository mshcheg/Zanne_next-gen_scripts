from __future__ import print_function
from Phred import Phred33

'''

Script to parse reads and calculate read quality for each barcode/primer.

Primers are parsed by looking for a primer sequence match in the read. This is
a very crude way to  identify the corresponding amplicon for a read. Read
quality is calculated as an average of base quality scores.

Comma seperated text is printed to standard out:

barcode,sample,read,quality,primer
Echo214,K6bZ,1,36,ITS
Echo214,K6bZ,2,36,ITS
Echo206,G6bZ,1,25,ITS
Echo206,G6bZ,2,26,ITS
Echo218,M6bZ,1,37,LSU
Echo218,M6bZ,2,37,LSU
Echo203,F6tZ,1,36,LSU
Echo203,F6tZ,2,35,LSU
Echo200,D6bZ,1,37,ITS
.
.
.

Some R code is included to visualize the output. 

'''

def main(FileR1, FileR2):
    
    #Define primer sequences
    ITS = ('CTTGGTCATTTAGAGGAAGTAA', 'TCCTCCGCTTATTGATATGC')
    LSU = ('ACCCGCTGAACTTAAGC', 'GTCTTGAAACACGGACC')
    SixTeenS = ('AGAGTTTGATCCTGGCTCAG', 'ATTACCGCGGCTGCTGGC')

    print('barcode', 'sample', 'read', 'quality', 'primer', sep=',')
    with open(FileR1, 'r') as Read1:
        with open(FileR2, 'r') as Read2:
            while 1: #initiate infinite loop
                #read 4 lines of the fasta file
                SequenceHeader1= Read1.readline()
                SequenceHeader2 = Read2.readline()
                if SequenceHeader2 == '': #exit loop when end of R2 file is reached
                    break
                barcode = SequenceHeader1.split('|')[1].strip('\n')
                sample = SampleBarcode[barcode]
                Sequence1 = Read1.readline()
                Sequence2 = Read2.readline()
                if any(substring in Sequence1 for substring in ITS):
                    primer = 'ITS'
                else:
                    if any(substring in Sequence1 for substring in LSU):
                        primer = 'LSU'
                    else:
                        if any(substring in Sequence1 for substring in SixTeenS):
                            primer = '16S'
                QualityHeader1 = Read1.readline()
                QualityHeader2 = Read2.readline()
                Quality1 = Read1.readline().strip('\n')
                Quality2 = Read2.readline().strip('\n')
                QualitySum1, QualitySum2 = 0, 0
                for Score in Quality1:
                    QualitySum1 = QualitySum1 + Phred33[Score]
                QualitySum1 = QualitySum1/len(Quality1)
                for Score in Quality2:
                    QualitySum2 = QualitySum2 + Phred33[Score]
                QualitySum2 = QualitySum2/len(Quality2)
                print(barcode, sample, '1',  QualitySum1, primer, sep=',')
                print(barcode, sample, '2',  QualitySum2, primer, sep=',')

SampleBarcode = {}

#Match sample to barcode from targets.txt file.
with open('targets.txt','r') as infile:
    line = infile.readline()
    for line in infile:
        line = line.split()
        if line[0] in SampleBarcode.items():
            break
        else:
            SampleBarcode[line[0]]=line[3]

main('Amy-Zanne_R1.fastq','Amy-Zanne_R4.fastq')
