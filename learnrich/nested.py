from ctypes import alignment
from rich import print
from rich.tree import Tree
from rich.table import Table

# Example 1: Nesting a Tree inside a Table
table = Table(min_width=30,title_style="bold gold",style="yellow")
table.title = "[bold #FF00FF]Beautiful[/bold #FF00FF]\n[cyan]This is where some data goes"
table.add_column("ID", style="cyan", justify="center",max_width=1, no_wrap = True, header_style="green")
table.add_column("Name", style="magenta")
table.add_row("A", "Alice",style="#FA00AF")
table.add_row("2", "Bob")
print(table)

tree = Tree("Root")
tree.add("Child 1").add("n2").add("n3").add(table)  # Nesting the table inside the tree
tree.add(table)  # Nesting the table inside the tree
tree.add("Child 2")
print(tree)

# Example 2: Nesting a Table inside a Tree
nested_table = Table()
nested_table.title = "Nice\nCool"
nested_table.caption = "caption"
nested_table.add_column("IDs", style="green")
nested_table.add_column("Values",width=60)
nested_table.add_row("A", "1")
nested_table.add_row("B", tree)
nested_table.add_row("C", "3")

nested_tree = Tree("Root")
nested_tree.add("Child 1",)
nested_tree.add(nested_table) # YO YO YO  # Nesting the table inside the tree
nested_tree.add("Child 2")

print(nested_tree)

# Example 3: Mixed Nested Structures
mixed_tree = Tree("Root")
mixed_tree.add("Child 1")
mixed_tree.add("Child 2")

mixed_table = Table()
mixed_table.add_column(tree, style="blue")
mixed_table.add_column("Age", style="red")
mixed_table.add_row("Alice", "30")
mixed_table.add_row("Bob", "25")

mixed_tree.add("Mixed Element", mixed_table)  # Nesting the table inside the tree

print(mixed_tree)
