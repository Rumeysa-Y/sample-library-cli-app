import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from connect import connect
import psycopg2
from config import config
import datetime

console = Console()
app = typer.Typer()



def signup(username: str):    
    conn = psycopg2.connect("dbname=Group2DB user=postgres password=postgres")
    cur = conn.cursor()
    sql = f"INSERT INTO  public.user (user_name) VALUES ('{username}')"
    cur.execute(sql)
    conn.commit()



def add():
    conn = psycopg2.connect("dbname=Group2DB user=postgres password=postgres")
    cur = conn.cursor()
    sql = f"""INSERT INTO  public.book (book_name, author_name, pages, genre, availability) 
            VALUES ('Hayat uzerine dusunceler', 'Tolstoy', 176, 'Thought', True)"""
    cur.execute(sql)
    conn.commit()


def delete():
    conn = psycopg2.connect("dbname=Group2DB user=postgres password=postgres")
    cur = conn.cursor()
    sql = f""" DELETE FROM public.book where book_id = 3"""
    cur.execute(sql)
    conn.commit()


def update():
    conn = psycopg2.connect("dbname=Group2DB user=postgres password=postgres")
    cur = conn.cursor()
    sql = f""" UPDATE book SET genre = 'Advanture'
                WHERE book_id = 1
         """
    cur.execute(sql)
    conn.commit()


def get_books():
    conn = psycopg2.connect("dbname=Group2DB user=postgres password=postgres")
    cur = conn.cursor()
    sql = f""" SELECT * FROM book
         """
    cur.execute(sql)
    books = cur.fetchall()
    conn.commit()
    return books









  
    
