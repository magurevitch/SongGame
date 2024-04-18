from src.DataStore import DataStore

class DataUser:
    def __init__(self, is_test=False):
        self.data_store = DataStore(is_test)