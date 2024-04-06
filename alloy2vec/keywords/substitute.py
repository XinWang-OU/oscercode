import argparse
import re
from tqdm import tqdm

keyword_files = ["/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/alloy.txt", 
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/mechanical_properties.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_general.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_melt_ded.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_melt_general.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_melt_pbf.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_solid_binder.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_solid_cold_spray.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_solid_extrusion.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_solid_field_assisted.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_solid_friction_based.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/process_solid_general.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/thermal_properties.txt",
                 "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/keywords_for_search.txt"]

keyword_mapping = {}
for file in keyword_files:
    with open(file, 'r') as f:
        for line in f:
            phrases = line.strip().split()
            if phrases:
                main_phrase = phrases[0]
                for phrase in phrases:
                    keyword_mapping[phrase] = main_phrase


# Set up ArgumentParser to accept the input file path
parser = argparse.ArgumentParser(description='Process keywords in text files.')
parser.add_argument('input_files', type=str, nargs='+', help='The path to the input file containing text to process.')
args = parser.parse_args()

# Loop over each input file and process it
for input_file in args.input_files:
    # Reading the current input file
    with open(input_file, 'r') as f:
        content = f.read()

    sorted_keyword_items = sorted(keyword_mapping.items(), key=lambda x: len(x[0].replace('_', '')), reverse=True)

    replacement_counts = {}
    for phrase, main_phrase in tqdm(sorted_keyword_items, desc="Processing keywords"):
        non_underscore_phrase = phrase.replace('_', ' ')
        pattern = re.compile(re.escape(non_underscore_phrase), re.IGNORECASE)
        matches = pattern.findall(content)
        count = len(matches)
        if count > 0:
            content = pattern.sub(main_phrase, content)
            replacement_counts[main_phrase] = replacement_counts.get(main_phrase, 0) + count


    aa_phrases = re.findall(r'\bAA \d+(?:-\w+)?\b', content)
    for phrase in tqdm(aa_phrases, desc="Processing AA phrases"):
        new_phrase = phrase.replace(' ', '_')
        content = content.replace(phrase, new_phrase)
        replacement_counts[new_phrase] = replacement_counts.get(new_phrase, 0) + 1

    base_file_name = input_file.split('/')[-1]

    output_file_name_1 = "1cleaned_" + base_file_name
    output_file_path_1 = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/time_slice/" + output_file_name_1
    with open(output_file_path_1, 'w') as f:
        f.write(content)

    output_file_name_2 = "AA_family_" + base_file_name
    output_file_path_2 = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/time_slice/" + output_file_name_2
    with open(output_file_path_2, 'w') as f:
        for phrase in aa_phrases:
            f.write(phrase + '\n')

    output_file_name_3 = "replacement_counts_" + base_file_name
    output_file_path_3 = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/time_slice/" + output_file_name_3
    with open(output_file_path_3, 'w') as f:
        for phrase, count in replacement_counts.items():
            f.write(f"{phrase}: {count}\n")
