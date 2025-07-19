"""
python redumb_cats.py \
  --input /home/derv/oComp/beta_v2/cc_nlp/output/cat0_uniqs.txt \
  --dict cat0_dict.txt \
  --sorted_dict cat0_sorted_dict.txt \
  --output cat0_output.txt \
  --reconstructed cat0_reconstructed.txt

"""

import argparse
import logging
from dumb_pre_v2 import DumbPreprocessor

def main():
    parser = argparse.ArgumentParser(description="Funnel cat0 uniqs through dumb pipeline")
    parser.add_argument("--input", required=True, help="Input text file (e.g., cat0_uniqs.txt)")
    parser.add_argument("--dict", default="dictionary.txt", help="Dictionary file to use")
    parser.add_argument("--sorted_dict", default="sorted_dictionary.txt", help="Sorted dictionary file")
    parser.add_argument("--output", default="output.txt", help="Transformed output text")
    parser.add_argument("--reconstructed", default="reconstructed.txt", help="Restored output text")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    pre = DumbPreprocessor()

    # Transform the text
    pre.transform_text(args.input, args.dict, args.sorted_dict, args.output)

    # Read the original text
    with open(args.input, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Restore the text
    reconstructed_text = pre.restore_text(args.dict, args.output, args.reconstructed)
    
    # Debug: Compare
    logging.debug(f"Original snippet: {original_text[:100]}")
    logging.debug(f"Reconstructed snippet: {reconstructed_text[:100]}")

    # If implemented as method on the class:
    # pre.debug_compare_texts(original_text, reconstructed_text)

    # Assertion
    if original_text != reconstructed_text:
        logging.error("Reconstructed text does not match original!")
        # Try both possibilities:
        try:
            pre.debug_compare_texts(original_text, reconstructed_text)
        except AttributeError:
            # fallback if it's still a free function
            from dumb_pre_v2 import debug_compare_texts
            debug_compare_texts(original_text, reconstructed_text)
        raise AssertionError("Mismatch between original and reconstructed text.")
    else:
        logging.info("Assertion passed. The reconstructed text matches the original.")

if __name__ == "__main__":
    main()
