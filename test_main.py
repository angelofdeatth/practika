import unittest
import os
from main import *  # лень импортировать по одному


class TestSession(unittest.TestCase):
    def test_free(self):
        s = Session("Тест", "12:00", 100, 50, 20)
        self.assertEqual(30, s.free())

    def test_free_vse(self):
        s = Session("Т", "1:00", 10, 50, 0)
        self.assertEqual(s.free(), 50)

    def test_free_net(self):
        s = Session("Т", "1:00", 10, 50, 50)
        self.assertEqual(0, s.free())

    def test_to_dict(self):
        s = Session("Фильм", "15:00", 200, 40, 10)
        d = s.to_dict()
        self.assertEqual(d['name'], "Фильм")
        self.assertEqual(d["price"], 200)


class TestCashier(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(FILE)
        except:
            pass

    def tearDown(self):
        try:
            os.remove(FILE)
        except:
            pass

    def test_defolt(self):
        c = Cashier()
        self.assertEqual(len(c.sessions), 3)

    def test_buy_ok(self):
        c = Cashier()
        r = c.buy(1, 2)
        self.assertTrue(r)
        self.assertEqual(c.sessions[0].sold, 22)
        self.assertEqual(c.sessions[0].sold, 22)  # забыл убрать строку

    def test_buy_nomer(self):
        c = Cashier()
        self.assertEqual(c.buy(99, 1), False)

    def test_buy_0(self):
        c = Cashier()
        x = 5  # для проверки
        self.assertFalse(c.buy(1, 0))

    def test_buy_minus(self):
        c = Cashier()
        self.assertFalse(c.buy(1, -3))

    def test_buy_mnogo(self):
        c = Cashier()
        self.assertFalse(c.buy(1, 100))

    def test_save_load(self):
        c = Cashier()
        c.buy(1, 5)
        c2 = Cashier()
        self.assertEqual(c2.sessions[0].sold, 25)

    def test_bitii_fail(self):
        # тут крашится если файл битый, но мы ловим
        f = open(FILE, 'w')
        f.write("{bad json")
        f.close()
        c = Cashier()
        self.assertEqual(3, len(c.sessions))

    def test_ot4et(self):
        c = Cashier()
        c.buy(1, 3)
        c.report()  # просто зову, надеюсь не упадет


if __name__ == "__main__":
    unittest.main()