import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from connect import connect
import psycopg2
from config import config
import datetime
from database import add, delete, signup, update, get_books


console = Console()
app = typer.Typer()


@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    connect()


@app.command("sign_up")
def sign_up(username: str):
    typer.echo(f"Nice that you are signing up!")
    signup(username)


@app.command("add_book")
def add_book():
    typer.echo(f"Book is added!")
    add()


@app.command("delete_book")
def delete_book():
    typer.echo(f"Book is deleted!")
    delete()


@app.command("update_book")
def update_book():
    typer.echo(f"Book is updated!")
    update() 
   
   
# Example function for tables, you can add more columns/row.

@app.command("get_book")
def get_book():
    typer.echo(f"Books are displayed!")
    books = get_books()
    print(books)
    display_table(books)


def display_table(books):


    table = Table(show_header=True, header_style="bold blue")
   
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)
    
    for book in books:
        table.add_row(str(book[0]),book[1], book[2], str(book[3]), book[4], str(book[5]), book[6])
    
    

    console.print(table)

if __name__ == "__main__":
    app()
    

