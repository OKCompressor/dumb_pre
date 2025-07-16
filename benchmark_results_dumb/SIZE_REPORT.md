# OKC Dumb Tokenizer – enwik8 Output File Sizes

| File                   | Size (bytes) | Size (MB) | Description                                  |
|------------------------|--------------|-----------|----------------------------------------------|
| enwik8_dict.txt        |   3,784,920  |   3.8     | Dictionary: one word/token per line          |
| enwik8_dict.txt.gz     |   2,054,373  |   2.1     | Gzipped dictionary                          |
| enwik8_output.txt      | 140,006,093  | 140.0     | Encoded token indices (plain text)           |
| enwik8_output.txt.gz   |  33,760,568  | 33.8      | Gzipped output indices                      |
| enwik8_merged.gz       |  35,815,744  | 35.8      | Gzipped (dict + output) [optimal]            |
| enwik8_dumb.gz         |  35,815,742  | 35.8      | (Legacy, should match merged.gz)             |
| enwik8_dumb_lvl9.gz    |  35,815,742  | 35.8      | (Gzip, level 9)                              |
| enwik8_reconstructed.txt |100,000,000 | 100.0     | Restored original text                       |
| enwik8_sorted_dict.txt |   3,784,920  |   3.8     | Dictionary (sorted variant)                  |

**Notes:**
- `enwik8_merged.gz` is the optimal compressed output (dict + output concatenated then gzipped).
- All files generated from the same enwik8 run, reproducible via [bench_dumb.py](../bench_dumb.py).
- All results use Python’s built-in gzip, level 9 compression.


