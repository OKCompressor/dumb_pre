import re
import logging
import base64
from interface import Preprocessor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')


import argparse

class DumbPreprocessor(Preprocessor):
    TAB_TOKEN = "\u0001"  # Using a non-printable character as the token
    SPACE_TOKEN = "\u0002"  # Using a non-printable character as the token
    NEWLINE_PLACEHOLDER = "\u0003"  # Using a non-printable character as the token
    CHAR_THRESHOLD = 0x7F  # Standard ASCII range
    B64_PREFIX = "\u0004"
    B64_SUFFIX = "\u0005"

    def transform_text(self, input_file, dict_file, sorted_dict_file, output_file):
        text = self.read_input_file(input_file)
        text = self.replace_special_chars(text)
        tokens = self.tokenize_text(text)
        dictionary = self.create_dictionary(tokens)
        transformed_text = self.replace_tokens_with_indices(tokens, dictionary)
        self.save_transformed_text(transformed_text, output_file)
        self.save_dictionary(dictionary, dict_file)
        # self.save_sorted_dictionary(dictionary, sorted_dict_file)

        return transformed_text

    def restore_text(self, dict_file, output_file, reconstructed_file):
        original_text = self.reverse_process(dict_file, output_file, reconstructed_file)
        return original_text

    @staticmethod
    def read_input_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def replace_special_chars(self, text):
        def replace_char(match):
            char = match.group(0)
            char_code = ord(char)
            if char_code > self.CHAR_THRESHOLD:  # Non-ASCII characters
                encoded = base64.b64encode(char.encode('utf-8')).decode('utf-8')
                return f"{self.B64_PREFIX}{encoded}{self.B64_SUFFIX}"
            return char

        text = re.sub(r'[^\x00-\x7F]', replace_char, text)
        text = text.replace('\n', self.NEWLINE_PLACEHOLDER)
        text = text.replace('\t', self.TAB_TOKEN)
        text = re.sub(r' {2,}(?!\d)', lambda m: f"{self.SPACE_TOKEN}{len(m.group(0))}{self.SPACE_TOKEN}", text)
        return text

    def tokenize_text(self, text):
        tokens = re.findall(r'\d+|\w+|&[a-z]+;|[^\w\s]|\u0004[A-Za-z0-9+/=]+\u0005|\u0001|\u0002\d+\u0002|\u0003| ', text)
        return tokens

    def create_dictionary(self, tokens):
        unique_tokens = list(dict.fromkeys(tokens))  # Preserve order and remove duplicates
        dictionary = {token: index for index, token in enumerate(unique_tokens)}
        return dictionary

    def replace_tokens_with_indices(self, tokens, dictionary):
        return [dictionary[token] for token in tokens]

    def save_dictionary(self, dictionary, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for token in dictionary.keys():
                file.write(f"{token}\n")

    def save_sorted_dictionary(self, dictionary, file_path):
        sorted_tokens = sorted(dictionary.keys())
        with open(file_path, 'w', encoding='utf-8') as file:
            for token in sorted_tokens:
                file.write(f"{token}\n")

    def save_transformed_text(self, transformed_text, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(' '.join(map(str, transformed_text)))

    def reverse_process(self, dict_file, output_file, reconstructed_file):
        dictionary = self.load_dictionary(dict_file)
        transformed_text = self.read_data_from_file(output_file)
        original_text = self.reconstruct_text(transformed_text, dictionary)
        original_text = self.restore_special_chars(original_text)
        self.save_data_to_file(original_text, reconstructed_file)
        return original_text

    @staticmethod
    def load_dictionary(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return {index: line for index, line in enumerate(lines)}

    @staticmethod
    def read_data_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = list(map(int, file.read().split()))
        return data

    def reconstruct_text(self, transformed_text, dictionary):
        reconstructed_text = ''.join(dictionary.get(index, "�") for index in transformed_text)
        return reconstructed_text

    def restore_special_chars(self, text):
        def restore_char(match):
            encoded = match.group(1)
            padding = '=' * (-len(encoded) % 4)  # Add padding if necessary
            try:
                decoded = base64.b64decode(encoded + padding).decode('utf-8')
                return decoded
            except (ValueError, UnicodeDecodeError) as e:
                logging.error("Error decoding base64 character %s: %s", encoded, e)
                return "�"  # Unicode replacement character

        text = re.sub(rf'{self.B64_PREFIX}([A-Za-z0-9+/=]+){self.B64_SUFFIX}', restore_char, text)
        text = text.replace(self.NEWLINE_PLACEHOLDER, '\n')
        text = text.replace(self.TAB_TOKEN, '\t')
        text = re.sub(rf'{self.SPACE_TOKEN}(\d+){self.SPACE_TOKEN}', lambda m: ' ' * int(m.group(1)), text)
        return text

    @staticmethod
    def save_data_to_file(data, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
        logging.info("Data written to %s", file_path)








def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--dict", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--sorted_dict", default=None)
    parser.add_argument("--restore", action="store_true", help="Restore/roundtrip output as check")
    parser.add_argument("--restore_out", default=None, help="Where to write restored text if --restore")
    args = parser.parse_args()

    pre = DumbPreprocessor()
    pre.transform_text(args.input, args.dict, args.sorted_dict or args.dict, args.out)
    if args.restore:
        out_restored = args.restore_out or (args.out + ".restored.txt")
        pre.restore_text(args.dict, args.out, out_restored)

if __name__ == "__main__":
    main()
