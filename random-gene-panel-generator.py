#!/usr/bin/env python
from operator import ge
import os.path
from time import sleep
import random
from GtfEntry import GtfEntry

homo_sapiens_gtf_path = "resources/homo-sapiens-gtf/Homo_sapiens.GRCh38.107.gtf" #gene file name
gene_panel_dimension = 100 #number of genes to randomly select

#if the file does not exist, suggest solution and exit the script
if not os.path.isfile(homo_sapiens_gtf_path):
    print("The gtf file does not exist. Go in resources/homo-sapiens-gtf and run homo-sapiens-gtf-download.sh")
    print("Closing in 5 seconds...")
    sleep(5)
    exit()

#reads the file
print("Reading " + homo_sapiens_gtf_path + "...")

homo_sapiens_gtf_file = open(homo_sapiens_gtf_path, "r")
homo_sapiens_gtf = homo_sapiens_gtf_file.readlines()
homo_sapiens_gtf_file.close()

print("File read")

#dictionary creation {"gene_id": (gtf_lines)}
print ("Creating dictionary...")

gene_dictionary = {}

for line in homo_sapiens_gtf:
    line = line.replace("\n", "")
    if(line[0] != "#"):
        entry = GtfEntry(line)
        gene_id = entry.get_gene_id()
        if gene_id in gene_dictionary:
            gene_dictionary[gene_id].append(line)
        else:
            gene_dictionary[gene_id] = [line]
del homo_sapiens_gtf #free some memory

print("Dictionary created")

#prints a list of random genes
print("\n- - - random gene panel - - -\n")
random_genes = random.sample(list(gene_dictionary.keys()), gene_panel_dimension)
print(random_genes)