from abc import ABC, abstractmethod
import json
import pickle


class SerializationInterface(ABC):

    @abstractmethod
    def save(self, data):
        pass


class JsonData(SerializationInterface):

    def save(self, data):
        with open('db.json', 'w') as json_db:
            json.dump(data, json_db)
            print('db has been saved successfully')


class BinData(SerializationInterface):

    def save(self, data):
        with open('db.bin', 'wb') as bin_db:
            pickle.dump(data, bin_db)
            print('db has been saved successfully')
