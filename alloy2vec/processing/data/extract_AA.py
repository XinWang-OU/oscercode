import re
from tqdm import tqdm

pattern = re.compile(r'([^.!?]*AA\s+\d+[^.!?]*[.!?])')

with open('/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/processing/data/original_all.txt', 'r') as source_file:
    lines = source_file.readlines()

with tqdm(total=len(lines), desc="Processing") as pbar, \
     open('/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/processing/data/AA_numl.txt', 'w') as output_file:
    for line in lines:
        matches = pattern.findall(line)
        for match in matches:
            output_file.write(match.strip() + '\n')
        pbar.update(1)
