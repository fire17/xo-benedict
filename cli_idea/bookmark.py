import os
import argparse
from rich.console import Console
from rich.table import Table

BOOKMARKS_FILE = os.path.expanduser("~/.cli_bookmarks")


def save_bookmark(bookmark_name):
    current_folder = os.getcwd()
    with open(BOOKMARKS_FILE, "a") as f:
        f.write(f"{bookmark_name},{current_folder}\n")
    console.print(f"Bookmark '{bookmark_name}' saved for '{current_folder}'", style="green")


def delete_bookmark(bookmark_name):
    try:
        with open(BOOKMARKS_FILE, "r") as f:
            lines = f.readlines()
        with open(BOOKMARKS_FILE, "w") as f:
            for line in lines:
                if not line.startswith(f"{bookmark_name},"):
                    f.write(line)
        console.print(f"Bookmark '{bookmark_name}' deleted", style="red")
    except FileNotFoundError:
        console.print("No bookmarks found.")


def list_bookmarks():
    table = Table(title="Bookmarks")
    table.add_column("Index", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Path", style="green")

    try:
        with open(BOOKMARKS_FILE, "r") as f:
            bookmarks = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        bookmarks = []

    for idx, (name, path) in enumerate(bookmarks, start=1):
        table.add_row(str(idx), name, path)

    console.print(table)


def select_bookmark():
    bookmarks = list_bookmarks()
    if not bookmarks:
        return

    choice = input("Enter the index of the bookmark to select (q to quit): ")
    if choice.lower() == "q":
        return

    try:
        index = int(choice)
        if 1 <= index <= len(bookmarks):
            return bookmarks[index - 1][1]
        else:
            console.print("Invalid index. Please enter a valid index.", style="yellow")
    except ValueError:
        console.print("Invalid input. Please enter a valid index.", style="yellow")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Bookmarks")
    parser.add_argument("bookmark_name", nargs="?", help="Name for the bookmark")
    parser.add_argument("-del", metavar="bookmark_name", help="Delete a bookmark")
    args = parser.parse_args()

    console = Console()

    if args.del_bookmark:
        delete_bookmark(args.del_bookmark)
    elif args.bookmark_name:
        save_bookmark(args.bookmark_name)
    else:
        select_bookmark()
