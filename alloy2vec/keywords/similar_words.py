import sys
import os
from gensim.models import Word2Vec

# Add the project directory to the system path
sys.path.append("/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main")

model_path = "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/training/models/updated_1model_all"

file_paths = [
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/alloy.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/AA_family_all.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/mechanical_properties.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_general.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_melt_ded.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_melt_general.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_melt_pbf.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_solid_binder.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_solid_cold_spray.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_solid_extrusion.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_solid_field_assisted.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_solid_friction_based.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/process_solid_general.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/thermal_properties.txt",
    "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/keywords_for_search.txt"
]
    
def find_similar_words(model, word):
    """Find and return similar words for a given word using the provided model."""
    try:
        return model.wv.most_similar(word, topn=5)
    except KeyError:
        return []

def process_files(model_path, file_paths):
    """Process each file to find similar words for each keyword and write to a new file."""
    model = Word2Vec.load(model_path)
    
    for file_path in file_paths:
        similar_words = []
        first_word_collected = False 
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                if words:
                    first_word = words[0]
                    if not first_word_collected:
                        first_word_file_path = os.path.join("/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/first_words/", f'firstword_{os.path.basename(file_path)}')
                        with open(first_word_file_path, 'w') as fw_file:
                            fw_file.write(first_word + '\n')
                        first_word_collected = True 
                        
                    similar = find_similar_words(model, first_word) + find_similar_words(model, first_word.lower())
                    similar_words.extend([word for word, _ in similar])

        # Determine the new file path for similar words
        similar_file_name = "similar_" + os.path.basename(file_path)
        new_file_path = os.path.join('/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/new_keywords/other_words', similar_file_name)
        
        # Write the similar words to the new file
        with open(new_file_path, 'w') as new_file:
            for word in set(similar_words):  # Use `set` to remove duplicates
                new_file.write(f'{word}\n')
                
# Execute the processing
process_files(model_path, file_paths)