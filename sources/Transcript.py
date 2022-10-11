class Transcript:
    def __init__(self, gene_id, transcript_id, length, strand, error, fasta_content):
        self.gene_id = gene_id
        self.transcript_id = transcript_id
        self.start = 1
        self.end = int(length)
        self.strand = strand
        self.error = error
        self.fasta_content = fasta_content
        self.step_size = 80
    
    def to_str(self, read_id):
        output = self.gene_id + "\t" + self.transcript_id + "\t" + str(self.start) + "\t" + str(self.end)
        output = output + "\t" + self.strand + "\t" + str(self.error) + "\n"
        
        if(len(self.fasta_content) > self.step_size):
            output_fasta = [self.fasta_content[x : x+self.step_size] for x in range(0, (len(self.fasta_content) // self.step_size + 1) * self.step_size, self.step_size)]
            output = output + "\n".join(output_fasta) #might be a problem if the fasta is under 80 characters
        else:
            output = output + self.fasta_content + "\n"
        return ">@" + read_id + "\t" + output


class ChimericTranscript(Transcript):
    def __init__(self, gene_id1, gene_id2, transcript_id1, transcript_id2, length, strand1, strand2, error, fasta_content, bp):
        super().__init__(gene_id1, transcript_id1, length, strand1, error, fasta_content)
        self.gene_id2 = gene_id2
        self.transcript_id2 = transcript_id2
        self.strand2 = strand2
        self.start2 = 0
        self.end2 = 0
        self.bp = int(bp)
        #bp = breakpoint
    
    def to_str(self, read_id):
        output =self.gene_id + "\t" + self.transcript_id + "\t" + str(self.start) + "\t" + str(self.end)
        output = output + "\t" + self.strand + "\t" + str(self.error) + " | "

        output = output + self.gene_id2 + "\t" + self.transcript_id2 + "\t" + str(self.start2) + "\t" + str(self.end2)
        output = output + "\t" + self.strand2 + "\t" + str(self.error) + "\n"

        if(len(self.fasta_content) > self.step_size):
            output_fasta = [self.fasta_content[x : x+self.step_size] for x in range(0, (len(self.fasta_content) // self.step_size + 1) * self.step_size, self.step_size)]
            output = output + "\n".join(output_fasta)
        else:
            output = output + self.fasta_content + "\n"
        return ">@" + read_id + "\t" + output