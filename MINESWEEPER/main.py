from tkinter import *
import settings
import utils
from cell import Cell

root = Tk()
# Override the window settings
root.configure(bg='black')
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("MineSweeper")
root.resizable(False,False)

top_frame = Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height= utils.height_percent(25)
)
top_frame.place(x= 0, y=0)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text=' Mine Sweeper',
    font=('',48)
)

game_title.place(x=utils.width_percent(25),y=0)

left_frame = Frame(
    root,
    bg='black', 
    width =utils.width_percent(25),
    height=utils.height_percent(75)
)
left_frame.place(x=0,y=utils.height_percent(25))

center_frame= Frame(
    root, 
    bg='black',
    width = utils.width_percent(75),
    height = utils.height_percent(75) 
)
center_frame.place(x=utils.width_percent(25),y=utils.height_percent(25))

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_button_object(center_frame)
        c.cell_button_object.grid(column=x,row=y)

# Call the Label From the Cell Class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0,y=0)

Cell.randomize_mines()
for c in Cell.all:
    print(c.is_mine)

#Run the Window
root.mainloop()