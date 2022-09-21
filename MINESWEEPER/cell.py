from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    #List of Instances we created 
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False 
        self.is_mine_candidate = False
        self.cell_button_object = None
        self.x = x
        self.y = y

        # Append the object to Cell.all list
        Cell.all.append(self)
    
    def create_button_object(self, location):
        btn = Button(
        location,
        width = 3,
        height=1)
        btn.bind('<Button-1>', self.left_click_action) # Left Click 
        btn.bind('<Button-2>', self.left_click_action) # Right Click
        self.cell_button_object = btn
    
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_action(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'You have WON THE GAME','Game Over',0)

        # Cancel Right / Left Click event when cell is open
        self.cell_button_object.unbind('<Button-1>')
        self.cell_button_object.unbind('<Button-2>')
    
    def get_cell_by_axis(self, x, y):
        # Return cell object based on  value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1),
            self.get_cell_by_axis(self.x, self.y+1)
        ]
        
        cells = [cell for cell in cells if cell is not None]
        return cells
    
    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter


    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_button_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of cell count label with the new count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f'Cells Left:{Cell.cell_count}')
        self.cell_button_object.configure(bg='SystemButtonFace')
        
        self.is_opened = True
    
    def show_mine(self):
        # A logic to interrupt the game to display a message that player lost!
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a MINE', 'Game Over', 0)
        sys.exit()
        self.cell_button_object.configure(bg='red')

    def right_click_action(self, event):
        if not self.is_mine_candidate:
            self.cell_button_object.configure(
                bg='orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_button_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True  

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"