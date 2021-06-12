import visual as vi
from aggregator import *
from database import DatabaseWorker


class GetData:

    def __init__(self):
        self.data = list()
        self.df = list()
        self.graph_number = int()

        self.save_path = ''
        self.file_name = ''
        self.form = ''
        self.connection = DatabaseWorker()

    @staticmethod
    def checker(user_input):
        if user_input.isdigit():
            return True
        return False

    @staticmethod
    def print_df(df):
        if len(df) > 1:
            print('Текущие фреймы')
            for frame in df:
                print(frame)
        else:
            print('Текущий фрейм\n', df)

    def db_init(self):
        print('Инициализация базы данных')
        frame_count = input("Введите количество файлов ")
        if GetData.checker(frame_count):
            for _ in range(int(frame_count)):
                name = input('Введите название файла с данными: ')
                df = pd.read_csv(name)
                self.connection.insert(df, 'kiva_loans')

    def preprocess(self):
        frame_count = input("Введите количество датафреймов ")
        if GetData.checker(frame_count):
            for _ in range(int(frame_count)):
                name = input('Введите название таблицы: ')
                df = self.connection.select(table=name)
                # print(df)
                self.data.append(df)

        else:
            print("Введите число")
            return self.preprocess()

    def get_agg(self):
        # выбор фрейма
        frame_index = input('Введите номер фрейма для аггрегации: ')
        if GetData.checker(frame_index):
            df = self.data[int(frame_index) - 1]
        else:
            print("Введите число")
            return self.get_agg()

        # выбор колонок
        columns = input("Введите названия колонок через пробел: ").split()
        df = Aggregator.aggregate(data_frame=df, columns=columns)
        GetData.print_df(df)

        # выбор фильтра
        filt = input('Введите условие фильтра для определенной колонки: ')
        df = Aggregator.aggregate(data_frame=df, filter=filt)
        GetData.print_df(df)

        # выбор столбцов для группировки
        group_names = input("Введите названия столбцов для группировки через пробел: ").split()

        # False только для barplot_ и world_map, остальные - True
        as_index = bool(int(input("Столбец, по которому группировали в качестве индекса? (0 или 1) ")))

        df = Aggregator.aggregate(data_frame=df, group_name=group_names, as_index=as_index)
        GetData.print_df(df)

        # аггрегация
        column = input("Введите название колонки для аггрегации: ")
        funcs = input("Введите функцию для аггрегации: ")
        agg = {column: funcs}

        df = Aggregator.aggregate(data_frame=df, agg_name=agg)
        GetData.print_df(df)

        return df

    def get_save(self):
        # сохранение
        is_save = bool(int(input("Нужно ли сохранить график? (0 или 1) ")))
        if is_save:
            self.save_path = input('Введите полный путь для сохранения графика ')
            self.file_name = input('Введите название файла для сохранения: ')
            self.form = input('Введите формат сохранения ')

    def get_graph(self):
        self.graph_number = (input('''Какой тип графика вам нужен:
        1) barplot_
        2) stack_bar
        3) multi_bar
        4) hist_
        5) distributions\n'''))  # 6) world_map
        if GetData.checker(self.graph_number):
            self.graph_number = int(self.graph_number) - 1
        else:
            print('Введите число')
            return self.get_graph()

        if self.graph_number == 0:
            count_plot = int(input('''Введите количество полотен'''))
            data_col = list()

            print('''Введите столбцы, по которым будет группировка''')
            for cols in range(count_plot):
                names = input("Введите столбцы для группировки через пробел: ").split()
                data_col.append(names)

            return data_col

        elif self.graph_number == 3 or self.graph_number == 4:
            value = input('Введите ключевое значение: ')
            return value

    def insert_data(self, cols, values, name):
        val = values.split(",")
        col = cols.split(",")
        self.df.append(dict(zip(col, val)))
        self.connection.insert(pd.DataFrame(self.df), name)

    def save_df(self):
        print('''Сохранить ли данные в базе данных 0 или 1''')
        value = int(input('Введите ключевое значение: '))
        if value == 1:
            print('''Сохранить как файл или ввести вручную?''')
            value = input('Введите ключевое значение файл или вручную: ')
            if value == 'файл':
                print('''Введите название файла''')
                file = input('Введите ключевое значение файл или вручную: ')
                self.connection.insert_from_csv(file)
            else:
                print('''Введите имя таблицы''')
                name = input('Введите ключевое значение файл или вручную: ')
                print('''Введите имена колонок''')
                cols = input('Введите ключевое значение файл или вручную: ')
                print('''Введите данные или Exit для выхода''')
                while True:
                    values = input('Введите ключевое значение файл или вручную: ')
                    if values == 'exit':
                        return None
                    self.insert_data(cols, values, name)


analysis = GetData()

analysis.db_init()
analysis.preprocess()
df = analysis.get_agg()
params = analysis.get_graph()
analysis.get_save()
visualisator = vi.Visual(df=df, graph_number=analysis.graph_number,
                         save_path=analysis.save_path, file_name=analysis.file_name, form=analysis.form)

visualisator.run(params)


analysis.save_df()

