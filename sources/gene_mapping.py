import re
from collections import Counter
import GtfDictionary
from GtfEntry import GtfEntry
from Transcript import ChimericTranscript, Transcript
import random

print("Mapping genes...")

gene_dictionary = GtfDictionary.gtf_to_dictionary("../resources/gene-panel/gene_panel.gtf", "transcript_id")
gene_panel_keys = list(gene_dictionary.keys())

fasta = open("../resources/gene-panel/transcripts.fa", 'r')
fasta_content = fasta.readlines()
fasta.close()
fasta_transcripts = {}
current_transcript = ""
for line in fasta_content:
	if(line[0] == ">"):
		current_transcript = line.strip().split(" ")[0][1:]
		fasta_transcripts[current_transcript] = ""
	else:
		fasta_transcripts[current_transcript] = str(fasta_transcripts[current_transcript]) + line.strip()

transcripts = []

for id, fasta in fasta_transcripts.items():
	entries = gene_dictionary[id]
	for line in entries:
		entry = GtfEntry(line)
		if entry.feature == "transcript":
			transcript_gene_id = entry.get_attribute("gene_id") #
			transcript = Transcript(entry.get_attribute("gene_id"), id, len(fasta), '+', "0", fasta)
			transcripts.append(transcript)

gene_mapping = open("../resources/gene-panel/gene_mapping.out", 'w')
for transcript in transcripts:
	gene_mapping.write(transcript.transcript_id + "\t" + transcript.gene_id + "\n")
gene_mapping.close()

print("Genes mapped.")