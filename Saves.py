class Saves:
    pass


class FileManager:
    """Файловый менеджер, который необходим для работы с файлами"""
    def __init__(self, file):
        self.file = file


class Reader(FileManager):
    def read_levels(self):
        with open(self.file, mode='r', encoding='utf-8') as f:
            pass
class Writer(FileManager):
    def save_levels(self, levels, times):
        try:
            with open(self.file, mode='r', encoding='utf-8') as f:
                for i, j in zip(levels, times):
                    f.write(f'{i},{j}')
                return True
        except FileNotFoundError or FileExistsError:
            return False

