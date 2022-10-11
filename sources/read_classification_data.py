from functools import partial
import Bio
from Bio import SeqIO
from numpy import full

print("Classifying reads")

transcripts = list(SeqIO.parse('../resources/gene-panel/transcripts.fa', 'fasta'))
read_size = 150
kmer_size = 10

tr_kmers = {}

for tr in transcripts:
	kmer_list = [(i, str(tr.seq)[i : i + kmer_size]) for i in range(len(str(tr.seq)) - kmer_size + 1)]
	for (offset, kmer) in kmer_list:
		inner_dict = tr_kmers.get(kmer, {})
		value = inner_dict.get(tr.id, [])
		value.append(offset)
		inner_dict.update([(tr.id, value)])
		tr_kmers.update([(kmer, inner_dict)])

reads = list(SeqIO.parse('../resources/gene-panel/random_reads.fa', 'fasta'))
reads_statistics = {
	"total" : 0,
	"chimeric": 0,
	"non_chimeric": 0,
	"chimeric_match": 0,
	"non_chimeric_match": 0,
	"match": 0,
	"mismatch": 0,
	"assigned": 0,
	"assigned_chimeric" : 0,
	"assigned_non_chimeric" : 0,
	"correct_assignment": 0,
	"correct_assignment_chimeric": 0,
	"correct_assignment_non_chimeric": 0,
	"incorrect_assignment": 0,
	"incorrect_assignment_chimeric": 0,
	"incorrect_assignment_non_chimeric": 0,
	"unassigned": 0,
	"unassigned_chimeric": 0,
	"unassigned_non_chimeric": 0,
	"assignable": 0,
	"assignable_chimeric": 0,
	"assignable_non_chimeric": 0
}

#for r in reads:
#    kmer_list = [(i, str(r.seq)[i : i + kmer_size]) for i in range(len(str(r.seq)) - kmer_size + 1)]
#    print(r.id)
#    for (offset, kmer) in kmer_list:
#        print(offset)
#        inner_dict = tr_kmers.get(kmer, {})
#        for id in inner_dict:
#            print(id)

#carico un dizionario di mapping trascritto -> gene
gene_mapping = {}
gene_mapping_file = open("../resources/gene-panel/gene_mapping.out", 'r')
for line in gene_mapping_file.readlines():
	transcript, gene = line.strip().split("\t")
	gene_mapping[transcript] = gene

