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
#import os
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import datetime
#import seaborn

# =====================================================================
def read_data():
	'''
	загрузка данных из файла в фрейм
	'''

	print("Reading data from file " + url)
	frame = pd.read_csv(
		url,						# адрес источника данных
		sep = ';',					# сепаратор
		header = 0,					# первая строка - названия столбцов
        index_col = None,			# столбец индексов
		parse_dates = {'Datetime' : ['Date','Time']},	# восстанавиливаем дату и время
		infer_datetime_format = True,					# автоопределение формата даты/времени
		#dtype = {										# задаём типы данных для ячеек
		#	'Global_active_power' : np.float64,
		#	'Global_reactive_power' : np.float64,
		#	'Voltage;Global_intensity' : np.float64,
		#	'Sub_metering_1' : np.float64,
		#	'Sub_metering_2' : np.float64,
		#	'Sub_metering_3' : np.float64,
		#	},
		na_values = '?',
		#verbose = True,
		#low_memory = False			# убираем предупреждения системы
	)

	# убираем строки с отсутствующими данными
	frame.dropna(inplace=True)

	# возвращаем dataframe с данными по заданной области
	return frame

# =====================================================================
if __name__ == '__main__':
	'''
	Функція main
	'''
	# Считываем данные в pandas фрейм
	frame = read_data()

	# Убираем столбец с датой
	frame_clean = frame.drop(['Datetime'], axis=1)

	# Преобразуем фрейм в numpy array с сохранением индекса
	narray = frame_clean.reset_index().values
	del frame_clean		# удаляем ненужный фрейм
	
	#1.	
	# Обрати всі домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт.
	# с использованием pandas dataframe
	# засекаем время
	starttime = datetime.datetime.now()

	frame_5KW = frame[frame['Global_active_power'] > 5.0]

	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	print(frame_5KW)
	print(timedelta)

	# с использованием numpy array
	# засекаем время
	starttime = datetime.datetime.now()

	frame_5KW = narray[np.where(narray[:,1]>5.0)]
	
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	print(frame_5KW)
	print(timedelta)

	#2.	
	# Обрати всі домогосподарства, у яких вольтаж перевищую 235 В.

	#3.	
	# Обрати всі домогосподарства, у яких сила струму лежить в межах 19-20 А, для них виявити ті,
	# у яких пральна машина та холодильних споживають більше, ніж бойлер та кондиціонер.

	#4.	
	# Обрати випадковим чином 500000 домогосподарств (без повторів елементів вибірки),
	# для них обчислити середні величини усіх 3-х груп споживання електричної енергії, 
	# а також

	#5.	
	# Обрати ті домогосподарства, які після 18-00 споживають понад 6 кВт за хвилину в середньому,
	# серед відібраних визначити ті, у яких основне споживання електроенергії у вказаний проміжок часу
	# припадає на пральну машину, сушарку, холодильник та освітлення (група 2 є найбільшою),
	# а потім обрати кожен третій результат із першої половини та кожен четвертий результат 
	# із другої половини.