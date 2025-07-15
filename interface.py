from abc import ABC, abstractmethod

class Preprocessor(ABC):
    @abstractmethod
    def transform_text(self, input_file, dict_file, sorted_dict_file, output_file):
        pass

    @abstractmethod
    def restore_text(self, dict_file, output_file, reconstructed_file):
        pass