for r in reads:
	tr_distr = {}
	kmer_list = [(i, str(r.seq)[i : i + kmer_size]) for i in range(len(str(r.seq)) - kmer_size + 1)]
	for (offset, kmer) in kmer_list:
		inner_dict = tr_kmers.get(kmer, {})
		for id_tr in inner_dict:
			inner_list = tr_distr.get(id_tr, [])
				
			if len(inner_dict[id_tr]) == 1:
				tr_offset = inner_dict[id_tr][0]           
				inner_list.append([offset, tr_offset])
				
			tr_distr.update([(id_tr, inner_list)])
	
	#Vengono per ora scartati i kmers duplicati nel trascritto (anche se sono coerenti con il read)
	
	#Tengo solo i trascritti con successioni crescenti
	id_to_del = []
	for id_tr in tr_distr:
		tr_offsets = [offs[1] for offs in tr_distr[id_tr]]
		tr_offsets2 = [offs[1] for offs in tr_distr[id_tr]]
		tr_offsets.sort()
			
		if tr_offsets != tr_offsets2:
			id_to_del.append(id_tr)
	
	for id_tr in id_to_del:
		tr_distr.pop(id_tr)
			   
	#Tengo solo i trascritti che hanno almeno N kmers condivisi con il read (N da calcolare...)
	N = 10
	id_to_del = []
	for id_tr in tr_distr:
		tr_offsets = [offs[1] for offs in tr_distr[id_tr]]
		if len(tr_offsets) < N:
			id_to_del.append(id_tr)
	
	for id_tr in id_to_del:
		tr_distr.pop(id_tr)

	#salvataggio offset terminato, ora calcolo coperture
	#print(r.description)

	if r.id[-1] == 'c':
		reads_statistics["chimeric"] += 1
	else:
		reads_statistics["non_chimeric"] += 1

	full_coverage = []
	partial_coverage = []
	full_coverage_genes = []
	partial_coverage_genes = []

	for (id_tr, coverage) in tr_distr.items():
		coverage_length = len(coverage)
		if coverage_length == read_size - kmer_size + 1:
			full_coverage.append((id_tr, coverage_length + kmer_size - 1))
			full_coverage_genes.append(gene_mapping[id_tr])
		else:
			partial_coverage.append((id_tr, coverage_length + kmer_size - 1))
			partial_coverage_genes.append(gene_mapping[id_tr])
	
	if (len(full_coverage) > 0 and r.id[-1] != 'c') or (len(full_coverage) == 0 and r.id[-1] == 'c'):
		reads_statistics["match"] += 1
		if r.id[-1] == 'c':
			reads_statistics["chimeric_match"] += 1		
		else:
			reads_statistics["non_chimeric_match"] += 1

		if(r.id[-1] == 'c'):
			genes = [r.description.strip().split("\t")[1]]
			genes.append(r.description.strip().split("|")[1].strip().split("\t")[0])
			genes = sorted(genes)

			if len(partial_coverage_genes) == 2 and len(full_coverage_genes) == 0:
				reads_statistics["assigned"] += 1
				reads_statistics["assigned_chimeric"] += 1
				if sorted(partial_coverage_genes) == genes:
					reads_statistics["correct_assignment"] += 1
					reads_statistics["correct_assignment_chimeric"] += 1
				else:
					reads_statistics["incorrect_assignment"] += 1
					reads_statistics["incorrect_assignment_chimeric"] += 1
			elif len(full_coverage_genes) == 0 and genes[0] in partial_coverage_genes and genes[1] in partial_coverage_genes:
				reads_statistics["assignable"] += 1
				reads_statistics["assignable_chimeric"] += 1

				potential_assignments = []
				potential_genes = set()

				for i in range (len(partial_coverage) - 1):
					base = partial_coverage[0]
					for target in partial_coverage[i + 1:]:
						if gene_mapping[base[0]] != gene_mapping[target[0]]:
							potential_assignments.append((base, target))

				for potential_coverage in potential_assignments:
					potential_genes.add(tuple(sorted((gene_mapping[potential_coverage[0][0]], gene_mapping[potential_coverage[1][0]]))))
				
				assigned = False
				if len(potential_genes) == 1:
					for potential_gene_couple in potential_genes:
						if sorted(potential_gene_couple) == sorted(genes):
							assigned = True
							break

				if assigned == True:
					reads_statistics["assignable"] -= 1
					reads_statistics["assignable_chimeric"] -= 1
					reads_statistics["assigned"] += 1
					reads_statistics["assigned_chimeric"] += 1
					reads_statistics["correct_assignment"] += 1
					reads_statistics["correct_assignment_chimeric"] += 1
				
			else:
				reads_statistics["unassigned"] += 1
				reads_statistics["unassigned_chimeric"] += 1

		else:
			gene = r.description.strip().split("\t")[1]
			if len(full_coverage_genes) == 1:
				reads_statistics["assigned"] += 1
				reads_statistics["assigned_non_chimeric"] += 1
				if full_coverage_genes[0] == gene:
					reads_statistics["correct_assignment"] += 1
					reads_statistics["correct_assignment_non_chimeric"] += 1
				else:
					reads_statistics["incorrect_assignment"] += 1
					reads_statistics["incorrect_assignment_non_chimeric"] += 1
			elif len(full_coverage_genes) > 0 and gene in full_coverage_genes:
				reads_statistics["assignable"] += 1
				reads_statistics["assignable_non_chimeric"] += 1
			else:
				reads_statistics["unassigned"] += 1
				reads_statistics["unassigned_non_chimeric"] += 1
	else:
		reads_statistics["mismatch"] += 1


reads_statistics["total"] = reads_statistics["chimeric"] + reads_statistics["non_chimeric"]

print("Classification complete!\n\n")
print("Number of reads: " + str(reads_statistics["total"]))

print("Number of matches over total: " + str(reads_statistics["match"]) + " (" + str("{:.2f}".format(reads_statistics["match"] * 100 / reads_statistics["total"])) + "%)")
print("Number of mismatches over total: " + str(reads_statistics["mismatch"]) + " (" + str("{:.2f}".format(reads_statistics["mismatch"] * 100 / reads_statistics["total"])) + "%)")

print("\n--- chimeric data ---\n")

