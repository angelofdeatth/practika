import json
import os
import sys

FILE = "cinema.json"

# сеансы которые создаем если файла нет
defolt = [
    {"name": "Дюна-2", "time": "18:00", "price": 400, "total": 50, "sold": 20},
    {"name": 'Гарри Поттер', "time": "20:00", "price": 350, "total": 50, "sold": 38},
    {"name": "Интерстеллар", "time": "22:00", "price": 300, "total": 50, "sold": 45},
]


class Session:
    def __init__(self, name, time, price, total, sold=0):
        self.name = name
        self.time = time
        self.price = price
        self.total = total
        self.sold = sold

    def free(self):
        return self.total-self.sold

    def to_dict(self):
        return {"name": self.name, "time": self.time, "sold": self.sold,
                "price": self.price, "total": self.total}


class Cashier:
    def __init__(self):
        self.sessions = []
        self.load()

    def load(self):
        if os.path.exists(FILE):
            try:
                with open(FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for s in data:
                    self.sessions.append(Session(s['name'], s["time"], s['price'], s["total"], s['sold']))
            except:
                print("файл битый, создаю новые")
                self.create_def()
        else:
            self.create_def()

    def create_def(self):
        self.sessions = []
        for s in defolt:
            self.sessions.append(Session(s["name"], s["time"], s["price"], s["total"], s["sold"]))
        self.save()

    def save(self):
        data = []
        for s in self.sessions:
            data.append(s.to_dict())
        with open(FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def show_list(self):
        print("Сеансы:")
        for i in range(len(self.sessions)):
            s = self.sessions[i]
            # print("отладка", s.sold)
            print("%d) %s, %s, %dр, свободно %d" % (i+1, s.name, s.time, s.price, s.free()))

    def buy(self, nom, k):
        if nom < 1 or nom > len(self.sessions):
            print("Неверный номер сеанса.")
            return False
        sess = self.sessions[nom-1]
        if k <= 0:
            print("Количество должно быть больше 0.")
            return False
        if k > sess.free():
            print("Мест не хватает. Свободно: {}".format(sess.free()))
            return False
        sess.sold = sess.sold + k
        itogo = sess.price * k
        self.save()
        print(f"Итого: {itogo}р. Оплата прошла.")
        return True

    def report(self):
        print("Отчёт:")
        for i, s in enumerate(self.sessions, 1):
            summ = s.sold * s.price
            print(f"{i}) {s.name} — продано {s.sold}, сумма {summ}р")


def main():
    c = Cashier()
    while True:
        print()
        c.show_list()
        print()
        print("1) Купить билет  2) Отчёт  0) Выход")
        choice = input("> ")
        if choice == "1":
            # ввод номера
            try:
                nom = int(input("Номер сеанса: "))
            except ValueError:
                print("Введите число.")
                continue
            try:
                k = int(input("Количество мест: "))
            except ValueError:
                print("Введите число.")
                continue
            c.buy(nom, k)
        elif choice == '2':
            c.report()
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")


1