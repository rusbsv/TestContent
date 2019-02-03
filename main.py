import random
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic


# структура для хранения тестового вопроса, опишем поля согласно входному txt-файлу:
class Task:
    vopros = ''  # вопрос
    otv1 = ''  # вариант 1 ответа
    otv2 = ''  # вариант 2 ответа
    otv3 = ''  # вариант 3 ответа
    otv4 = ''  # вариант 4 ответа
    otv5 = ''  # вариант 5 ответа
    prav_otv = 0  # номер правильного ответа
    ball = 0  # начисляемые баллы


# содержит массив тестовых вопросов, методы добавления и удаления текстовых вопросов,
# а так же метод доступа к текстовому заданию по его порядковому номеру в списке.
class TextContent:
    def __init__(self):  # конструктор класса, 
        self.mas = []  # инициализирует массив текстовых вопросов

    def __del__(self):  # деструктор
        pass

    def addTask(self, vopros, otv1, otv2, otv3, otv4, otv5, prav_otv, ball):
        """ метод добавления текстовых вопросов """
        for prover_povtor in self.mas:  # проверяем, не повторяется ли вопрос
            if vopros == prover_povtor.vopros:
                return
        t = Task()
        t.vopros = vopros
        t.otv1 = otv1
        t.otv2 = otv2
        t.otv3 = otv3
        t.otv4 = otv4
        t.otv5 = otv5
        t.prav_otv = prav_otv
        t.ball = ball
        self.mas.append(t)

    def getTask(self, num):
        """ метод доступа к текстовому заданию по его порядковому номеру в списке """
        return self.mas[num]

    def delTask(self, num):
        """ метод удаления вопроса Task по его порядковому номеру"""
        del self.mas[num]

    def printAllTasks(self):
        """ вывод в консоль наборов, для отладки графического интерфейса """
        print('\n\n\nКол-во вопросов в наборе: ', len(self.mas))
        for i in range(len(self.mas)):
            print('\n\nВопрос номер ', i+1, ':')
            print(self.mas[i].vopros)
            print(self.mas[i].otv1)
            print(self.mas[i].otv2)
            print(self.mas[i].otv3)
            print(self.mas[i].otv4)
            print(self.mas[i].otv5)
            print(self.mas[i].prav_otv)
            print(self.mas[i].ball)


# Реализовать операцию слияния двух текстовых наборов,
# операцию пересечения,
# вычисления разности.
# Дополнительно реализовать операцию генерации конкретного обьекта Test обьемом не более К вопросов из обьекта типа TestContent.

def mergeContent(nabor1, nabor2):
    """ вычисляет слияние наборов"""
    naborRes = TextContent()
    for elem in nabor1.mas:
        naborRes.addTask(elem.vopros,
                         elem.otv1,
                         elem.otv2,
                         elem.otv3,
                         elem.otv4,
                         elem.otv5,
                         elem.prav_otv,
                         elem.ball)
    for elem in nabor2.mas:
        naborRes.addTask(elem.vopros,
                         elem.otv1,
                         elem.otv2,
                         elem.otv3,
                         elem.otv4,
                         elem.otv5,
                         elem.prav_otv,
                         elem.ball)
    return naborRes


def intersectionContent(nabor1, nabor2):
    """ вычисляет пересечение наборов"""
    naborRes = TextContent()
    for elem1 in nabor1.mas:
        for elem2 in nabor2.mas:
            if elem1.vopros == elem2.vopros:
                naborRes.addTask(elem1.vopros,
                                 elem1.otv1,
                                 elem1.otv2,
                                 elem1.otv3,
                                 elem1.otv4,
                                 elem1.otv5,
                                 elem1.prav_otv,
                                 elem1.ball)
    return naborRes


