import sqlite3


def get_movies(*years, duration, genre):
    conn = sqlite3.connect('films_db.sqlite')
    c = conn.cursor()
    query = (f"SELECT genre, title, year, duration FROM films "
             f"WHERE duration >= {duration} "
             f"AND year IN ({','.join('?' * len(years))})"
             f"AND genre in(SELECT id FROM genres WHERE title='{genre}') ORDER BY duration, title")
    films = c.execute(query, years).fetchall()
    conn.close()
    return films


print(get_movies(1999, 2000, 2001, 2002, 2003, 2004, 2005, duration=100, genre='фантастика'))
