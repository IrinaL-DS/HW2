import pandas as pd

class DataLoader:
    def __init__(self, url):
        self.url = url
        self.df = None

    def load_data(self):
        """Загрузка данных из NYC Open Data"""
        self.df = pd.read_csv(self.url)
        return self.df

    def get_summary(self):
        """Возвращает краткую информацию о базе"""
        if self.df is not None:
            return self.df.info()
        return "Данные еще не загружены"from google.colab import sheets
sheet = sheets.InteractiveSheet(df=df)
