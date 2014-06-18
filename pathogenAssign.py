import sys
import csv

#Barcode -> Sample
SampletoBarcode = {}

i=0
j=0
with open(sys.argv[1], 'rb') as csvfile:
    LookUpReader = csv.reader(csvfile, delimiter='\t') 
    for row in LookUpReader:
        if i == 0:
            SampleIndex = row.index('SampleID')
            BarcodeIndex = row.index('BarcodeID')
            YearIndex = row.index('HarvestYear') 
            i = 1
        else:
            sample = "_".join(row[SampleIndex].split())
            barcode = row[BarcodeIndex]
            year = row[YearIndex]
            if sample == "Neg":
                sample = sample+str(j)
                SampletoBarcode[barcode] = [sample, year]
                j+=1
            else:
                sample = sample
                SampletoBarcode[barcode] = [sample, year]

#Sample -> meta 
SampletoMeta = {}

i = 0
with open(sys.argv[2], 'rb') as csvfile:
    LookUpReader = csv.reader(csvfile, delimiter=',')
    for row in LookUpReader:
        if i == 0:
            SampleIndex = row.index('Sample')
            NameIndex = row.index('Name')
            CladeIndex = row.index('Clade')
            SpeciesIndex = row.index('Species')
            PositionIndex = row.index('Pos')
            i = 1
        else:
            sample = row[SampleIndex]
            name = row[NameIndex]
            clade = row[CladeIndex]
            species = row[SpeciesIndex]
            position = row[PositionIndex]
            SampletoMeta[sample] = [name, clade, species, position]

#Sample -> Plot
SampletoPlot = {}

with open(sys.argv[3], 'r') as locfile:
    LookUpReader = csv.reader(locfile, delimiter=',')
    for row in LookUpReader:
        SampletoPlot[row[2]] = row[0]

#Name, Sample, Clade, Species, Year, Pos, Plot, Pathogen, Bootstrap
#HWI-M01380:52:000000000-A64W5:1:1101:15884:15565:Foxtrot258    k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Hypocreales;f__Nectriaceae;g__Fusarium;s__Fusarium_circinatum  0.770

with open(sys.argv[4], 'r') as rdpfile:
    print "Name, Sample, Clade, Species, Year, Position, Plot, Pathogen, BootstrapVal"
    for line in rdpfile:
        line = line.split('\t')
        barcode = line[0].split(":")[7]
        bootvalue = line[len(line) - 1].strip("\n")
        pathogen = " ".join(line[len(line) - 2].split(";")[6].strip("s__").split("_"))
        sample = SampletoBarcode[barcode][0]
        year = SampletoBarcode[barcode][1] 
        try:
            plot = SampletoPlot[sample]
        except KeyError:
            plot = ""
        try:
            testSample = sample[0]+"2"+sample[2]+sample[3]
            try: 
                metaList = SampletoMeta[testSample]
                name = metaList[0]
                clade = metaList[1]
                species = metaList[2]
                position = metaList[3]
                print "%s,%s,%s,%s,%s,%s,%s,%s,%s" %(name, sample, clade, species, year, position, plot, pathogen, bootvalue)
            except KeyError:
                print ",%s,,,,,,%s,%s" %(sample, pathogen,bootvalue)
        except IndexError:
            print ",%s,,,,,,%s,%s" %(sample, pathogen,bootvalue)

