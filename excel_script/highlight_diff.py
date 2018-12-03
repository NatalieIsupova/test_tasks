import openpyxl as ox
import sys
import os


def read_data_from_excel(filename):
    """
    Функция читает одностраничные и многостраничные файлы Excel
    :param filename: путь к файлу, который хотим прочитать
    :return: возвращает head - "шапку" (названия столбцов, list); data - данные таблицы (list)
    """
    # загружаем документ
    document = ox.load_workbook(filename=filename)
    # определяем названия листов в файле
    sheets = document.sheetnames
    # сохраняем шапку таблицы
    head = [cell.value for cell in list(document[sheets[0]].rows)[0]]
    # построчно читаем данные с каждого листа
    data = []
    for sheet in sheets:
        data += [[cell.value for cell in row] for row in document[sheet].rows][1:]

    return head, data


def data_difference(head, source_file, updated_file):
    """
    Функция выявляет разницу между двумя файлами Excel: неизмененные строки остаются без цвета,
    добавленные во втором файле строки окрашиваются в зеленый цвет, удаленные во втором файле
    строки окрашиваются в красный цвет, строки второго файла, где были изменены данные (кроме ID)
    окрашиваются в желтый цвет
    :param head: шапка изначального документа
    :param source_file: данные изначального документа
    :param updated_file: данные измененного документа
    :return: data - данные для нового объединенного файла (list), colors - ключи для раскрашивания
    строк таблицы (list)
    """

    # находим столбец с ID, запоминаем его индекс
    for index, value in enumerate(head):
        if value == "ID":
            id_index = index
    # сортируем данные файлов по столбцу с индексами
    data_source_sorted = sorted(source_file, key=lambda column: column[id_index])
    data_updated_sorted = sorted(updated_file, key=lambda column: column[id_index])
    # создаем массивы для обозначения цветов и самих данных
    colors = []
    data = []

    i = 0
    j = 0
    # используется сортировка слиянием: идем по двум массивами и сравниваем их поэлементно
    while i < len(data_source_sorted) and j < len(data_updated_sorted):
        # если ID строки первого файла меньше ID строки второго файла, то строка была удалена
        if data_source_sorted[i][id_index] < data_updated_sorted[j][id_index]:
            # добавляем строку первого файла в массив для новой таблицы
            data.append(data_source_sorted[i])
            # указываем красный цвет
            colors.append("red")
            # движемся дальше по первому файлу
            i += 1
        # если ID строки первого файла равно ID строки второго файла, то нужно сравнить содержимое строк
        elif data_source_sorted[i][id_index] == data_updated_sorted[j][id_index]:
            # если содержимое равно, то строка не была изменена
            if data_source_sorted[i] == data_updated_sorted[j]:
                # добавляем строку из первого файла в массив для новой таблицы
                data.append(data_source_sorted[i])
                # не указываем цвет
                colors.append("")
            # если содержимое не равно, строка изменена
            else:
                # добавляем измененную строку второго файла в массив для новой таблицы
                data.append(data_updated_sorted[j])
                # указываем для нее желтый цвет
                colors.append("yellow")
            # продвигаемся дальше по обоим файлам
            i += 1
            j += 1
        # если ID строки первого файла больше ID строки второго файла, то строка была добавлена
        elif data_source_sorted[i][id_index] > data_updated_sorted[j][id_index]:
            # добавляем строку из второго файла в массив для новой таблицы
            data.append(data_updated_sorted[j])
            # указываем зеленый цвет
            colors.append("green")
            # движемся дальше по второму файлу
            j += 1

    # если один из файлов закончился, то мы должны добавить в новый файл оставшиеся строки другого файла
    while i < len(data_source_sorted):
        # остались строки изначального файла, значит, они были удалены, добавляем их, красим в красный
        data.append(data_source_sorted[i])
        colors.append("red")
        i += 1
    while j < len(data_updated_sorted):
        # остались строки измененного файла, значит, они были добавлены, добавляем их, красим в зеленый
        data.append(data_updated_sorted[j])
        colors.append("green")
        j += 1

    return data, colors


def write_data_to_excel(filename, head, data, colors):
    """
    Функция записывает шапку и данные в файл Excel, применяя к ним окраску из массива colors
    :param filename: путь к новому файлу
    :param head: шапка таблицы (list)
    :param data: данные таблицы (list)
    :param colors: массив с цветами строк (list)
    """
    # определяем цвета заливки - названия должны совпадать с теми, которые мы добавляли в colors
    red = ox.styles.colors.Color(rgb='DA9694')
    red_fill = ox.styles.fills.PatternFill(patternType='solid', fgColor=red)
    yellow = ox.styles.colors.Color(rgb='FFFF00')
    yellow_fill = ox.styles.fills.PatternFill(patternType='solid', fgColor=yellow)
    green = ox.styles.colors.Color(rgb='C4D79B')
    green_fill = ox.styles.fills.PatternFill(patternType='solid', fgColor=green)

    # создаем новый файл, выбираем первую страницу таблицы
    wb = ox.Workbook()
    ws = wb.active
    # к данным для записи добавляем нашу шапку, поправляем массив цветов (шапка бесцветная)
    data = [head] + data
    colors = [""] + colors
    # создаем ячейки, пишем туда данные, красим согласно массиву цветов
    for row in range(len(data)):
        for col in range(len(data[row])):
            _ = ws.cell(column=col + 1, row=row + 1, value=data[row][col])
            if colors[row] == "red":
                _.fill = red_fill
            if colors[row] == "yellow":
                _.fill = yellow_fill
            if colors[row] == "green":
                _.fill = green_fill
    # сохраняем файл
    wb.save(filename)


if __name__ == "__main__":
    # читаем пути к файлам из терминала, нормализуем
    source = os.path.abspath(sys.argv[1])
    updated = os.path.abspath(sys.argv[2])
    new = os.path.abspath(sys.argv[3])

    # читаем два файла
    head, data_source = read_data_from_excel(source)
    useless_head, data_updated = read_data_from_excel(updated)

    # узнаем разницу между ними и цвета, в которые нужно покрасить строки
    data, colors = data_difference(head, data_source, data_updated)

    # записываем результат в новый файл, красим
    write_data_to_excel(new, head, data, colors)
