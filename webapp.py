'''
Лабораторная работа 2
'''

# Глобальные переменные
urlprov = "Provinces.xlsx"

# Импорт модулей
import os
import pandas as pd
import datetime
from spyre import server

server.include_df_index = True

# =====================================================================
class WebDataOutput(server.App):
	
	def __init__(self):
		# инициализация нового объекта класса

		# открываем таблицу с названиями областей
		self.provinces = pd.read_excel(
			urlprov,			# имя файла
			index_col=None,		# столбец индексов
			header=0,			# используем первую строку в качестве названий столбцов
			usecols = 'B:C'		# используем колонки с названием и номером области
		)
		self.provinces.columns = ['label','value']					# переименовываем колонки
		self.optionlist = self.provinces.to_dict(orient='records')	# сохраняем в виде dictionary
		self.inputs = [
			{
			"type": 'dropdown',
			"label": 'Область',
			"options": self.optionlist,
			"value": 22,
			"key": 'region'},
			{
			"type": 'dropdown',
			"label": 'Индекс',
			"options": [
            {"label": "VCI", "value": "VCI"},
            {"label": "TCI", "value": "TCI"},
            {"label": "VHI", "value": "VHI"}],
			"value": 'VHI',
			"key": 'indx'},
			{
			"type": 'slider',
			"label": 'Начальный год',
			"value": 2007,
			"min" : 2007,
			"max" : 2017,
			"key": 'yr'},
			{
			"type": 'slider',
			"label": 'Начальный месяц',
			"value": 1,
			"min" : 1,
			"max" : 12,
			"key": 'mth'},
			{
			"type": 'slider',
			"label": 'Кол-во лет',
			"value": 1,
			"min" : 1,
			"max" : 10,
			"key": 'yr_n'},
			]
		
	title = "Вегетаційний індекс"

	controls = [{
        "type": "button",
        "id": "update_data",
        "label": "get data"
    }]

	tabs = ["Plot", "Table"]

	outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"},
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

	def getData(self, params):
		# запрос данных по выбранным параметрам

		region = params['region']
		indx = params['indx']
		yr = params['yr']
		mth = params['mth']
		yr_n = params['yr_n']
		startdate = datetime.date(int(yr),int(mth),1)
		endyr = yr + yr_n
		enddate = datetime.date(int(endyr),int(mth),1)

		# создаём url файла в формате '1-Vinnytsya.csv'
		url = str(region) + '-' + self.provinces[self.provinces.value == int(region)].iloc[0, 0] + '.csv'

		# загружаем данные по заданой области из файла
		frame = pd.read_csv(
			url,								# адрес источника данных
			index_col = 0,						# столбец индексов
			usecols = ['datetime', indx],		# считываем только нужные колонки
			parse_dates = ['datetime']			# восстанавливаем столбец даты
		)

		# возвращаем dataframe с данными по заданной области
		frame = frame[startdate:enddate]
		return frame

# =====================================================================
if __name__ == '__main__':
	'''
	Функція main
	'''
	
	# устанавливаем рабочую директорию
	os.chdir("C:\\Users\\vladi\\OneDrive\\СЕМЬЯ\\Политех\\repos\\PythonClassifierApplication1")

	# запускаем web приложение
	app = WebDataOutput()
	app.launch(port=9093)
