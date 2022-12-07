#!/usr/bin/python
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import datetime
import psycopg2
from config import config
from connect import connect

console = Console()
app = typer.Typer()
params = config()

def signup(username: str):    
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f"INSERT INTO  public.user (user_name) VALUES ('{username}')"
    cur.execute(sql)
    conn.commit()


def add(book_name: str, author_name: str, pages: int, genre: str):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    time = str(datetime.datetime.now())
    sql = f"""INSERT INTO  public.book (book_name, author_name, pages, genre, availability, book_date_added) 
            VALUES ('{book_name}', '{author_name}', {pages}, '{genre}', True, '{time}')"""
    cur.execute(sql)
    conn.commit()


def delete():
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" DELETE FROM public.book where book_id = 8"""
    cur.execute(sql)
    conn.commit()

def update():
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" UPDATE book SET genre = 'Advanture'
                WHERE book_id = 1
         """
    cur.execute(sql)
    conn.commit()

def get_books(name: str):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" SELECT * FROM public.book 
            WHERE book_name = '{name}'
            """
    cur.execute(sql)
    books = cur.fetchall()
    conn.commit()
    return books

def search_name(name: str):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" SELECT * FROM public.book where book_name = '{name}'
         """
    cur.execute(sql)
    books = cur.fetchall()
    conn.commit()
    return books
def search_author(author: str):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" SELECT * FROM public.book where author_name = '{author}'
         """
    cur.execute(sql)
    books = cur.fetchall()
    conn.commit()
    return books

def recent_added(author):
    list=[]
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" SELECT author_name FROM public.book 
                 """
    cur.execute(sql)
    authors = cur.fetchall()
    r= len((authors))
    for i in range(r):
         list.append(authors[i][0])


    if bool(author) is True:
        if author in list:
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sql = f""" SELECT * FROM public.book where author_name = '{author}'order by book_date_added desc limit 5
                 """
            cur.execute(sql)
            books = cur.fetchall()
            conn.commit()
            return books
        else:
            print("author does not exist!")


    elif bool(author) is False:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = f""" SELECT * FROM public.book order by book_date_added desc limit 5
                     """
        cur.execute(sql)
        books = cur.fetchall()
        conn.commit()
        return books

def mostread_books(genre):
    list=[]
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" SELECT genre FROM public.book 
                 """
    cur.execute(sql)
    genres = cur.fetchall()
    r= len((genres))
    for i in range(r):
         list.append(genres[i][0])


    if bool(genre) is True:
        if genre in list:
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sql = f"""select b.book_id, b.book_name, b.author_name,b.genre, c.count
from public.book as b
join (SELECT book_id, count(mark_read) FROM command GROUP BY book_id) as c
on b.book_id = c.book_id 
where genre = '{genre}' order by c.count desc limit 10
                 """
            cur.execute(sql)
            books = cur.fetchall()
            conn.commit()
            return books
        else:
            print("genre does not exist!")


    elif bool(genre) is False:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = f""" select b.book_id, b.book_name, b.author_name,b.genre, c.count
from public.book as b
join (SELECT book_id, count(mark_read) FROM command GROUP BY book_id) as c
on b.book_id = c.book_id 
order by c.count desc limit 10
                     """
        cur.execute(sql)
        books = cur.fetchall()
        conn.commit()
        return books

def most_favorite(genre):
    list=[]
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" SELECT genre FROM public.book 
                 """
    cur.execute(sql)
    genres = cur.fetchall()
    r= len((genres))
    for i in range(r):
         list.append(genres[i][0])


    if bool(genre) is True:
        if genre in list:
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            sql = f"""select b.book_id, b.book_name, b.author_name,b.genre, c.count
from public.book as b
join (SELECT book_id, count(fav_book) FROM command GROUP BY book_id) as c
on b.book_id = c.book_id 
where genre = '{genre}' order by c.count desc limit 10
                 """
            cur.execute(sql)
            books = cur.fetchall()
            conn.commit()
            return books
        else:
            print("genre does not exist!")


    elif bool(genre) is False:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = f""" select b.book_id, b.book_name, b.author_name,b.genre, c.count
