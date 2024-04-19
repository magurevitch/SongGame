from src.DataUsers.DataUser import DataUser

class GameManager(DataUser):
    def reset_tables(self):
        self.data_store.reset_tables()

    def start_game(self, prompt: str):
        return self.data_store.start_new_game(prompt)