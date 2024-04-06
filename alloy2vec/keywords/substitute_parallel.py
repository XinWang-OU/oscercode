import argparse
import re
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed


# Assuming the list of keyword files remains the same
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

def load_keyword_mapping(keyword_files):
    keyword_mapping = {}
    for file in keyword_files:
        with open(file, 'r') as f:
            for line in f:
                phrases = line.strip().split()
                if phrases:
                    main_phrase = phrases[0]
                    for phrase in phrases:
                        keyword_mapping[phrase] = main_phrase
    return keyword_mapping

def process_chunk(content, keyword_mapping):
    # Processing logic for each chunk
    sorted_keyword_items = sorted(keyword_mapping.items(), key=lambda x: len(x[0].replace('_', '')), reverse=True)
    replacement_counts = {}
    for phrase, main_phrase in sorted_keyword_items:
        non_underscore_phrase = phrase.replace('_', ' ')
        pattern = re.compile(re.escape(non_underscore_phrase), re.IGNORECASE)
        matches = pattern.findall(content)
        count = len(matches)
        if count > 0:
            content = pattern.sub(main_phrase, content)
            replacement_counts[main_phrase] = replacement_counts.get(main_phrase, 0) + count

    # Process AA phrases
    aa_phrases = re.findall(r'\bAA \d+(?:-\w+)?\b', content)
    for phrase in aa_phrases:
        new_phrase = phrase.replace(' ', '_')
        content = content.replace(phrase, new_phrase)
        replacement_counts[new_phrase] = replacement_counts.get(new_phrase, 0) + 1

    return content, aa_phrases, replacement_counts

def parallel_process_file(input_file, keyword_mapping):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.readlines()

    # Determine the number of lines per chunk (aiming for 128 chunks)
    n_chunks = 90
    chunk_size = len(content) // n_chunks + (len(content) % n_chunks > 0)

    # Split content into chunks
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    # Use ProcessPoolExecutor to process chunks in parallel
    processed_chunks = []
    with ProcessPoolExecutor(max_workers=n_chunks) as executor:
        future_to_chunk = {executor.submit(process_chunk, ''.join(chunk), keyword_mapping): chunk for chunk in chunks}
        for future in tqdm(concurrent.futures.as_completed(future_to_chunk), total=len(future_to_chunk), desc="Processing chunks"):
            chunk_result = future.result()
            processed_chunks.append(chunk_result)

    # Combine processed chunks
    combined_content = ''.join([result[0] for result in processed_chunks])
    combined_aa_phrases = sum([result[1] for result in processed_chunks], [])
    combined_replacement_counts = {}
    for _, _, replacement_counts in processed_chunks:
        for key, value in replacement_counts.items():
            combined_replacement_counts[key] = combined_replacement_counts.get(key, 0) + value

    return combined_content, combined_aa_phrases, combined_replacement_counts

def main():
    # Load the keyword mapping
    keyword_mapping = load_keyword_mapping(keyword_files)

    parser = argparse.ArgumentParser(description='Process keywords in text files in parallel.')
    parser.add_argument('input_files', type=str, nargs='+', help='The path to the input file containing text to process.')
    args = parser.parse_args()

    for input_file in args.input_files:
        processed_content, aa_phrases, replacement_counts = parallel_process_file(input_file, keyword_mapping)

        # Write the processed content and other information to output files
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
            
if __name__ == "__main__":
    main()
