#!/usr/bin/env bash

# This script extracts the relevant informatino of the tfbs.txt file to create a .bed format

#set -x
mkdir -p ../../data/day1

cut -f 2- ../../data/tfbsConsSites.txt > ../../output/day1/tfbsConsSites.bed
