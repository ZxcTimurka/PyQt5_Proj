import sqlite3
import time


class CarNumber:

    def create_table(self):
        con = sqlite3.connect('LicensePlates.db')
        with con:
            cursor = con.cursor()
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS car_numbers(
                            id INTEGER PRIMARY KEY,
                            number TEXT,
                            date TEXT,
                            file TEXT
                        )
                    ''')

    def add_car_number(self, number, timee, file_path):
        conn = sqlite3.connect('LicensePlates.db')
        with conn:
            data = conn.execute("select count(*) from sqlite_master where type='table' and name='goods'")
            for row in data:
                if row[0] == 0:
                    self.create_table()
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                                INSERT INTO car_numbers(number, date, file) VALUES(?, ?, ?)
                            ''', (number, timee, file_path))
                        conn.commit()
                else:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                                INSERT INTO car_numbers(number, date, file) VALUES(?, ?, ?)
                            ''', (number, timee, file_path))
                        conn.commit()

    def get_car_numbers(self):
        with sqlite3.connect('LicensePlates.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT * FROM car_numbers
                ''')
            rows = cursor.fetchall()
            return rows

    def main(self, number, file_path):
        car_number = CarNumber()
        timee = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())
        self.add_car_number(number, timee, file_path)
