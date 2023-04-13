
import gzip

# path for input files
path = "C:/Users/admg200/Downloads/gencode.v19.annotation.gtf.gz"
cgiPath = "C:/Users/admg200/Desktop/teaching/PythonCourse2021/data/cpgIslandExt.txt.gz"


def parseGeneId1(s):
    return s.split("gene_id")[1].split('"')[1]

def parseTag(s,tag):
    return s.split(tag)[1].split('"')[1]


def processFile(path,outpath="genes.bed",typeCol=2):
    f = gzip.open(path,'rt') # open the file in text mode
    out = open(outpath,'w')
    #cnt = 0
    for line in f:
    
        # skip the comment
        if line[0] == '#':
            continue
        # split by column
        cols = line.split('\t') # spliting the line by tabulator

        # filter for genes (not transcripts or exons)
        if cols[typeCol] != 'gene':
            continue
        
        #print(str(line),str(line)[0])
        
        # Explicit parsing - Demo
        #print("GeneId: ",parseGeneId1(line))
    
        # Parsing by tag - Demo
        #for tag in ["gene_id","gene_name"]:
        #    print(tag,parseTag(line,tag))


        chrom = cols[0]
        start = cols[3]
        end = cols[4]
        strand = cols[6]
        name = "%s_%s"%(parseTag(line,"gene_name"),parseTag(line,"gene_id"))

        bed = "\t".join([chrom,start,end,name,"0",strand]) + "\n"

        out.write(bed) # writing the line into the output file

        #print(bed)
    
        #cnt += 1
        #if cnt == 3:
        #    break
    out.close()

processFile(path)

def convertToPromoter(fp,outFp="promoter.bed",upstream=500,downstream=100):
    f = open(fp,'r')
    out = open(outFp,'w')

    for line in f:
        (chrom,start,end,name,score,strand) = tuple( line.strip().split('\t') )
        promStart = 0
        promEnd = 0
        if strand == '+':
            promStart = str( int(start) - upstream )
            promEnd = str( int(start) + downstream )
        else:
            promStart = str( int(end) + upstream )
            promEnd = str( int(end) - downstream )
        out.write( '\t'.join((chrom,promStart,promEnd,name,score,strand)) + '\n' )

    f.close()
    out.close() # files are closed automatically if the all references are terminated, but clean code should close them if they are no longer required

#convertToPromoter("genes.bed")

def task2_1(fp):
    f = open(fp,'r')
    chroms = {}

    for line in f:
        cols = line.strip().split('\t')
        #print(cols)
        (chrom,start,end,name,score,strand) = tuple(cols[0:6])

        
        gene = (chrom,start,int(cols[2]),cols[3],cols[4],cols[5])
        if chrom in chroms: # test if this chromosome symbol is encountered the first time
            if start in chroms[chrom]:
                ls = chroms[chrom][start] # find the correct list for the start pos on the correct chromosome
                ls.append(gene) # append the gene to the list
            else:
                chroms[chrom][start] = [gene] # account for multiple identical start positions by using a list
        else:
            chroms[chrom] = {start : [gene]} # create a new dictionary if chromosome seen the first time

    return chroms

def task2_2(chrom,start,end,chroms):
    #check if chrom symbol is known, otherwise no overlap is possible
    if not chrom in chroms:
        return []

    starts = chroms[chrom]
    overlaps = []

    lsStart = starts.keys()

    for geneStart in lsStart:
        if start < int(geneStart) and end > int(geneStart):
            overlaps.extend(starts[geneStart])
            continue
        genes = starts[geneStart]
        for gene in genes:
            geneEnd = int(gene[2])
            if start < geneEnd and end > geneEnd:
                overlaps.append(gene)
    return overlaps

def task3_2(fpPromoter,fpCgi,outFpCgi,outFpPlain):
    chroms = task2_1(fpPromoter)
    outCgi = open(outFpCgi,'w') # output file for cgi promoter
    outPlain = open(outFpPlain,'w') # output file for plain promoters

    for line in gzip.open(fpCgi,'rt'): # the Promoter file is gziped
        cols = line.split('\t')
        
        # the cgi track is not bed format, but has an additional first column
        # therefore all indices are shifted by 1
        if task2_2(cols[1],int(cols[2]),int(cols[3]),chroms): 
            outCgi.write("\t".join(cols[1:])) # leave out the first column to create a true bed file, the last column still contains the linebreak
        else:
            outPlain.write("\t".join(cols[1:]))
        
#task3_2("promoter.bed",cgiPath,"cgi_promoter.bed","plain_promoter.bed")
    
