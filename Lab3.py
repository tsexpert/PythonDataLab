'''
Лабораторная работа 3

Sample data
Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity;Sub_metering_1;Sub_metering_2;Sub_metering_3
16/12/2006;17:24:00;4.216;0.418;234.840;18.400;0.000;1.000;17.000
16/12/2006;17:25:00;5.360;0.436;233.630;23.000;0.000;1.000;16.000
'''

# Глобальные переменные
url = "household_power_consumption.zip"

# Импорт модулей
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn

# =====================================================================
def read_data():
	'''
	загрузка данных из файла в фрейм
	'''

	# загружаем данные по заданой области из файла
	print("Reading data from file " + url)
	frame = pd.read_csv(
		url,						# адрес источника данных
		sep = ';',					# сепаратор
		header = 0,					# header is a first row
        index_col = None,			# столбец индексов
		parse_dates = {'datetime' : ['Date','Time']},
		infer_datetime_format = True,
	)

	# возвращаем dataframe с данными по заданной области
	return frame

# =====================================================================
def find_min_max(frame, year):
	'''
	Ряд VHI для області за рік, пошук екстремумів (min та max)
	'''

	# обираємо вегетаційний період з вересня по липень наступного року
	# frame = frame[frame['datetime'].between(datetime.date(year, 9, 1), datetime.date(year + 1, 8, 31))]
	# starttme = datetime.date(year, 9, 1)
	starttme = str(year) + '-09-01'
	# endtime = datetime.date(year + 1, 8, 31)
	endtime = str(year+1) + '-08-31'
	# frame.set_index('datetime')
	frame = frame[(frame['datetime'] >= starttme) & (frame['datetime'] < endtime)]
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
	
	# Task 1.
	# Для кожної із адміністративних одиниць України завантажити тестові
	# структуровані файли,
	# що містять значення VHI-індексу
	# print("Downloading data")
	# download_data()

	# Task 2.
	# Зчитати текстовий файл у фрейм
	frame = read_data()

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
