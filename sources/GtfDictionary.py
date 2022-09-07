#!/usr/bin/env python
import os.path
from time import sleep
from GtfEntry import GtfEntry

#I want to change this function so that only one line at a time gets read so that we don't have to use double the memory to store the
#information, but just the dictionary size plus one line of space (reducing it by half)
def gtf_to_dictionary(gtf_file_path, dictionary_id):
    if not os.path.isfile(gtf_file_path):
        print("The gtf file " + gtf_file_path + " does not exist.")
        return None
    
    print("Reading " + gtf_file_path + "...")

    gtf_file = open(gtf_file_path, "r")
    gtf_content = gtf_file.readlines()
    gtf_file.close()

    print("File read")
    print ("Creating dictionary...")

    gtf_dictionary = {}
    gtf_header = ""

    for line in gtf_content:
        line = line.replace("\n", "")
        if(line[0] != "#"):
            entry = GtfEntry(line)
            if entry.has_attribute(dictionary_id):
                entry_key = entry.get_attribute(dictionary_id)
                if entry_key in gtf_dictionary:
                    gtf_dictionary[entry_key].append(line)
                else:
                    gtf_dictionary[entry_key] = [line]
        else:
            gtf_header = gtf_header + line + "\n"

    gtf_dictionary["gtf_header"] = gtf_header

    del gtf_content #free some memory

    print("Dictionary created")

    return gtf_dictionary

def dictionary_to_gtf(dictionary, gtf_file_path):
    gtf_output = open(gtf_file_path, "w")
    gtf_output.write(dictionary["gtf_header"])
    for entry in dictionary:
        for line in entry:
            gtf_output.write(str(line) + "\n")
    gtf_output.close()