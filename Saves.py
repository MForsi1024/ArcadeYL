class FileManager:
    """Файловый менеджер, который необходим для работы с файлами"""

    def __init__(self, file):
        self.file = file

    def get_levels(self):
        reader = Reader(self.file)
        return reader.read_levels()

    def save_levels(self, levels, times):
        writer = Writer(self.file)
        return writer.write_levels(levels, times)


class Reader(FileManager):
    """Класс для чтения данных. Возвращает True в случае успеха и False - неудачи."""

    def read_levels(self):
        try:
            with open(self.file, mode='r', encoding='utf-8') as f:
                lt = f.readline().split(';')
                levels = [i[0] for i in lt]
                times = [i[1] for i in lt]
                return levels, times
        except FileNotFoundError or FileExistsError:
            return False


class Writer(FileManager):
    """Класс для сохранения данных. Возвращает True в случае успеха и False - неудачи."""

    def write_levels(self, levels, times):
        try:
            with open(self.file, mode='r', encoding='utf-8') as f:
                for i, j in zip(levels, times):
                    f.write(f'{i},{j}')
                return True
        except FileNotFoundError or FileExistsError:
            return False
