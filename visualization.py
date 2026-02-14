import matplotlib.pyplot as plt
import seaborn as sns

def plot_trip_counts(df):
    """Гистограмма по ключевым категориям (Районы или Зоны)"""
    # Ищем колонки с ID зон (часто бывают в новых данных NYC)
    target_col = None
    for col in ['PULocationID', 'Borough', 'VendorID']:
        if col in df.columns:
            target_col = col
            break
            
    if target_col:
        plt.figure(figsize=(12, 6))
        sns.countplot(data=df, x=target_col, palette='viridis')
        plt.title(f'Количество поездок по категории: {target_col}')
        plt.xticks(rotation=45)
        plt.show()
    else:
        print("Подходящие колонки для категорий не найдены.")

def plot_trip_distances(df):
    """Распределение дистанций поездок"""
    col = 'trip_distance'
    if col in df.columns:
        plt.figure(figsize=(10, 5))
        # Ограничим до 20 миль, чтобы убрать выбросы и увидеть график
        sns.histplot(df[df[col] < 20][col], bins=30, kde=True, color='orange')
        plt.title('Распределение дистанций поездок (до 20 миль)')
        plt.xlabel('Миля')
        plt.show()

def plot_route_heatmap(df):
    """Строит тепловую карту перемещений между районами/зонами"""
    cols = ['PULocationID', 'DOLocationID']
    if all(c in df.columns for c in cols):
        # Выбираем топ-10 популярных зон отправления, чтобы график был читаемым
        top_zones = df['PULocationID'].value_counts().head(10).index
        subset = df[df['PULocationID'].isin(top_zones) & df['DOLocationID'].isin(top_zones)]
        
        # Создаем таблицу сопряженности (Pivot table)
        route_matrix = pd.crosstab(subset['PULocationID'], subset['DOLocationID'])
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(route_matrix, annot=True, fmt="d", cmap="YlGnBu")
        plt.title('Топ-10 маршрутов: Откуда (PULocationID) -> Куда (DOLocationID)')
        plt.xlabel('Зона прибытия')
        plt.ylabel('Зона отправления')
        plt.show()
    else:
        print("Колонки PULocationID или DOLocationID не найдены.")

def plot_top_zones(df):
    """Показывает топ-20 самых популярных зон (мест) посадки"""
    # Ищем колонку с названием Zone
    col = None
    for c in ['PULocationID_Name', 'pickup_zone', 'Zone', 'Location']:
        if c in df.columns:
            col = c
            break
    
    if col:
        plt.figure(figsize=(12, 8))
        # Считаем количество поездок для каждой зоны и берем топ-20
        top_20 = df[col].value_counts().head(20)
        sns.barplot(x=top_20.values, y=top_20.index, palette='coolwarm')
        plt.title(f'Топ-20 самых популярных зон (по колонке {col})')
        plt.xlabel('Количество поездок')
        plt.ylabel('Название зоны')
        plt.show()
    else:
        print(f"Колонка с зонами не найдена. Доступные колонки: {df.columns.tolist()}")
from matplotlib.ticker import MaxNLocator

def plot_top_zones_fixed(df):
    """График с целыми числами на шкале X"""
    col = 'Zone' # Используем вашу колонку Zone
    
    if col in df.columns:
        plt.figure(figsize=(12, 8))
        top_zones = df[col].value_counts().head(20)
        
        ax = sns.barplot(x=top_zones.values, y=top_zones.index, palette='coolwarm')
        
        # Устанавливаем ТОЛЬКО целые числа на шкале X
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.title(f'Топ-20 зон по количеству поездок')
        plt.xlabel('Количество поездок (целые числа)')
        plt.ylabel('Название зоны')
        plt.grid(axis='x', linestyle='--', alpha=0.7) # Добавим сетку для удобства
        plt.show()
    else:
        print("Колонка Zone не найдена")

def plot_trip_length_by_borough(df):
    """Сравнивает длину поездок (shape_length) по районам (Borough)"""
    if 'shape_length' in df.columns and 'Borough' in df.columns:
        plt.figure(figsize=(14, 8))
        
        # Строим график. Фильтруем слишком длинные значения (выбросы), чтобы график был читаемым
        # Например, берем только 95% самых частых поездок
        q_high = df['shape_length'].quantile(0.95)
        df_filtered = df[df['shape_length'] < q_high]
        
        sns.boxplot(data=df_filtered, x='Borough', y='shape_length', palette='Set2')
        
        plt.title('Распределение длины поездок по районам Нью-Йорка')
        plt.xlabel('Район')
        plt.ylabel('Длина пути (shape_length)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.show()
    else:
        print(f"Колонки не найдены. В наличии: {df.columns.tolist()}")

def plot_trip_length_by_borough_fixed(df):
    """Сравнивает длину поездок по районам (с учетом регистра имен колонок)"""
    # Используем точные названия из вашего списка
    length_col = 'Shape Length'
    borough_col = 'Borough'
    
    if length_col in df.columns and borough_col in df.columns:
        plt.figure(figsize=(14, 8))
        
        # Строим график, отсекая экстремально длинные значения для наглядности
        q_high = df[length_col].quantile(0.95)
        df_filtered = df[df[length_col] < q_high]
        
        sns.barplot(data=df_filtered, x=borough_col, y=length_col, palette='viridis', ci=None)
        
        plt.title('Средняя длина пути по районам Нью-Йорка')
        plt.xlabel('Район (Borough)')
        plt.ylabel('Длина (Shape Length)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.show()
    else:
        print(f"Ошибка! Проверьте колонки. В наличии: {df.columns.tolist()}")
import plotly.express as px

def plot_interactive_treemap(df):
    """Интерактивная карта: иерархия Район -> Зона по площади"""
    fig = px.treemap(
        df, 
        path=[px.Constant("Нью-Йорк"), 'Borough', 'Zone'], 
        values='Shape Area',
        color='Borough',
        title='Иерархия районов и зон по занимаемой площади (Shape Area)',
        hover_data=['Shape Length']
    )
    fig.update_traces(root_color="lightgrey")
    fig.show()

def plot_interactive_bubble(df):
    """Пузырьковая диаграмма: Площадь vs Длина с выбором зон"""
    fig = px.scatter(
        df, 
        x="Shape Area", 
        y="Shape Length",
        size="Shape Area", 
        color="Borough",
        hover_name="Zone", 
        log_x=True, 
        size_max=60,
        title='Сравнение зон: Площадь vs Периметр (Интерактивно)'
    )
    fig.show()
