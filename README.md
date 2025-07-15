# OKC Dumb Tokenizer (okc-dumb_pre)

The reference implementation for word-level, reversible text tokenization and compression—  
serving as the open, auditable baseline for the OKCompressor pipeline.

---

## What is this?

A minimal, readable Python toolkit that:
- Tokenizes raw text at the word level
- Compresses by mapping each unique word to an integer (dictionary encoding)
- Restores the original text perfectly (full round-trip)
- Benchmarks against industry standards (e.g., tiktoken)
- Publishes all benchmark results for verification and collaboration

---

## Why?

Too many modern NLP and LLM tokenizers are “black boxes.”  
OKC Dumb Tokenizer sets the baseline for open, fully auditable text preprocessing—so everyone can see, verify, and build on our results.

- **Transparent**: No hidden steps, 100% reproducible
- **Collaborative**: Designed for research, extension, and real-world testing
- **Comparable**: Benchmarked directly against OpenAI tiktoken (and others)

---

## How does it work?

1. **Transform:** Reads text, splits to words, creates a dictionary, encodes the text as integer IDs.
2. **Restore:** Uses the dictionary and IDs to reconstruct the exact original text.
3. **Benchmark:** Measures token count, compression size, time, and correctness; outputs results as CSV.

---

## Quick Start

```bash
git clone https://github.com/OKCompressor/dumb_pre.git
cd dumb_pre
pip install -r requirements.txt

# Place your test corpus in ./data/ (e.g., enwik8)
python bench_dumb.py


```

Results will appear in benchmark_results/ as CSV for easy review and sharing.

## Example Results (enwik8)

| Method     | Gzipped Size (MB) | Unique Tokens | Round-trip Lossless |
|------------|-------------------|---------------|---------------------|
| dumb_pre   | 36.7              | 424,268       | ✅ True             |
| tiktoken   | 37.0              | 71,161        | ✅ True             |

---

## Roadmap

- Rust implementation (target: 10x faster)
- Binary and advanced output layers
- Multi-lingual and character-level tokenization
- Integration as a default layer in OKCompressor

---

## About OKCompressor

OKCompressor is a collective for open, benchmarked, and collaborative corpus compression tech.

- [github.com/OKCompressor](https://github.com/OKCompressor)
- Collaboration, feedback, and forks are welcomed!

---

*Transparency is the new baseline. Benchmarks are public. The journey is open.*

