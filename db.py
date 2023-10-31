import sqlite3


class CarNumber:

    def create_table(self):
        con = sqlite3.connect('LicensePlates.db')
        with con:
            cursor = con.cursor()
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS car_numbers(
                            id INTEGER PRIMARY KEY,
                            number TEXT NOT NULL
                        )
                    ''')

    def add_car_number(self, number):
        conn = sqlite3.connect('LicensePlates.db')
        with conn:
            # получаем количество таблиц с нужным нам именем
            data = conn.execute("select count(*) from sqlite_master where type='table' and name='goods'")
            for row in data:
                # если таких таблиц нет
                if row[0] == 0:
                    self.create_table()
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                                INSERT INTO car_numbers(number) VALUES(?)
                            ''', (number,))
                        conn.commit()
                else:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                                INSERT INTO car_numbers(number) VALUES(?)
                            ''', (number,))
                        conn.commit()

    def get_car_numbers(self):
        with sqlite3.connect('LicensePlates.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT * FROM car_numbers
                ''')
            rows = cursor.fetchall()
            return rows

    def main(self, number):
        car_number = CarNumber()
        self.add_car_number(number)
