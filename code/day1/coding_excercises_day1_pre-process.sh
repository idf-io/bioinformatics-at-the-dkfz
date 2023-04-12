#!/usr/bin/env bash

set -x

tail -n +6 ../../data/gencode.v19.annotation.gtf > ../../data/gencode.v19.annotation_no-meta.gtf

cut -f 1 ../../data/gencode.v19.annotation_no-meta.gtf > ../../output/cache/temp1.txt
cut -f 4 ../../data/gencode.v19.annotation_no-meta.gtf > ../../output/cache/temp2.txt
awk '{print $1-1}' ../../output/cache/temp2.txt > ../../output/cache/temp2-1.txt
cut -f 5 ../../data/gencode.v19.annotation_no-meta.gtf > ../../output/cache/temp3.txt

paste ../../output/cache/temp1.txt ../../output/cache/temp2-1.txt ../../output/cache/temp3.txt > ../../data/gencode.v19.annotation.bed

rm ../../output/cache/temp1.txt
rm ../../output/cache/temp2.txt
rm ../../output/cache/temp2-1.txt
rm ../../output/cache/temp3.txt
