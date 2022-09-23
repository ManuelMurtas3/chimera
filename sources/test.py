import re
from collections import Counter
import GtfDictionary
from GtfEntry import GtfEntry
from Transcript import ChimericTranscript, Transcript
import random

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
			transcript = Transcript(entry.get_attribute("gene_id"), id, len(fasta), '+', "0", fasta)
			transcripts.append(transcript)
			break

del fasta_content
del fasta_transcripts
del gene_dictionary
del gene_panel_keys

kmer_size = 15
dictionary_filter = {}

print("Creating filter dictionary...")

for transcript in transcripts:
	transcript_length = len(transcript.fasta_content)
	for i in range(0, transcript_length - kmer_size + 1):
		kmer = transcript.fasta_content[i : i + 5]
		if(kmer in dictionary_filter.keys()):
			dictionary_filter[kmer].add(transcript.gene_id)
		else:
			dictionary_filter[kmer] = set()
			dictionary_filter[kmer].add(transcript.gene_id)

print("Filter dictionary created")

reads = open("../resources/gene-panel/random_reads.out", 'r')
reads_content = reads.readlines()
reads.close()
read_transcripts = {}
current_read = ""
headers = {}
for line in reads_content:
	if(line[0] == "@"):
		current_read = line.strip().split("\t")[0]
		headers[current_read] = "\t".join(line.strip().split("\t")[1:])
		read_transcripts[current_read] = ""
	else:
		read_transcripts[current_read] = str(read_transcripts[current_read]) + line.strip()

del reads_content

print("Creating read classification profile...")

classification = open("../resources/gene-panel/classification.count", "w")

classification.write("Classification profile (k = " + str(kmer_size) + ")\n")
for read_id in read_transcripts.keys():
	classification.write(read_id + "\t" + headers[read_id] + "\n")
	read_length = len(read_transcripts[read_id])
	for i in range(0, read_length - kmer_size + 1):
		kmer = read_transcripts[read_id][i : i + 5]
		gene_list = dictionary_filter[kmer]
		classification.write(str(i + 1) + ".\t" + "\t".join(gene_list) + "\n")

classification.close()
print("Classification profile created")