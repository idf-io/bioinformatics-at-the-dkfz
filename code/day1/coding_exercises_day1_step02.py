# Script takes the "gencode.v19.annotation.gtf" gencode formatted file and generates a .bed formatted file
#
# Gencode format (tab-separated, 1-based coorfinate system):
#   1. Chromosome name
#   2. Annotation source
#   3. Feature type
#   4. Genomic start location
#   5. Genomic stop location
#   6. Score
#   7. Strand (+/-)
#   8. Genomic phase
#   9. Additional information as key-value pairs
#
# BED format (tab/space-separated, 0-based coordinate system):
#   1. Chromosome
#   2. Genomic start location
#   3. Genomic stop location
#   ---
#   4. Name of the line
#   5. Score
#   6. Strand

import os


# Open files to read and write
file = open("../../data/gencode.v19.annotation.gtf", "rt")

os.system("mkdir -p ../../output/day1")
out = open("../../output/day1/gencode.v19.annotation_promoters.bed", "w")

# Metadata
out.write("## Description: Gencode human annotated genome v19 transformed to .bed format\n##date: 2023-04-12\n")

# GTF -> BED, filter and transform for promoters
for line in file:

    # Remove metadata lines
    if line.startswith("##"):
        continue

    # Read line
    list_gtf = line.split("\t")

    # Format new line, extract chrom, feature type, start, stop, strand
    mylist = [list_gtf[i] for i in [0,2,3,4,6]]

    # Transform gene to promoter positions
    if mylist[4] == "+":

        mylist[2] = int(mylist[2])
        mylist[2] = mylist[2] - 500 - 1 # -1 because we switch from a 0-based to a 1-based coordinate notation
        mylist[3] = mylist[2] + 100

    elif mylist[4] == "-":
        
        mylist[3] = int(mylist[3])
        mylist[2] = mylist[3] - 100 - 1
        mylist[3] = mylist[3] + 500

    # Filter for genes
    if mylist[1] != "gene":
        continue
    del mylist[1]

    # Add line name based on "additional information" field in the gtf file. Format="HugoGeneSymbol_EmsemblID"
    attributes = list_gtf[8].split(";")

    id = attributes[0].split(" ")[1][1:-1]
    name = attributes[4].split(" ")[2][1:-1]

    mylist.insert(3, 0)
    mylist.insert(3, name + "_" + id)
    
    # Write line
    line_out = list(map(lambda x: str(x), mylist))
    line_out = "\t".join(line_out) + "\n"
    out.write(line_out)

out.close()
file.close()
