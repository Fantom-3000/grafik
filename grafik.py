from PyQt5 import QtWidgets, QtGui, QtCore
import sys

# Обработчик нажатия кнопки. Вывод годового графика смены №...
def enter_btn_click():
    norma = float(norma_edit.text())
    smena_id = smena_cbox.currentText()

    row = 0
    for month_id in grafik[smena_id]:
        col = 0
        for day_id in grafik[smena_id][month_id]:
            hours_day = QtGui.QStandardItem(str(day_id))
            table_model.setItem(row, col, hours_day)
            col += 1
        row += 1
    hours_count()


# Формирование годового графика всех смен
def creat_grafik():
    for smena_id in smena:
        day = 0
        grafik.setdefault(smena_id, {})
        for month_id in range(12):
            smena_month = []
            for day_id in range(month_days[month_id]):
                smena_month.append(smena[smena_id][day])
                if day == 3:
                    day = 0
                else:
                    day += 1
            grafik[smena_id].setdefault(
                str(month[month_id]), smena_month)
    return grafik

# Подсчет и вывод общего, вечерних и ночных количества часов за год
def hours_count():
    norm_hours_in_year = float(norma_edit.text())
    # Подсчет часов за месяц
    for row_index in range(12):
        month_hours = 0
        month_evening_hours = 0
        month_night_hours = 0
        for col_index in range(month_days[row_index]):
            day_hours = float(
                table_model.data(table_model.index(row_index, col_index))
                )
            month_hours += day_hours
            if day_hours == 11:
                month_evening_hours += 2
            elif day_hours == 3.5:
                month_evening_hours += 2
                month_night_hours += 1.5
            elif day_hours == 7.5:
                month_night_hours += 5.5
        # Вывод часов за месяц
        table_model.setItem(
            row_index, 31, QtGui.QStandardItem(str(month_hours))
            )
        table_model.setItem(
            row_index, 32, QtGui.QStandardItem(str(month_evening_hours))
            )
        table_model.setItem(
            row_index, 33, QtGui.QStandardItem(str(month_night_hours))
            )

    # Подсчет общего количества часов за год по факту
    year_hours_count = 0
    for row_index in range(12):
        year_hours_count += float(
            table_model.data(table_model.index(row_index, 31))
            )
    # Вывод суммарного количества часов за год по факту
    table_model.setItem(
        12, 31, QtGui.QStandardItem(str(year_hours_count))
        )

    # Вывод суммарного количества часов за год по норме    
    table_model.setItem(
        13, 31, QtGui.QStandardItem(str(norm_hours_in_year))
        )

    # Вывод количества часов переработки за год
    table_model.setItem(
        14, 31, QtGui.QStandardItem(
            str(year_hours_count - norm_hours_in_year)
            )
        )

    table.resizeColumnsToContents()
'''
    # Вывод общего количества вечерних часов за год
    year_evening_hours = hours_count('year_evening_hours')
    table_model.setItem(
        12, 32, QtGui.QStandardItem(str(year_evening_hours))
        )

    # Вывод общего количества ночных часов за год
    year_night_hours = hours_count('year_night_hours')
    table_model.setItem(
        12, 33, QtGui.QStandardItem(str(year_night_hours))
        )

    # Подсчет общего количества вечерних часов
    elif time_of_day == 'year_evening_hours':
        for row_index in range(12):
            hours_count += float(
                table_model.data(table_model.index(row_index, 32))
                )

    # Подсчет общего количества ночных часов за год
    elif time_of_day == 'year_night_hours':
        for row_index in range(12):
            hours_count += float(
                table_model.data(table_model.index(row_index, 33))
                )        
'''          

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    grafik = {}
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    smena = {'Смена №1': [0, 11, 3.5, 7.5], 'Смена №2': [3.5, 7.5, 0, 11],
             'Смена №3': [7.5, 0, 11, 3.5], 'Смена №4': [11, 3.5, 7.5, 0]}
    month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
             'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    h_header = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                '24', '25', '26', '27', '28', '29', '30', '31', 'Часы', 'Вечер.',
                'Ночн.']
    v_header = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
                'Итого', 'Норма', 'Перераб.']

    window = QtWidgets.QWidget()
    window.setWindowState(QtCore.Qt.WindowMaximized)
    box = QtWidgets.QVBoxLayout(window)
    vbox1 = QtWidgets.QVBoxLayout()
    hbox1 = QtWidgets.QHBoxLayout()
    table = QtWidgets.QTableView()
    table.setFont(QtGui.QFont('Arial', 8))
    table.setAlternatingRowColors(True)
    table_model = QtGui.QStandardItemModel()
    table_model.setVerticalHeaderLabels(v_header)
    table_model.setHorizontalHeaderLabels(h_header)
    table.setSpan(12, 0, 1, 31)
    table.setSpan(13, 0, 1, 31)
    table.setSpan(14, 0, 1, 31)
    table.setModel(table_model)
    table.resizeColumnsToContents()
    smena_cbox_model = QtCore.QStringListModel(smena.keys())
    smena_cbox = QtWidgets.QComboBox()
    smena_cbox.setModel(smena_cbox_model)
    norma_edit = QtWidgets.QLineEdit('1993')
    norma_edit.setFixedWidth(100)

    enter_btn = QtWidgets.QPushButton('Пересчитать')

    grafik = creat_grafik() # Формирование годового графика
    enter_btn_click()

    enter_btn.clicked.connect(hours_count)
    smena_cbox.currentTextChanged.connect(enter_btn_click)

    hbox1.addWidget(norma_edit)
    hbox1.addWidget(smena_cbox)
    hbox1.addWidget(enter_btn)
    vbox1.addWidget(table)   
    box.addLayout(hbox1)
    box.addLayout(vbox1)
    window.show()
    sys.exit(app.exec_())
