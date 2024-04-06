import os, re, sys

bad_chars = [',', ';', ':', '!', '.', '(', ')', '"', "*"] 

input_file_path = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/processing/data/yearchunk/extracted_2009_2004.txt"
output_file_path = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/processing/data/yearchunk/cleaned_2009_2004.txt"

os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

with open(output_file_path, 'a+') as corpus_w:
    with open(input_file_path, "r") as corpus:
        data = corpus.readlines()
        for line in data:
            for ii in bad_chars: 
                line = line.replace(ii, '') 
            corpus_w.write(line + '\n')
