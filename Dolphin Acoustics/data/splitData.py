import os
import re
import shutil
import random
from collections import defaultdict
from math import ceil
 
# Source and destination directories
source_dir = "ocean_downloads"
dest_dir = "split_ocean_downloads"
 
# Set random seed for reproducibility
random.seed(42)
 
# Function to extract encounter ID from filename
def extract_encounter_id(filename):
    # Extract encounter ID (like enc065)
    enc = filename.split("_")[1].split("-")[2]
    enc.split(".")[0]
    return enc
 
# Function to get species names from filenames
# Example filename:
# 3ebfce8d-769b-11ef-9a56-0050568e393c_Selection-1-20170922T003704-Lasker_AC_150.wav
# Other filenames will NOT WORK

def get_species_name(source_dir):
    species=[]
    for filename in os.listdir(source_dir):
        s = filename.split("_")[0]
        if s not in species:
            print(s)
            species.append(s)
    return species

def run_split():
    # Create destination directories
    os.makedirs(dest_dir, exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "training"), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "testing"), exist_ok=True)
    
    species = get_species_name(source_dir)

    for species_name in species:
        os.makedirs(os.path.join(dest_dir, "training", species_name), exist_ok=True)
        os.makedirs(os.path.join(dest_dir, "testing", species_name), exist_ok=True)
    
    # Process each species
    for species_name in species:
        print(f"Processing {species_name}...")
    
        # Get list of audio files
        # species_dir = os.path.join(source_dir, species_name)
        # if not os.path.exists(species_dir):
        #     print(f"  Directory not found: {species_dir}")
        #     continue
        audio_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        if not audio_files:
            print(f"  No files found in {source_dir}")
            continue
    
        # Group files by encounter
        encounters = defaultdict(list)
        for file in audio_files:
            encounter_id = extract_encounter_id(file)
            if encounter_id:
                encounters[encounter_id].append(file)
            else:
                print(f"  Warning: Could not extract encounter ID from {file}")
                # Files without encounter ID go to a special group
                encounters["unknown"].append(file)
    
        print(f"  Found {len(encounters)} unique encounters")

        # Split encounters into training and testing sets (70/30)
        encounter_ids = list(encounters.keys())
        random.shuffle(encounter_ids)
    
        split_idx = ceil(len(encounter_ids) * 0.7)
        training_encounters = encounter_ids[:split_idx]
        print(f"  Training encounters: {training_encounters}")
        testing_encounters = encounter_ids[split_idx:]
        print(f"  Testing encounters: {testing_encounters}")

        encounter_sizes = []
        for f in encounters.values():
            encounter_sizes.append(len(f))
        print(f"  Encounter sizes: {encounter_sizes}")
        encounter_size = min(encounter_sizes)
        if(encounter_size < 20):
            encounter_size = 20
        print(f"  Encounter size: {encounter_size} file(s)")

    
        print(f"  Split: {len(training_encounters)} encounters for training, {len(testing_encounters)} for testing")
    
        # Copy files to destination
        train_count = 0
        test_count = 0
    
        for encounter_id in training_encounters:
            enc_count = 0
            for file in encounters[encounter_id]:
                if(enc_count < encounter_size):
                    enc_count += 1
                    src_path = os.path.join(source_dir, file)
                    dst_path = os.path.join(dest_dir, "training", species_name, file)
                    shutil.copy2(src_path, dst_path)
                    train_count += 1
    
        for encounter_id in testing_encounters:
            enc_count = 0
            for file in encounters[encounter_id]:
                if(enc_count < encounter_size):
                    enc_count += 1
                    src_path = os.path.join(source_dir, file)
                    dst_path = os.path.join(dest_dir, "testing", species_name, file)
                    shutil.copy2(src_path, dst_path)
                    test_count += 1
    
        print(f"  Copied {train_count} files to training and {test_count} files to testing")
    
    print(f"Split complete. Data is now organized in {dest_dir}")