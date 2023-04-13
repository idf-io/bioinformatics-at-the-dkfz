#!/usr/bin/env bash

#set -x
mkdir -p ../../output/day1

# Format cpgIsland raw file
cut -f 2,3,4 ../../data/cpgIslandExt.txt > ../../output/day1/cpgIslandExt.bed

# STEP 3
# Bedtools intersect: a='reference sequence'=promoters b='sequence to compare'=cpgIslands

# Promoters intersect cpgIslands
bedtools intersect -wa -a ../../output/day1/gencode.v19.annotation_promoters.bed -b ../../output/day1/cpgIslandExt.bed > ../../output/day1/cpgIsland_promoters_intersection.bed

# Promoters diff cpgIsland
bedtools intersect -v -a ../../output/day1/gencode.v19.annotation_promoters.bed -b ../../output/day1/cpgIslandExt.bed > ../../output/day1/cpgIsland_promoters_difference.bed

# STEP 4
mkdir -p ../../output/day1/{CgiProm,NonCgiProm}

for chr in $(cut -f 1 ../../output/day1/cpgIsland_promoters_intersection.bed | uniq)
do
	grep -P "$chr\s"  ../../output/day1/cpgIsland_promoters_intersection.bed > ../../output/day1/CgiProm/cpgIsland_promoters_intersection_$chr.bed
done

for chr in $(cut -f 1 ../../output/day1/cpgIsland_promoters_difference.bed | uniq)
do
	grep -P "$chr\s"  ../../output/day1/cpgIsland_promoters_difference.bed > ../../output/day1/NonCgiProm/cpgIsland_promoters_difference_$chr.bed
done
