#!/usr/bin/env python
import os.path
from time import sleep
import random
import GtfDictionary

homo_sapiens_gtf_path = "../resources/homo-sapiens-gtf/Homo_sapiens.GRCh38.107.gtf" #gene file name
gene_panel_dimension = 100 #number of genes to randomly select

gene_dictionary = GtfDictionary.gtf_to_dictionary(homo_sapiens_gtf_path, "gene_id")

#prints a list of random genes
#TODO: cheange random sample to randomizing a number between the number of current keys, creating a new dictionary with the random
#chosen entry, copying the header and printing the dictionary with the appropriate method
print("\n- - - random gene panel - - -\n")
random_genes = random.sample(list(gene_dictionary.keys()), gene_panel_dimension)
print(random_genes)

gtf_output = open("../resources/gene-panel/gene_panel.gtf", "w")
gtf_output.write(gene_dictionary["gtf_header"])
for gene in random_genes:
    for line in gene_dictionary[gene]:
        gtf_output.write(str(line) + "\n")
gtf_output.close()