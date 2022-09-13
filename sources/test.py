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
			transcript = Transcript(entry.get_attribute("gene_id"), id, len(fasta), entry.strand, "0", fasta)
			transcripts.append(transcript)
			break

test_output = open("test.output", "w")
#for transcript in transcripts:
#	test_output.write(transcript.to_str() + "\n")
#test_output.close()

read_size = 150

#generate reads here
bp_range = [30, 70]

while len(transcripts) > 1:
	transcript1 = random.choice(transcripts)
	transcripts.remove(transcript1)
	is_chimeric = random.choice([True, False])
	if is_chimeric:
		transcript2 = random.choice(transcripts)
		transcripts.remove(transcript2)
		bp = round((read_size / 100) * random.randint(bp_range[0], bp_range[1]))
		if transcript1.end >= bp and transcript2.end >= read_size - bp:
			#random start for transcript 1
			transcript1_start = random.randint(0, transcript1.end - bp)
			print(str(transcript1.start) + " -> " + str(transcript1_start) + " -> " + 
			str(transcript1_start + bp) + " -> " + str(transcript1.end) + " (bp: " + str(bp) + ")")

			transcript2_start = random.randint(0, transcript2.end - (read_size - bp))
			print(str(transcript2.start) + " -> " + str(transcript2_start) + " -> " + 
			str(transcript2_start + (read_size - bp)) + " -> " + str(transcript2.end) + " (bp: " + str(bp) + ")")

			chimeric_transcript = ChimericTranscript(transcript1.gene_id, transcript2.gene_id,
			transcript1.transcript_id, transcript2.transcript_id,
			read_size, transcript1.strand, transcript2.strand, 0,
			transcript1.fasta_content[transcript1_start:transcript1_start + bp] + 
				transcript2.fasta_content[transcript2_start:transcript2_start + (read_size - bp)], bp) #CHANGE THIS IN RANDOM LOCATIONS!!!
			
			chimeric_transcript.start = transcript1_start
			chimeric_transcript.end = transcript1_start + bp - 1
			chimeric_transcript.start2 = transcript2_start
			chimeric_transcript.end2 = transcript2_start + (read_size - bp) - 1
			
			test_output.write(chimeric_transcript.to_str() + "\n")
		else:
			if transcript1.end > read_size:
				transcript1.fasta_content = transcript1.fasta_content[:read_size]
			test_output.write(transcript1.to_str() + "\n")
			if transcript2.end > read_size:
				transcript2.fasta_content = transcript1.fasta_content[:read_size]
			test_output.write(transcript2.to_str() + "\n")
			#CHANGE THIS IN NEW BP CALCULATION

	else:
		if transcript1.end >= read_size:
			start = random.randint(transcript1.start, transcript1.end - read_size)
			transcript1.start = start
			transcript1.end = start + read_size
			transcript1.fasta_content = transcript1.fasta_content[transcript1.start : transcript1.end]
		test_output.write(transcript1.to_str() + "\n")


if len(transcripts) == 1:
	transcript = transcripts[0]
	if transcript.end >= read_size:
		start = random.randint(transcript.start, transcript.end - read_size)
		transcript.start = start
		transcript.end = start + read_size
	transcript.fasta_content = transcript.fasta_content[transcript.start : transcript.end]
	test_output.write(transcript.to_str() + "\n")

test_output.close()