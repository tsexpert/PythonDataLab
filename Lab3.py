'''
Лабораторная работа 3

Sample data
Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity;Sub_metering_1;Sub_metering_2;Sub_metering_3
16/12/2006;17:24:00;4.216;0.418;234.840;18.400;0.000;1.000;17.000
16/12/2006;17:25:00;5.360;0.436;233.630;23.000;0.000;1.000;16.000
'''

# Импорт модулей
import pandas as pd
import numpy as np
import datetime
from random import sample

# Глобальные переменные
url = "household_power_consumption.zip"

# =====================================================================
def read_data():
	'''
	загрузка данных из файла в фрейм
	'''

	print("Reading data from file " + url + "...")
	frame = pd.read_csv(
		url,						# адрес источника данных
		sep = ';',					# сепаратор
		header = 0,					# первая строка - названия столбцов
        index_col = None,			# столбец индексов отсутствует
		parse_dates = {'Datetime' : ['Date','Time']},	# восстанавиливаем дату и время
		infer_datetime_format = True,					# автоопределение формата даты/времени
		na_values = '?',			# указываем какой символ применяется для неопределённых значений
	)

	# убираем строки с отсутствующими данными
	frame.dropna(inplace=True)
	print("Done!")
	# возвращаем dataframe с данными
	return frame

# =====================================================================
def task1():
	'''
	Завдання 1.	
	Обрати всі показники домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт.
	'''
	global dataframe		# используем переменную из функции main
	global nparray			# используем переменную из функции main
	power = 5.0				# пороговое значение мощности по заданию
	
	print('\nTask 1')
	#### с использованием pandas dataframe ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем фильтр к фрейму
	frame_res = dataframe[dataframe['Global_active_power'] > power]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(frame_res.loc[:,'Global_active_power'])
	print('Pandas time: ' + str(timedelta))

	#### с использованием numpy array ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем фильтр к массиву
	array_res = nparray[np.where(nparray[:,1] > power)]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(array_res[:,[0,1]])
	print(array_res.shape)
	print('Numpy time: ' + str(timedelta))

	return

# =====================================================================
def task2():
	'''
	Завдання 2.	
	Обрати всі показники домогосподарства, у яких вольтаж перевищую 235 В.
	'''
	global dataframe		# используем переменную из функции main
	global nparray			# используем переменную из функции main
	voltage = 235.0			# пороговое значение напряжения по заданию
	
	print('\nTask 2')
	#### с использованием pandas dataframe ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем фильтр к фрейму
	frame_res = dataframe[dataframe['Voltage'] > voltage]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(frame_res.loc[:,'Voltage'])
	print('Pandas time: ' + str(timedelta))

	#### с использованием numpy array ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем фильтр к массиву
	array_res = nparray[np.where(nparray[:,3] > voltage)]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(array_res[:,[0,3]])
	print(array_res.shape)
	print('Numpy time: ' + str(timedelta))

	return

# =====================================================================
def task3():
	'''
	Завдання 3.	
	Обрати всі показники домогосподарства, у яких сила струму лежить в межах 19-20 А, для них виявити ті,
	у яких пральна машина та холодильних споживають більше, ніж бойлер та кондиціонер.
	'''
	global dataframe		# используем переменную из функции main
	global nparray			# используем переменную из функции main
	ampmin = 19.0			# нижнее значение силы тока по заданию
	ampmax = 20.0			# верхнее значение силы тока по заданию
	
	print('\nTask 3')
	#### с использованием pandas dataframe ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем фильтр к фрейму
	frame_res = dataframe[(dataframe['Global_intensity'] > ampmin) & (dataframe['Global_intensity'] < ampmax)]
	# применяем дополнительный фильтр
	frame_res = frame_res[frame_res['Sub_metering_2'] > frame_res['Sub_metering_3']]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(frame_res.loc[:,'Global_intensity'])
	print('Pandas time: ' + str(timedelta))

	#### с использованием numpy array ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем фильтр к массиву
	array_res = nparray[(nparray[:,4] > ampmin) & (nparray[:,4] < ampmax)]
	# применяем дополнительный фильтр
	array_res = array_res[array_res[:,6] > array_res[:,7]]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(array_res[:,[0,4]])
	print(array_res.shape)
	print('Numpy time: ' + str(timedelta))

	return

