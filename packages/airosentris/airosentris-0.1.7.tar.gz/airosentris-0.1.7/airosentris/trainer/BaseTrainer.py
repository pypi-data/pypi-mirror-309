from abc import ABC, abstractmethod


class BaseTrainer(ABC):
    @abstractmethod
    def train(self, data, labels):
        pass

    @abstractmethod
    def evaluate(self, test_data, test_labels):
        pass

    @abstractmethod
    def save_model(self, file_path):
        pass

    @abstractmethod
    def load_model(self, file_path):
        pass
