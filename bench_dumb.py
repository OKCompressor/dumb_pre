import os
import glob
import time
import pandas as pd
from dumb_pre_v2 import DumbPreprocessor  # see below for this class
import logging

DATASET_PATH = './data/'
OUTPUT_PATH = './benchmark_results_dumb/'
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Glob all enwik* files in data/
dataset_files = sorted(glob.glob(os.path.join(DATASET_PATH, 'enwik*')))
DATASETS = {os.path.basename(f): f for f in dataset_files}

logging.basicConfig(level=logging.INFO)

results = []

# Use a concrete implementation of Preprocessor
pre = DumbPreprocessor()

for name, path in DATASETS.items():
    logging.info(f"Processing {name} ...")

    # Files for intermediate outputs
    dict_file = os.path.join(OUTPUT_PATH, f"{name}_dict.txt")
    sorted_dict_file = os.path.join(OUTPUT_PATH, f"{name}_sorted_dict.txt")
    output_file = os.path.join(OUTPUT_PATH, f"{name}_output.txt")
    reconstructed_file = os.path.join(OUTPUT_PATH, f"{name}_reconstructed.txt")

    # --- Step 1: Transform/Compress ---
    t0 = time.time()
    pre.transform_text(path, dict_file, sorted_dict_file, output_file)
    t_transform = time.time() - t0

    # --- Step 2: Restore/Decompress ---
    t0 = time.time()
    _ = pre.restore_text(dict_file, output_file, reconstructed_file)
    t_restore = time.time() - t0

    # --- Step 3: Unique tokens, sizes ---
    with open(dict_file, 'r', encoding='utf-8') as f:
        vocab = [line.rstrip('\n') for line in f]
    uniq_tokens = len(vocab)

    raw_size = os.path.getsize(path)
    output_size = os.path.getsize(output_file)
    reconstructed_size = os.path.getsize(reconstructed_file)

    # --- Step 4: Check round-trip correctness ---
    with open(path, 'r', encoding='utf-8') as f:
        original_text = f.read()
    with open(reconstructed_file, 'r', encoding='utf-8') as f:
        restored_text = f.read()
    match = original_text == restored_text

    results.append({
        'Dataset': name,
        'Raw Size (MB)': round(raw_size/(1024*1024),2),
        'Compressed Size (MB)': round(output_size/(1024*1024),2),
        'Reconstructed Size (MB)': round(reconstructed_size/(1024*1024),2),
        'Unique Tokens': uniq_tokens,
        'Transform Time (s)': round(t_transform, 2),
        'Restore Time (s)': round(t_restore, 2),
        'Correct Roundtrip': match,
    })

# Save results
df = pd.DataFrame(results)
print(df.to_markdown(index=False))
df.to_csv(os.path.join(OUTPUT_PATH, 'dumb_benchmark_results.csv'), index=False)
print(f"Benchmark complete. Results in {OUTPUT_PATH}")

