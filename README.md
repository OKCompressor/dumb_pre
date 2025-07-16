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

# 🚀 OKC Dumb Tokenizer: Reference Implementation & Benchmarks Released

We’re excited to share the **first open-source reference for word-level, reversible tokenization and compression**—the new baseline for [OKCompressor](https://github.com/OKCompressor).

---

## 🔍 Why does this matter?

Most tokenizers and compressors used in LLM pipelines are closed-source or difficult to audit.  
**OKC Dumb Tokenizer** is fully open, reproducible, and delivers real numbers:

| Method     | Gzipped Size (MB) | Unique Tokens | Round-trip Lossless |
|------------|-------------------|---------------|---------------------|
| dumb_pre   | 35.8              | 424,268       | ✅ True             |
| tiktoken   | 37.0              | 71,161        | ✅ True             |

*(enwik8, gzip compressed)*

## 📊 Benchmark Results

- [Raw CSV benchmark results](benchmark_results_dumb/dumb_benchmark_results.csv)
- [Size report with all output files](benchmark_results_dumb/SIZE_REPORT.md)

---

## 🛠️ Features

- **Python-based, minimal, and readable**
- 100% round-trip guarantee
- Benchmark scripts and public CSV results included
- Easy to extend, fork, or integrate

---

## 📈 Roadmap

- [ ] Rust implementation (aiming for 10x speed)
- [ ] Binary output & advanced layers
- [ ] Multi-lingual and character tokenization
- [ ] Seamless integration with OKCompressor suite

---

## 🤝 Join Us!

- Try it out, fork, open an issue, or suggest a feature.
- Looking for collaborators, researchers, and partners—especially for the next-gen Rust build and real-world testing.

**Transparency is the new baseline. Benchmarks are public. The journey is open.**

[github.com/OKCompressor/dumb_pre](https://github.com/OKCompressor/dumb_pre)

