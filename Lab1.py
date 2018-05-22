'''
Лабораторные работы 1 + 2
'''

# Глобальные переменные
urlprov = "Provinces.xlsx"
# Для нашей работы берем данные за 10 лет: с 2007 по 2017
urlmean = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&year1=2007&year2=2017&type=Mean&provinceID="
urlparea = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&year1=2007&year2=2017&type=VHI_Parea&provinceID="

# Импорт модулей
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
	provinces = pd.read_excel(urlprov,			# имя файла
        index_col=None,		# столбец индексов
        header=0,			# используем первую строку в качестве названий столбцов
    )

	# загружаем данные по всем областям
	for index, row in provinces.iterrows():
		
		# считывваем информацию об индексах
		url = urlmean + str(row['provinceID'])
		frameMean = pd.read_table(url,					# адрес источника данных
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
		frameParea = pd.read_table(url,					# адрес источника данных
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
	frame = pd.read_csv(
		url,						# адрес источника данных
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
	starttme = str(year) + '-09-01'
	endtime = str(year + 1) + '-08-31'
	frame = frame[(frame['datetime'] >= starttme) & (frame['datetime'] <= endtime)]

	# пошук екстремумів (min та max)
	minvalue = frame['VHI'].idxmin()
	maxvalue = frame['VHI'].idxmax()
	print("Minimum VHI value: " + str(frame['VHI'][minvalue]) + " was on " + str(frame['datetime'][minvalue].strftime('%d %B %Y')))
	print("Maximum VHI value: " + str(frame['VHI'][maxvalue]) + " was on " + str(frame['datetime'][maxvalue].strftime('%d %B %Y')))

	# відображення ряду VHI за вегетаційний період
	plot(frame, frame['VHI'][maxvalue])

	return

# =====================================================================
def plot(results, threshold):
	'''
	Графічне відображення результатів
	з виводом порогового значення
	'''
	
	# Підготовка маркерів
	years = mdates.YearLocator()			# every year
	months = mdates.MonthLocator()			# every month
	yearsFmt = mdates.DateFormatter('%Y')	# ticker format

	# Підготовка графіка
	fig, ax = plt.subplots()
	ax.plot(results['datetime'], results['VHI'])
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)
	fig.autofmt_xdate()
	plt.title('VHI for the year')
	plt.xlabel('Date')
	plt.ylabel('VHI average')
	plt.legend(loc='lower left')
	plt.axhline(y=threshold, color='r', linestyle='-')
	
	# поліпшення графіка
	plt.tight_layout()

	# показ графіка в вікні
	plt.show()

	# закритті вікна, звільнення пам'яті
	plt.close()

# =====================================================================
if __name__ == '__main__':
	'''
	Функція main
	'''
	# Task 1.
	# Для кожної із адміністративних одиниць України завантажити тестові
	# структуровані файли, що містять значення VHI-індексу
	# print("Downloading data")
	# download_data()

	# Task 2.
	# Зчитати завантажені текстові файли у фрейм (за номером області)
	region = '14'
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
	# нехай вказаний відсоток = 20%
	percent = 20
	frame['VHI'] = frame['10']
	plot(frame, percent)

	# Task 5.
	# Аналогічно для помірних посух (26 < VHI < 35)
	frame['VHI'] = frame['30']
	plot(frame, percent)