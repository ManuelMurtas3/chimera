#gtf file format
#seqname source feature start end score strand frame [attributes]

class GtfEntry:
    def __init__(self, gtf_line):
        gtf_values = gtf_line.split("\t")
        self.seqname = gtf_values[0]
        self.source = gtf_values[1]
        self.feature = gtf_values[2]
        self.start = int(gtf_values[3])
        self.end = int(gtf_values[4])
        self.score = gtf_values[5]
        self.strand = gtf_values[6]
        self.frame = gtf_values[7]
        self.attributes = None
        if(len(gtf_values) == 9):
            self.attributes = gtf_values[8].split(";")
    
    def has_attribute(self, attribute_string):
        if(self.attributes != None):
            for attribute in self.attributes:
                if attribute_string in attribute:
                    return True
        return False

    def get_attribute(self, attribute_string):
        if(self.attributes != None):
            for attribute in self.attributes:
                if attribute_string in attribute:
                    return attribute.strip().split(" ")[1][1:][:-1]
        return None