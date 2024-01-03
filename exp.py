from tkinter import *

root = Tk()

# Define a Tkinter variable

tkvar = StringVar(root)
# Dictionary with options
choices = {'Option 1', 'Option 2', 'Option 3'}
tkvar.set('Option 1')  # set the default option

popupMenu = OptionMenu(root, tkvar, *choices)
Label(root, text="Choose an option").grid(row=1, column=1)
popupMenu.grid(row=2, column=1)

# on change dropdown value
def change_dropdown(*args):
   print(tkvar.get())

# link function to change dropdown
tkvar.trace_add('write', change_dropdown)

root.mainloop()