from public.book as b
join (SELECT book_id, count(fav_book) FROM command GROUP BY book_id) as c
on b.book_id = c.book_id 
order by c.count desc limit 10
                     """
        cur.execute(sql)
        books = cur.fetchall()
        conn.commit()
        return books

def mostread_genres():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f"""select b.genre, sum(c.count)
from public.book as b
join (SELECT book_id, count(mark_read) FROM command GROUP BY book_id) as c
on b.book_id = c.book_id
GROUP BY genre order by sum desc limit 5
                 """
    cur.execute(sql)
    books = cur.fetchall()
    conn.commit()
    return books
def mostread_authors():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f"""select b.author_name, sum(c.count)
from public.book as b
join (SELECT book_id, count(mark_read) FROM command GROUP BY book_id) as c
on b.book_id = c.book_id
GROUP BY author_name order by sum desc limit 5
                 """
    cur.execute(sql)
    books = cur.fetchall()
    conn.commit()
    return books

def markread(book_id: int, user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" 
        INSERT INTO public.command (book_id, user_id, mark_read) VALUES ({book_id}, {user_id}, 'True'); 
        """

    cur.execute(sql)
    conn.commit()

def markreading(book_id: int, user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" 
        INSERT INTO public.command (book_id, user_id, mark_reading) VALUES ({book_id}, {user_id}, 'True');
        """

    cur.execute(sql)
    conn.commit()

def mark_willread(book_id: int, user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" 
        INSERT INTO public.command (book_id, user_id, mark_will_read) VALUES ({book_id}, {user_id}, 'True');
        """
    cur.execute(sql)
    conn.commit()

def fav_books(book_id: int, user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = f""" 
        INSERT INTO public.command (book_id, user_id, fav_book) VALUES ({book_id}, {user_id}, 'True');
        """
    try:    
        cur.execute(sql)
        conn.commit()
    except:
        sql = f""" 
        UPDATE public.command SET fav_book = 'True' 
        WHERE book_id = {book_id} and user_id = {user_id}
        """
        cur.execute(sql)
        conn.commit()

def my_book_read(user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql1 = f"""
        SELECT 
                command.book_id,
                book_name,
                author_name,
                pages,
                genre,
                availability
        FROM command 
        INNER JOIN book ON command.book_id = book.book_id
        WHERE mark_read = 'True' and user_id= {user_id}
        """
    cur.execute(sql1)
    books = cur.fetchall()
    conn.commit()
    return books

def my_book_reading(user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql1 = f"""
        SELECT 
                command.book_id,
                book_name,
                author_name,
                pages,
                genre,
                availability
        FROM command 
        INNER JOIN book ON command.book_id = book.book_id
        WHERE mark_reading = 'True' and user_id= {user_id}
        """
    cur.execute(sql1)
    books = cur.fetchall()
    conn.commit()
    return books

def my_book_will_read(user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql1 = f"""
        SELECT 
                command.book_id,
                book_name,
                author_name,
                pages,
                genre,
                availability
        FROM command 
        INNER JOIN book ON command.book_id = book.book_id
        WHERE mark_will_read = 'True' and user_id= {user_id}
        """
    cur.execute(sql1)
    books = cur.fetchall()
    conn.commit()
    return books

def my_fav_book(user_id: int):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql1 = f"""
        SELECT 
                command.book_id,
                book_name,
                author_name,
                pages,
                genre,
                availability
        FROM command 
        INNER JOIN book ON command.book_id = book.book_id
        WHERE fav_book = 'True' and user_id= {user_id}
        """
    cur.execute(sql1)
    books = cur.fetchall()
    conn.commit()
    return books
    
