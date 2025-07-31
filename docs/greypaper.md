# dumb_pre

**Idiot-Proof, Fully Reversible Tokenizer & Preprocessor**  
_by OKCompressor Labs — 2024_

---

## Abstract

Modern tokenizers (like tiktoken or SentencePiece) are clever but complex, often introducing opacity, language bias, or hard-to-debug edge cases. **dumb_pre** takes the opposite approach:  
It is a minimalist, fully reversible tokenizer and preprocessor.  
- **Every unique input sequence gets a unique integer index via an explicit, readable dictionary.**
- **No “smart” NLP or language awareness happens at this stage.**  
- **Lossless by design:** roundtripping always restores your original data.

**dumb_pre** is the stage-zero of a modular text pipeline. Advanced NLP (clustering, semantic merges, etc) is explicitly deferred to later stages—making dumb_pre the perfect, auditable foundation.

---

## Features

- **Fully reversible:** Never lose a byte. Special handling for all whitespace, newlines, tabs, non-ASCII (via base64).
- **Explicit dictionary:** Saved as plain text for analysis, debugging, or further processing.
- **No language tricks:** Not BPE, not wordpiece, not even Unicode-savvy—just pure, auditable mapping.
- **Pipeline ready:** Output dictionary/tokens are intended for downstream tools (like [OKCompressor](https://github.com/OKCompressor)) or for later NLP processing.
- **Idiot simple:** Read the code, see exactly what happens.

---

## Why No NLP Yet?

dumb_pre is intentionally *not* smart. It’s a preprocessor that guarantees nothing is lost or mangled before any “clever” or language-aware steps. All true NLP (token merging, clustering, etc.) happens **after** dumb_pre, never before.

---

## Benchmarks

| Dataset | Raw Size (MB) | dumb_pre Output (MB) | Gzip Output (MB) | Unique Tokens | Time (s) | tiktoken IDs Size (MB) | tiktoken Gzipped IDs (MB) | tiktoken Unique Tokens | tiktoken Tokenize Time (s) |
|---------|---------------|----------------------|------------------|--------------|----------|------------------------|---------------------------|-----------------------|---------------------------|
| enwik7  | 9.54          | 13.52                | 3.19             | 97,485       | 2.92     | 10.05                  | 3.58                      | 50,500                | 1.41                      |
| enwik8  | 95.37         | 133.52               | 32.2             | 424,268      | 88.39    | 98.39                  | 35.06                     | 71,161                | 25.9                      |

*Roundtrip always succeeds. dumb_pre may use more unique tokens, but gzip output is similar or even better than tiktoken, and all data is recoverable.*

---

## Usage

```bash
python dumb_pre.py --input file.txt --dict dict.txt --out output.ids [--restore --restore_out file.restored.txt]
````

* Outputs: integer token IDs, explicit dictionary, and (optionally) restored roundtrip file.
* The dictionary can be further processed by OKCompressor or any custom NLP layer.

---

## Minimal Code Example

```python
class DumbPreprocessor:
    def tokenize_text(self, text):
        tokens = ... # explicit handling, see full code
        dictionary = {token: i for i, token in enumerate(tokens)}
        ids = [dictionary[token] for token in tokens]
        return ids, dictionary
    # ...full roundtrip and special character handling in repo
```

---

## Design Philosophy

* **Transparency:** If a bug appears, you can see exactly where.
* **Reproducibility:** Provides a gold standard baseline for comparison against “smart” tokenizers.
* **Modularity:** Use as a safe, lossless first step in any pipeline.
* **Hacker-friendly:** Read, modify, or port in minutes.

---

## Pipeline Overview

1. **Preprocess with dumb\_pre:**

   * Lossless, dictionary-driven tokenization.
2. **(Later) NLP / Semantic Layer:**

   * Smart merges, language modeling, deduplication, etc.
3. **(Optional) Further Compression or ML Modeling:**

   * Use with OKCompressor or any downstream tool.

---

## Summary Table

| Property            | dumb\_pre          | tiktoken        |
| ------------------- | ------------------ | --------------- |
| Reversible          | Yes                | Not always      |
| Explicit Dictionary | Yes (plain text)   | No (internal)   |
| Handles all Unicode | Yes (b64 fallback) | Partial/complex |
| Opaque merges?      | None               | Yes             |
| Language-aware?     | No (by design)     | Yes             |
| Pipeline-ready?     | Yes                | Not modular     |

---

## License

(Copyleft for humans, paid for AI/corporate extractors.)

---

> Sometimes, being “dumb” is the smartest way to guarantee zero-loss, reproducible, and hackable pipelines for text, data, and AI.

For further integration, see [OKCompressor](https://github.com/OKCompressor) for advanced processing and NLP.

---