# =====================================================================
def task4():
	'''
	Завдання 4.	
	Обрати випадковим чином 500000 показників домогосподарства (без повторів елементів вибірки),
	для них обчислити середні величини усіх 3-х груп споживання електричної енергії
	'''
	global dataframe		# используем переменную из функции main
	global nparray			# используем переменную из функции main
	samples = 500000		# количество элементов выборки
	
	print('\nTask 4')
	#### с использованием pandas dataframe ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем выборку к фрейму
	# и вычисляем средние значения
	mean = dataframe[['Sub_metering_1','Sub_metering_2','Sub_metering_3']].sample(n=samples).mean()
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(mean)
	print('Pandas time: ' + str(timedelta))

	#### с использованием numpy array ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем выборку к массиву
	# и вычисляем средние значения
	mean = np.mean(nparray[np.random.choice(nparray.shape[0], size=samples, replace=False)][:,5:8], axis=0)
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(mean)
	print('Numpy time: ' + str(timedelta))

	return

# =====================================================================
def task5():
	'''
	Завдання 5.	
	Обрати ті показники домогосподарства, які після 18-00 споживають понад 6 кВт за хвилину в середньому,
	серед відібраних визначити ті, у яких основне споживання електроенергії у вказаний проміжок часу
	припадає на пральну машину, сушарку, холодильник та освітлення (група 2 є найбільшою),
	а потім обрати кожен третій результат із першої половини та кожен четвертий результат 
	із другої половини.
	'''
	global dataframe		# используем переменную из функции main
	global nparray			# используем переменную из функции main
	power = 6.0				# значение мощности

	print('\nTask 5')
	#### с использованием pandas dataframe ####
	# засекаем время
	starttime = datetime.datetime.now()
	# применяем выборку по времени и мощности
	frame_res = dataframe[dataframe['Global_active_power'] > power].reset_index().set_index('Datetime').between_time('18:00','23:59')
	# делим выборку на группы:
	# группа 1: пральна машина, сушарка, холодильник та освітлення 
	frame1 = frame_res[frame_res[['Sub_metering_1','Sub_metering_2','Sub_metering_3']].idxmax(axis=1) == 'Sub_metering_2']
	# группа 2: решта споживачів
	frame2 = frame_res[frame_res[['Sub_metering_1','Sub_metering_2','Sub_metering_3']].idxmax(axis=1) != 'Sub_metering_2']
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	# каждый третий результат группы 1
	print(frame1.iloc[2::3,:])
	# каждый четвертый результат группы 2
	print(frame2.iloc[3::4,:])
	print('Pandas time: ' + str(timedelta))

	#### с использованием numpy array ####
	# засекаем время
	starttime = datetime.datetime.now()
	# преобразуем отфильтрованный dataframe в numpy array с учётом условий задачи
	array_res = frame_res.values
	# делим выборку на группы:
	# группа 1: пральна машина, сушарка, холодильник та освітлення 
	# каждый третий результат группы 1
	array1 = array_res[np.argmax(array_res[:,5:8], axis=1) == 1][2::3,:]
	# группа 2: решта споживачів
	# каждый четвертый результат группы 2
	array2 = array_res[np.argmax(array_res[:,5:8], axis=1) != 1][3::4,:]
	# останавливаем время
	endtime = datetime.datetime.now()
	timedelta = endtime - starttime
	# вывод результатов на экран
	print(array1)
	print(array1.shape)
	print(array2)
	print(array2.shape)
	print('Numpy time: ' + str(timedelta))

	return

# =====================================================================
if __name__ == '__main__':
	'''
	Функція main
	'''
	# Считываем данные в pandas фрейм
	dataframe = read_data()

	# Убираем столбец с датой и
	# Преобразуем фрейм в numpy array с сохранением индекса
	print('Creating numpy array from dataframe\n')
	nparray = dataframe.drop(['Datetime'], axis=1).reset_index().values
	print('Done!')

	# Завдання 1.
	# Обрати всі домогосподарства, у яких загальна активна споживана потужність
	# перевищує 5 кВт.
	task1()

	# Завдання 2.
	# Обрати всі домогосподарства, у яких вольтаж перевищую 235 В.
	task2()

	# Завдання 3.
	# Обрати всі домогосподарства, у яких сила струму лежить в межах 19-20 А, для
	# них виявити ті,
	# у яких пральна машина та холодильних споживають більше, ніж бойлер та
	# кондиціонер.
	task3()

	# Завдання 4.
	# Обрати випадковим чином 500000 домогосподарств (без повторів елементів
	# вибірки),
	# для них обчислити середні величини усіх 3-х груп споживання електричної
	# енергії
	task4()

	# Завдання 5.	
	# Обрати ті показники домогосподарства, які після 18-00 споживають понад 6 кВт за хвилину в середньому,
	# серед відібраних визначити ті, у яких основне споживання електроенергії у вказаний проміжок часу
	# припадає на пральну машину, сушарку, холодильник та освітлення (група 2 є найбільшою),
	# а потім обрати кожен третій результат із першої половини та кожен четвертий результат 
	# із другої половини.
	task5()