import os

# Open files to read and write
file = open("../../data/gencode.v19.annotation.gtf", "rt")

os.system("mkdir -p ../../output/day1")
os.system("touch ../../gencode.v19.annotation_promoters.bed")
out = open("../../output/day1/gencode.v19.annotation_promoters.bed", "w")

# Metadata
out.write("##description: Gencode human annotated genome v19 transformed to .bed format\n##date: 2023-04-12\n")

# GTF -> BED, filter and transform for promoters
for line in file:

    # Remove metadata lines
    if line.startswith("##"):
        continue

    # Read line
    list_gtf = line.split("\t")

    # Format new line
    mylist = [list_gtf[i] for i in [0,2,3,4,6]]

    # Transform gene to promoter positions
    mylist[3] = int(mylist[3]) + 100

    mylist[2] = int(mylist[2])
    mylist[2] = int(mylist[2]) - 500 - 1 # -1 because we switch from a 0-based to a 1-based coordinate notation


    # Filter for genes
    if mylist[1] != "gene":
        continue
    del mylist[1]

    attributes = list_gtf[8].split(";")

    id = attributes[0].split(" ")[1][1:-1]
    name = attributes[4].split(" ")[2][1:-1]

    mylist.insert(3, 0)
    mylist.insert(3, name + "_" + id)

    print(mylist)
    line_out = list(map(lambda x: str(x), mylist))
    line_out = "\t".join(line_out) + "\n"
    out.write(line_out)

out.close()
file.close()
