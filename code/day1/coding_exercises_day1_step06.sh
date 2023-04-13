#!/usr/bin/env bash

#set -x

# Function
# Input: $1: bedfile 2$: output file path
# Output: Bedtools intersect of $1 and tfbdConsSites fiete

mkdir -p $(dirname $2)
bedtools intersect -wa -a ../../output/day1/tfbsConsSites.bed -b $1 >> $2
