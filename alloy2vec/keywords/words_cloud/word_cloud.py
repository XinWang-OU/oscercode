from collections import Counter
import re
import csv

keywords = [
    "metal", "alloy", "metallic materials", "extreme conditions", "extreme environments", 
    "severe conditions", "harsh conditions", "harsh environments", "harsh service conditions", 
    "harsh service environments", "extreme operating conditions", "high temperatures", 
    "cryogenic temperatures", "low temperatures", "high pressure", "creep", "shock", "impact", 
    "high strain rate", "ballistic", "ablation", "vaporization", "neutron", "proton", "helium", 
    "photon", "photons", "radiation", "irradiation", "nuclear reactors", "fission reactors", 
    "fusion reactors", "cladding materials", "corrosion", "corrosive", "molten salt", 
    "molten salts", "oxidation", "oxidative", "hydrogen embrittlement", "chemical reduction", "chemically reactive"
]


file_path = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/extracted_all.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read().lower()

for keyword in keywords:
    if ' ' in keyword:  
        text = text.replace(keyword, keyword.replace(' ', '_'))


words = re.findall(r'\w+', text)
word_counts = Counter(words)


keyword_counts = {keyword.replace(' ', '_'): word_counts[keyword.replace(' ', '_')] for keyword in keywords if keyword.replace(' ', '_') in word_counts}


output_path = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/words_cloud//keyword_counts.csv"

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Keyword', 'Frequency'])
    for keyword, frequency in keyword_counts.items():
        writer.writerow([keyword.replace('_', ' '), frequency]) 


print("Keyword frequency count has been saved to", output_path)