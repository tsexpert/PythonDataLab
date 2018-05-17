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
	# Считываем данные в pandas фрейм
	frame = read_data()

	# Отделяем столбец с датой в отдельный фрейм. В оставшемся фрейме - только числовые данные по потреблению
	frame_split = np.split(frame, [1], axis=1)
		
	# Преобразуем фрейм в numpy array
	narray = frame_split[1].reset_index().values
		
	#1.	
	# Обрати всі домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт.
	frame_5KW = frame[frame['Global_active_power'] > 5.0]
	print(frame_5KW)
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