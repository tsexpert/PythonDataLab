'''
Лабораторные работы 1 + 2
'''

# Глобальные переменные
urlprov = "Provinces.xlsx"
# Для нашей работы берем данные за 10 лет: с 2007 по 2017
urlmean = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&year1=2007&year2=2017&type=Mean&provinceID="
urlparea = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&year1=2007&year2=2017&type=VHI_Parea&provinceID="

# Импорт модулей
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn

# =====================================================================
def download_data():
	'''
	загрузка данных из интернета
	'''

	# функция вычленения даты из года и номера недели
	dateparse = lambda x, y: pd.datetime.strptime(x + '-' + y + '-1', "%G-%V-%u")
	
	# открываем таблицу с названиями областей
	provinces = pd.read_excel(
		urlprov,			# имя файла
        index_col=None,		# столбец индексов
        header=0,			# используем первую строку в качестве названий столбцов
    )

	# загружаем данные по всем областям
	for index, row in provinces.iterrows():
		
		# считывваем информацию об индексах
		url = urlmean + str(row['provinceID'])
		frameMean = pd.read_table(
			url,					# адрес источника данных
			encoding='latin-1',		# кодировка
			sep=r"[,\s]+",			# разделитель запятая или пробел
			skipinitialspace=True,	# игнорировать пробелы после разделителя
			index_col=None,			# без столбца индексов
			header=None,			# без строки залоловков
			names=['year','week','SMN','SMT','VCI','TCI','VHI'],    #наименования колонок
			skiprows = 1,			# убираем текст перед таблицей
			skipfooter = 1,			# убираем пустую последнюю строку
			engine = 'python',		# движок конвертации
			parse_dates = {'datetime': ['year', 'week']},	# вычленяем дату из года и номера недели
			date_parser=dateparse,	# правило вычленения
		)

		# считываем информацию о процентах территории
		url = urlparea + str(row['provinceID'])
		frameParea = pd.read_table(
			url,					# адрес источника данных
			encoding='latin-1',		# кодировка
			sep=r"[,\s]+",			# разделитель запятая или пробел
			skipinitialspace=True,	# игнорировать пробелы после разделителя
			index_col=None,			# без столбца индексов
			header=None,			# без строки залоловков
			names=['year','week', '0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100'],
			skiprows = 1,			# убираем текст перед таблицей
			skipfooter = 1,			# убираем пустую последнюю строку
			engine = 'python',		# движок конвертации
			parse_dates = {'datetime': ['year', 'week']},	# вычленяем дату из года и номера недели
			date_parser=dateparse,	# правило вычленения
		)
		
		# объединяем полученные данные в один фрейм
		frame = pd.merge(frameMean, frameParea, on = ['datetime'])

		# записываем полученный фрейм в файл с названием области в формате
		# '1-Vinnytsya.csv'
		frame.to_csv(str(row['localID']) + '-' + row['province'] + '.csv')

	return

# =====================================================================
def read_data(region):
	'''
	загрузка данных по заданной области из файла в фрейм
	'''

	# открываем таблицу с названиями областей
	provinces = pd.read_excel(
		urlprov,			# имя файла
        index_col=0,		# столбец индексов
        header=0,			# используем первую строку в качестве названий столбцов
    )

	# создаём url файла в формате '1-Vinnytsya.csv'
	url = str(region) + '-' + provinces[provinces.localID == int(region)].iloc[0, 0] + '.csv'

	# загружаем данные по заданой области из файла
	print("Reading data from file " + url)
	frame = pd.read_csv(url,						# адрес источника данных
        index_col=0,				# столбец индексов
		parse_dates = ['datetime']	# восстанавливаем столбец даты
	)

	# возвращаем dataframe с данными по заданной области
	return frame

# =====================================================================
def find_min_max(frame, year):
	'''
	Ряд VHI для області за рік, пошук екстремумів (min та max)
	'''

	# обираємо вегетаційний період з вересня по липень наступного року
	frame = frame[frame['datetime'].between(datetime.date(year, 9, 1), datetime.date(year + 1, 8, 31))]

	# пошук екстремумів (min та max)
	minvalue = frame['VHI'].idxmin()
	maxvalue = frame['VHI'].idxmax()
	print("Minimum VHI value: " + str(frame['VHI'][minvalue]) + " was on " + str(frame['datetime'][minvalue].strftime('%d %B %Y')))
	print("Maximum VHI value: " + str(frame['VHI'][maxvalue]) + " was on " + str(frame['datetime'][maxvalue].strftime('%d %B %Y')))

	# відображення ряду VHI за вегетаційний період
	plot(frame)

	return

# =====================================================================
def droughts(frame, percent):
	'''
	Ряд VHI за всі роки для області, виявити роки з екстремальними посухами, 
	які торкнулися більше вказаного відсотка області
	'''
	frame['VHI'] = frame['0'] + frame['5']
	plot(frame)

	return

# =====================================================================
def plot(results):
    '''
    Create a plot
    '''

    # Preparing the plot
    fig = plt.figure()
    fig.canvas.set_window_title('VHI index')
    plt.plot(results['datetime'], results['VHI'])

    plt.title('VHI for the year')
    plt.xlabel('Date')
    plt.ylabel('VHI average')
    plt.legend(loc='lower left')

    # Let matplotlib improve the layout
    plt.tight_layout()

    # Display the plot in interactive UI
    plt.show()

    # Closing the figure allows matplotlib to release the memory used.
    plt.close()

# =====================================================================
if __name__ == '__main__':
	'''
	Функція main
	'''
	
	# устанавливаем рабочую директорию
	os.chdir("C:\\Users\\vladi\\OneDrive\\СЕМЬЯ\\Политех\\repos\\PythonClassifierApplication1")

	# Task 1.
	# Для кожної із адміністративних одиниць України завантажити тестові
	# структуровані файли,
	# що містять значення VHI-індексу
	# print("Downloading data")
	# download_data()

	# Task 2.
	# Зчитати завантажені текстові файли у фрейм (за номером області)
	region = '1'
	frame = read_data(region)

	# Task 3.
	# Ряд VHI для області за рік, пошук екстремумів (min та max)
	year = 2010
	print("Seeking Min and Max VHI for the year " + str(year))
	find_min_max(frame, year)

	# Task 4.
	# Ряд VHI за всі роки для області,
	# виявити роки з екстремальними посухами (6 < VHI < 15),
	# які торкнулися більше вказаного відсотка області
	droughts(frame, 10)

	# Task 5. 
	# Аналогічно для помірних посух (26 < VHI < 35)
