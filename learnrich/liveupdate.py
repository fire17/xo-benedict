import sys
import random
import time

from rich.live import Live
from rich.table import Table
from rich.console import Console

console = Console()

def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        status = "[red]ERROR" if value < 50 else "[green]SUCCESS"
        table.add_row(
            f"{row}", f"{value:3.2f}", status
        )
    return table

def update_table_color(table: Table) -> Table:
    """Cycle the color of the 'Status' column."""
    for row in table.rows:
        current_status = row.cells[2]
        if "[red]" in current_status.text:
            new_status = current_status.text.replace("[red]", "[green]")
        else:
            new_status = current_status.text.replace("[green]", "[red]")
        row.cells[2].update(new_status)
    return table

run = False
if run:
    with Live(generate_table(), refresh_per_second=4) as live:
        for _ in range(40):
            time.sleep(0.4)
            updated_table = update_table_color(generate_table())
            live.update(updated_table)


