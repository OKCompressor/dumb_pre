import logging
from dumb_pre_v2 import transform_text, restore_text, debug_compare_texts

def main():
    input_file = '/media/zen/data/backup/Zen/IT/2024/_ UPGRADE IT/data/enwik8'  # Your input file path
    dict_file = 'dictionary.txt'  # Your dictionary file path
    sorted_dict_file = 'sorted_dictionary.txt'  # Your sorted dictionary file path
    output_file = 'output.txt'  # Your transformed text file path
    reconstructed_file = 'reconstructed.txt'  # Your reconstructed text file path

    # Transform the text
    transform_text(input_file, dict_file, sorted_dict_file, output_file)

    # Read the original text
    with open(input_file, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Restore the text
    reconstructed_text = restore_text(dict_file, output_file, reconstructed_file)
    
    # Debugging output to peek at the original and reconstructed texts
    logging.debug(f"Original text snippet: {original_text[:100]}")
    logging.debug(f"Reconstructed text snippet: {reconstructed_text[:100]}")
    
    # Assertion to check if the original and reconstructed texts match
    try:
        assert original_text == reconstructed_text, "The reconstructed text does not match the original text."
    except AssertionError as e:
        logging.error(e)
        debug_compare_texts(original_text, reconstructed_text)
        raise

    logging.info("Assertion passed. The reconstructed text matches the original text.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
