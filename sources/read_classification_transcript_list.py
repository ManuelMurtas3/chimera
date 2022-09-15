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

kmer_size = 5
dictionary_filter = {}

print("Creating filter dictionary...")

for transcript in transcripts:
	transcript_length = len(transcript.fasta_content)
	for i in range(0, transcript_length - kmer_size + 1):
		kmer = transcript.fasta_content[i : i + 5]
		if(kmer in dictionary_filter.keys()):
			dictionary_filter[kmer].append(transcript.transcript_id)
		else:
			dictionary_filter[kmer] = [transcript.transcript_id]

print("Filter dictionary created")

reads = open("../resources/gene-panel/random_reads.out", 'r')
reads_content = reads.readlines()
reads.close()
read_transcripts = {}
current_read = ""
for line in reads_content:
	if(line[0] == "@"):
		current_read = line.strip().split("\t")[0]
		read_transcripts[current_read] = ""
	else:
		read_transcripts[current_read] = str(read_transcripts[current_read]) + line.strip()

del reads_content

print("Creating read classification profile...")

classification = open("../resources/gene-panel/classification.transcript.list.count", "w")

for read_id in read_transcripts.keys():
	read_length = len(read_transcripts[read_id])
	transcript_list = []
	for i in range(0, read_length - kmer_size + 1):
		kmer = read_transcripts[read_id][i : i + 5]
		transcript_list.extend(dictionary_filter[kmer])
	classification.write(read_id + " classification: \n")
	gene_counter = Counter(transcript_list)
	for (gene_id, count) in gene_counter.most_common():
		classification.write("\t" + gene_id + ": " + str(count) + "\n")
	classification.write("\n")

classification.close()
print("Classification profile created")