def diffContent(nabor1, nabor2):
    """ вычисляет разность наборов"""
    naborRes = TextContent()
    for elem1 in nabor1.mas:
        flag = True
        for elem2 in nabor2.mas:
            if elem1.vopros == elem2.vopros:
                flag = False
        if flag:
            naborRes.addTask(elem1.vopros,
                             elem1.otv1,
                             elem1.otv2,
                             elem1.otv3,
                             elem1.otv4,
                             elem1.otv5,
                             elem1.prav_otv,
                             elem1.ball)

    return naborRes


def generateTest(nabor, k):
    """ генерация конкретного объекта Test объемом не более К вопросов из объекта типа TestContent"""
    test = TextContent()
    randomNums = list(range(len(nabor.mas)))
    random.shuffle(randomNums)  # формируем список из не более чем К случайных номеров вопросов
    for i in randomNums[:k]:
        test.addTask(nabor.mas[i].vopros,
                     nabor.mas[i].otv1,
                     nabor.mas[i].otv2,
                     nabor.mas[i].otv3,
                     nabor.mas[i].otv4,
                     nabor.mas[i].otv5,
                     nabor.mas[i].prav_otv,
                     nabor.mas[i].ball)
    return test

# Далее - графический интерфейс приложения
class AddTaskDialog(QtWidgets.QDialog):  # Окно добавления вопросов в набор
    def __init__(self):
        super().__init__()
        uic.loadUi("AddTaskDialog.ui", self)


