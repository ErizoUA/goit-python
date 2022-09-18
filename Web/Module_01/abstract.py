from abc import ABC, abstractmethod
import json
import pickle


class SerializationInterface(ABC):

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def restore(self):
        pass


class JsonData(SerializationInterface):

    def save(self, data):
        with open('db.json', 'w') as file_db:
            json.dump(data, file_db)
            print('db has been saved successfully')

    def restore(self):
        with open('db.json', 'r') as file_db:
            data = json.load(file_db)


class BinData(SerializationInterface):

    def save(self, data):
        with open('db.bin', 'wb') as file_db:
            pickle.dump(data, file_db)
            print('db has been saved successfully')

    def restore(self):
        with open('db.bin', 'rb') as file_db:
            data = pickle.load(file_db)
