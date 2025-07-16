import os
import glob
import time
import pandas as pd
from dumb_pre_v2 import DumbPreprocessor
import logging
import gzip
import shutil

DATASET_PATH = './data/'
OUTPUT_PATH = './benchmark_results_dumb/'
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Find enwik* files
dataset_files = sorted(glob.glob(os.path.join(DATASET_PATH, 'enwik*')))
DATASETS = {os.path.basename(f): f for f in dataset_files}

logging.basicConfig(level=logging.INFO)

results = []

pre = DumbPreprocessor()

for name, path in DATASETS.items():
    logging.info(f"Processing {name} ...")

    # Output paths
    dict_file = os.path.join(OUTPUT_PATH, f"{name}_dict.txt")
    sorted_dict_file = os.path.join(OUTPUT_PATH, f"{name}_sorted_dict.txt")
    output_file = os.path.join(OUTPUT_PATH, f"{name}_output.txt")
    reconstructed_file = os.path.join(OUTPUT_PATH, f"{name}_reconstructed.txt")
    gzipped_file = os.path.join(OUTPUT_PATH, f"{name}_dumb.gz")

    # Transform/Compress
    t0 = time.time()
    pre.transform_text(path, dict_file, sorted_dict_file, output_file)
    t_transform = time.time() - t0

    # Restore/Decompress
    t0 = time.time()
    _ = pre.restore_text(dict_file, output_file, reconstructed_file)
    t_restore = time.time() - t0

    # Unique tokens, sizes
    with open(dict_file, 'r', encoding='utf-8') as f:
        vocab = [line.rstrip('\n') for line in f]
    uniq_tokens = len(vocab)

    raw_size = os.path.getsize(path)
    output_size = os.path.getsize(output_file)
    reconstructed_size = os.path.getsize(reconstructed_file)

    # --- Gzip both files together for optimal compression ---
    gzipped_merged_file = os.path.join(OUTPUT_PATH, f"{name}_merged.gz")
    with gzip.open(gzipped_merged_file, 'wb') as gz_out:
        with open(dict_file, 'rb') as f1:
            shutil.copyfileobj(f1, gz_out)
            gz_out.write(b'\n')
        with open(output_file, 'rb') as f2:
            shutil.copyfileobj(f2, gz_out)
    compressed_merged_size = os.path.getsize(gzipped_merged_file)

    # --- Gzip each file separately ---
    gzipped_dict_file = os.path.join(OUTPUT_PATH, f"{name}_dict.txt.gz")
    gzipped_output_file = os.path.join(OUTPUT_PATH, f"{name}_output.txt.gz")
    with open(dict_file, 'rb') as f_in, gzip.open(gzipped_dict_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    with open(output_file, 'rb') as f_in, gzip.open(gzipped_output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    compressed_dict_size = os.path.getsize(gzipped_dict_file)
    compressed_output_size = os.path.getsize(gzipped_output_file)
    compressed_separate_size = compressed_dict_size + compressed_output_size



    # Round-trip check
    with open(path, 'r', encoding='utf-8') as f:
        original_text = f.read()
    with open(reconstructed_file, 'r', encoding='utf-8') as f:
        restored_text = f.read()
    match = original_text == restored_text

    results.append({
        'Dataset': name,
        'Raw Size (MB)': round(raw_size/(1024*1024),2),
        'Output Size (MB)': round(output_size/(1024*1024),2),
        'Gzip Merged (MB)': round(compressed_merged_size/(1024*1024),2),
        'Gzip Dict (MB)': round(compressed_dict_size/(1024*1024),2),
        'Gzip Output (MB)': round(compressed_output_size/(1024*1024),2),
        'Gzip Sep. Sum (MB)': round(compressed_separate_size/(1024*1024),2),
        'Reconstructed Size (MB)': round(reconstructed_size/(1024*1024),2),
        'Unique Tokens': uniq_tokens,
        'Transform Time (s)': round(t_transform, 2),
        'Restore Time (s)': round(t_restore, 2),
        'Correct Roundtrip': match,
    })


df = pd.DataFrame(results)
print(df.to_markdown(index=False))
df.to_csv(os.path.join(OUTPUT_PATH, 'dumb_benchmark_results.csv'), index=False)
print(f"Benchmark complete. Results in {OUTPUT_PATH}")