class MainWindow(QtWidgets.QMainWindow):  # графический интерфейс главного окна на Qt5
    def __init__(self):
        super().__init__()
        uic.loadUi("MainForm.ui", self)
        self.nabor1 = TextContent()
        self.nabor2 = TextContent()
        self.naborRes = TextContent()

        # сигналы, посылаемые кнопками главного окна
        self.pushButtonOpen.clicked.connect(self.open_file_window_nabor)
        self.pushButtonAdd.clicked.connect(self.show_dialog_add_task_nabor)
        self.pushButtonDel.clicked.connect(self.del_task_nabor1)
        self.pushButtonGet.clicked.connect(self.get_task_nabor1)
        self.pushButtonGenerateTest.clicked.connect(self.generare_test_nabor)
        self.pushButtonSave.clicked.connect(self.save_file_window_nabor)

        self.pushButtonOpen_2.clicked.connect(self.open_file_window_nabor)
        self.pushButtonAdd_2.clicked.connect(self.show_dialog_add_task_nabor)
        self.pushButtonDel_2.clicked.connect(self.del_task_nabor2)
        self.pushButtonGet_2.clicked.connect(self.get_task_nabor2)
        self.pushButtonGenerateTest_2.clicked.connect(self.generare_test_nabor)
        self.pushButtonSave_2.clicked.connect(self.save_file_window_nabor)

        self.pushButtonMerge.clicked.connect(self.merge_nabor)
        self.pushButtonIntersection.clicked.connect(self.intersection_nabor)
        self.pushButtonDiff.clicked.connect(self.diff_nabor)
        self.pushButtonSave_3.clicked.connect(self.save_file_window_nabor)

    def open_file_window_nabor(self):
        """ открываем файл txt, считываем из него строки и заполняем набор вопросов"""
        sender = self.sender()
        if sender.objectName() == 'pushButtonOpen':
            self.nabor1 = TextContent()  # вызываем конcтруктор класса TestContent
            self.nab = self.nabor1
            self.pl = self.plainTextEdit
            self.sbg = self.spinBoxGet
            self.sbd = self.spinBoxDel

        if sender.objectName() == 'pushButtonOpen_2':
            self.nabor2 = TextContent()  # вызываем конcтруктор класса TestContent
            self.nab = self.nabor2
            self.pl = self.plainTextEdit_2
            self.sbg = self.spinBoxGet_2
            self.sbd = self.spinBoxDel_2

        fname = ''
        # открываем системное окно выбора файла
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'nabor.txt')[0]
        if fname != '':
            num = 0
            n = 0
            # считываем количество строк в файле
            with open(fname) as f:
                for t in f.read():
                    if t == '\n':
                        n += 1
            # делим число строк без остатка на 8, чтобы узнать количество полностью заполненных Task-ов
            n = (n + 1) // 8
            # заполняем массив Task-ов нашими вопросами из файла
            with open(fname) as f:
                for num in range(n):
                    self.nab.addTask(f.readline()[:-1],  # [:-1] обрезает последний символ перевода строки
                                     f.readline()[:-1],
                                     f.readline()[:-1],
                                     f.readline()[:-1],
                                     f.readline()[:-1],
                                     f.readline()[:-1],
                                     int(f.readline()),
                                     int(f.readline()))
            # меняем максимальное число значаний числового переключателя на главном окне, соотв. кол-ву вопросов
            self.sbg.setMinimum(1)
            self.sbg.setMaximum(n)
            self.sbd.setMinimum(1)
            self.sbd.setMaximum(n)
            self.upd_qtext(self.pl, self.nab)   

    def show_dialog_add_task_nabor(self):
        """ открывает диалоговое окно для добавления Task в набор"""
        sender = self.sender()
        if sender.objectName() == 'pushButtonAdd':
            add = AddTaskDialog()
            add.exec()  # делает окно модальным
            add.show()
            ok = add.exec_()
            # Если была нажата клавиша Ок, то считываем введенные значения
            if ok:
                self.nabor1.addTask(add.lineEditVopros.text(),
                                    add.lineEditOtv1.text(),
                                    add.lineEditOtv2.text(),
                                    add.lineEditOtv3.text(),
                                    add.lineEditOtv4.text(),
                                    add.lineEditOtv5.text(),
                                    add.spinBoxPrav_otv.value(),
                                    add.spinBoxBall.value())
                self.upd_qtext(self.plainTextEdit, self.nabor1)
                self.spinBoxGet.setMaximum(self.spinBoxDel.maximum() + 1)
                self.spinBoxDel.setMaximum(self.spinBoxDel.maximum() + 1)
        if sender.objectName() == 'pushButtonAdd_2':
            add = AddTaskDialog()
            add.show()
            ok = add.exec_()
            # Если была нажата клавиша Ок, то считываем введенные значения
            if ok:
                self.nabor2.addTask(add.lineEditVopros.text(),
                                    add.lineEditOtv1.text(),
                                    add.lineEditOtv2.text(),
                                    add.lineEditOtv3.text(),
                                    add.lineEditOtv4.text(),
                                    add.lineEditOtv5.text(),
                                    add.spinBoxPrav_otv.value(),
                                    add.spinBoxBall.value())
                self.upd_qtext(self.plainTextEdit_2, self.nabor2)
                self.spinBoxGet_2.setMaximum(self.spinBoxDel_2.maximum() + 1)
                self.spinBoxDel_2.setMaximum(self.spinBoxDel_2.maximum() + 1)

    def del_task_nabor1(self):
        # удаляем вопрос из набора1 по номеру из числового переключателя в главном окне
        num = self.spinBoxDel.value()
        self.nabor1.delTask(num - 1)
        self.spinBoxGet.setMaximum(self.spinBoxGet.maximum() - 1)
        self.spinBoxDel.setMaximum(self.spinBoxDel.maximum() - 1)
        self.upd_qtext(self.plainTextEdit, self.nabor1)

    def del_task_nabor2(self):
        # удаляем вопрос из набора2 по номеру из числового переключателя в главном окне
        num = self.spinBoxDel_2.value()
        self.nabor2.delTask(num - 1)
        self.spinBoxGet_2.setMaximum(self.spinBoxGet_2.maximum() - 1)
        self.spinBoxDel_2.setMaximum(self.spinBoxDel_2.maximum() - 1)
        self.upd_qtext(self.plainTextEdit_2, self.nabor2)

    def get_task_nabor1(self):
        # получаем вопрос из набора1 по номеру из числового переключателя в главном окне
        self.naborRes = TextContent()
        num = int(self.spinBoxGet.value())
        self.naborRes.mas.append(self.nabor1.getTask(num-1))
        self.upd_qtext(self.plainTextEdit_3, self.naborRes)

    def get_task_nabor2(self):
        # получаем вопрос из набора2 по номеру из числового переключателя в главном окне
        self.naborRes = TextContent()
        num = int(self.spinBoxGet_2.value())
        self.naborRes.mas.append(self.nabor2.getTask(num-1))
        self.upd_qtext(self.plainTextEdit_3, self.naborRes)

    def generare_test_nabor(self):
        # генерируем вопросы количеством не более, чем задано числовым переключателя в главном окне
        sender = self.sender()
        if sender.objectName() == 'pushButtonGenerateTest':
            self.nabor = self.nabor1
            k = int(self.spinBoxGenerateTest.value())
        if sender.objectName() == 'pushButtonGenerateTest_2':
            self.nabor = self.nabor2
            k = int(self.spinBoxGenerateTest_2.value())

        self.naborRes = TextContent()
        self.naborRes = generateTest(self.nabor, k)
        self.upd_qtext(self.plainTextEdit_3, self.naborRes)

    def save_file_window_nabor(self):
        """ сохраняем в файл txt набор из объекта-набора TextContent"""
        sender = self.sender()
        if sender.objectName() == 'pushButtonSave':
            self.nab = self.nabor1
        if sender.objectName() == 'pushButtonSave_2':
            self.nab = self.nabor2
        if sender.objectName() == 'pushButtonSave_3':
            self.nab = self.naborRes

        fsavename = ''
        # открывает окно сохранения файла
        fsavename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 'nabor.txt')[0]
        if fsavename != '':
            with open(fsavename, 'w+') as fsav:
                # пишем построчно каждый Task в файл
                for str in self.nab.mas:
                    fsav.write('%s\n' % str.vopros)
                    fsav.write('%s\n' % str.otv1)
                    fsav.write('%s\n' % str.otv2)
                    fsav.write('%s\n' % str.otv3)
                    fsav.write('%s\n' % str.otv4)
                    fsav.write('%s\n' % str.otv5)
                    fsav.write('%s\n' % str.prav_otv)
                    fsav.write('%s\n' % str.ball)

    def merge_nabor(self):
        self.naborRes = TextContent()
        self.naborRes = mergeContent(self.nabor1, self.nabor2)
        self.upd_qtext(self.plainTextEdit_3, self.naborRes)

    def intersection_nabor(self):
        self.naborRes = TextContent()
        self.naborRes = intersectionContent(self.nabor1, self.nabor2)
        self.upd_qtext(self.plainTextEdit_3, self.naborRes)

    def diff_nabor(self):
        self.naborRes = TextContent()
        self.naborRes = diffContent(self.nabor1, self.nabor2)
        self.upd_qtext(self.plainTextEdit_3, self.  naborRes)

    def upd_qtext(self, qtobj, nabor):
        """ выводит/обновляет на экран набор вопросов в соответствующем QPlainEditText"""
        qtobj.clear()
        for i in range(len(nabor.mas)):
            # В txt-файле вопрос/ответы/номер-правильного/баллы отделяются только переводом строки,
            # Данный метод оформляет вывод текста на экран:
            qtobj.insertPlainText(nabor.mas[i].vopros+'\n\n')
            qtobj.insertPlainText('1 - '+nabor.mas[i].otv1+'\n')
            qtobj.insertPlainText('2 - '+nabor.mas[i].otv2+'\n')
            qtobj.insertPlainText('3 - '+nabor.mas[i].otv3+'\n')
            qtobj.insertPlainText('4 - '+nabor.mas[i].otv4+'\n')
            qtobj.insertPlainText('5 - '+nabor.mas[i].otv5+'\n')
            qtobj.insertPlainText('\nПравильный ответ:  '+str(nabor.mas[i].prav_otv)+'\n')
            qtobj.insertPlainText('Начисляемый балл:  '+str(nabor.mas[i].ball)+'\n\n\n')


def main():  # создание экземпляра главного окна, запуск и инициализация программы
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