print("Number of chimeric reads: " + str(reads_statistics["chimeric"]))
print("Number of correctly assigned chimeric reads over chimeric reads: " + 
	str(reads_statistics["correct_assignment_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["correct_assignment_chimeric"] * 100 / reads_statistics["chimeric"])) + "%)")
print("Number of incorrectly assigned chimeric reads over chimeric reads: " + 
	str(reads_statistics["incorrect_assignment_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["incorrect_assignment_chimeric"] * 100 / reads_statistics["chimeric"])) + "%)")
print("Number of assignable chimeric reads over chimeric reads: " + 
	str(reads_statistics["assignable_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["assignable_chimeric"] * 100 / reads_statistics["chimeric"])) + "%)")
print("Number of unassigned chimeric reads over chimeric reads: " + 
	str(reads_statistics["unassigned_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["unassigned_chimeric"] * 100 / reads_statistics["chimeric"])) + "%)")
print("Number of identified chimeric reads over chimeric reads: " + 
	str(reads_statistics["chimeric_match"]) + " (" + str("{:.2f}".format(reads_statistics["chimeric_match"] * 100 / reads_statistics["chimeric"])) + "%)")
print("Number of unidentified chimeric reads over chimeric reads: " + 
	str(reads_statistics["chimeric"] - reads_statistics["chimeric_match"]) + " (" + 
	str("{:.2f}".format((reads_statistics["chimeric"] - reads_statistics["chimeric_match"]) * 100 / reads_statistics["chimeric"])) + "%)")

print("\n--- non chimeric data ---\n")

print("Number of non chimeric reads: " + str(reads_statistics["non_chimeric"]))
print("Number of correctly assigned non chimeric reads over non chimeric reads: " + 
	str(reads_statistics["correct_assignment_non_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["correct_assignment_non_chimeric"] * 100 / reads_statistics["non_chimeric"])) + "%)")
print("Number of incorrectly assigned non chimeric reads over non chimeric reads: " + 
	str(reads_statistics["incorrect_assignment_non_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["incorrect_assignment_non_chimeric"] * 100 / reads_statistics["non_chimeric"])) + "%)")
print("Number of assignable non chimeric reads over non chimeric reads: " + 
	str(reads_statistics["assignable_non_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["assignable_non_chimeric"] * 100 / reads_statistics["non_chimeric"])) + "%)")
print("Number of unassigned non chimeric reads over non chimeric reads: " + 
	str(reads_statistics["unassigned_non_chimeric"]) + " (" + str("{:.2f}".format(reads_statistics["unassigned_non_chimeric"] * 100 / reads_statistics["non_chimeric"])) + "%)")
print("Number of identified non chimeric reads over non chimeric reads: " + 
	str(reads_statistics["non_chimeric_match"]) + " (" + str("{:.2f}".format(reads_statistics["non_chimeric_match"] * 100 / reads_statistics["non_chimeric"])) + "%)")
print("Number of unidentified non chimeric reads over non chimeric reads: " + 
	str(reads_statistics["non_chimeric"] - reads_statistics["non_chimeric_match"]) + " (" + 
	str("{:.2f}".format((reads_statistics["non_chimeric"] - reads_statistics["non_chimeric_match"]) * 100 / reads_statistics["non_chimeric"])) + "%)")

print("Saving data...")

data_out = open("../resources/chimera_data.csv", "a")

data_out.write(str(reads_statistics["total"]) + ",")
data_out.write(str(reads_statistics["match"]) + ",")
data_out.write(str(reads_statistics["mismatch"]) + ",")
data_out.write(str(reads_statistics["chimeric"]) + ",")
data_out.write(str(reads_statistics["correct_assignment_chimeric"]) + ",")
data_out.write(str(reads_statistics["incorrect_assignment_chimeric"]) + ",")
data_out.write(str(reads_statistics["assignable_chimeric"]) + ",")
data_out.write(str(reads_statistics["unassigned_chimeric"]) + ",")
data_out.write(str(reads_statistics["chimeric_match"]) + ",")
data_out.write(str(reads_statistics["chimeric"] - reads_statistics["chimeric_match"]) + ",")
data_out.write(str(reads_statistics["non_chimeric"]) + ",")
data_out.write(str(reads_statistics["correct_assignment_non_chimeric"]) + ",")
data_out.write(str(reads_statistics["incorrect_assignment_non_chimeric"]) + ",")
data_out.write(str(reads_statistics["assignable_non_chimeric"]) + ",")
data_out.write(str(reads_statistics["unassigned_non_chimeric"]) + ",")
data_out.write(str(reads_statistics["non_chimeric_match"]) + ",")
data_out.write(str(reads_statistics["non_chimeric"] - reads_statistics["non_chimeric_match"]) + "\n")

data_out.close()

print("Data saved")