import wx #loads the GUI so tht  we can create windows,panels and buttons
from wx.lib.buttons import GenButton #customizable button class
#GenButton->its more flexible than wx.Button & allows to customize buttons
import create_val_fxn
##imports the file that has the values of our sudoku
import time #to track elapsed time

app = wx.App(False)
Frame = wx.Frame(None, title="SUDOKU", size=(600,600))
panel1 = wx.Panel(Frame)
panel1.SetBackgroundColour('thistle')

#***********************************************************************

intro = wx.StaticText(
        panel1,
        label=f"Welcome to Sudoku!\nChoose your level to begin.",pos=(220,90),
        style=wx.ALIGN_CENTER)
intro.SetFont(wx.Font(12,wx.FONTFAMILY_SCRIPT,wx.FONTSTYLE_NORMAL,wx.BOLD,faceName='Times New Roman'))
intro.SetForegroundColour('Classic Lavender') #text color


#***********************************************************************

# Dialog + callback
def on_click(event):
    dlg = wx.Dialog(None, title="Initializing", size=(250,120))
    panel = wx.Panel(dlg) #creates a panel inside the dialog box
    wx.StaticText(panel, label='loading board...', pos=(30,30))
    global level_chosen
    level_chosen = event.GetEventObject().GetLabel() #reads the label of the button clicked
    
    timer = wx.Timer(dlg) #ties timer to the dialog box
    def on_timeout(event):
        timer.Stop()
        dlg.Close()
    dlg.Bind(wx.EVT_TIMER, on_timeout, timer)
    timer.Start(2000)
    
    dlg.ShowModal() #blocks interaction with main window until dlg is closed
    dlg.Destroy()
    sudokuboard()
#***********************************************************************

# Button creation helper

def button_create(level, x_co, y_co):
    btn = GenButton(panel1, label=level, pos=(x_co,y_co), size=(120,40))
    btn.SetBezelWidth(8) #sets border thickness
    btn.SetBackgroundColour("lavender") #button bg color
    btn.SetForegroundColour("violet") 
    return btn

btn1 = button_create("Easy",250,150)
btn2 = button_create("Medium",250,200)
btn3 = button_create("Hard",250,250)

btn1.Bind(wx.EVT_BUTTON,on_click)
btn2.Bind(wx.EVT_BUTTON,on_click)
btn3.Bind(wx.EVT_BUTTON,on_click)

#***********************************************************************
# Replace panel contents with Sudoku grid
def sudokuboard():
    global solution,puzzle
    #extracting puzzle and solution boards from create_val_fxn.py
    solution,puzzle=create_val_fxn.val(level_chosen)   

    panel1.DestroyChildren()   # remove all buttons
    panel1.SetBackgroundColour('thistle')
    # Outer box sizer to control margins
    outer_sizer = wx.BoxSizer(wx.VERTICAL) #stacks widgets vertically
    # Add top margin
    outer_sizer.AddSpacer(20)

    def only_digits(event):
        ctrl = event.GetEventObject() #Gets the actual widget (the TextCtrl) where the key was typed
        value = ctrl.GetValue() #Reads the current text inside that box
    # Keep only digits 1-9
        if value and (not value.isdigit() or value == "0"):  # value - makes sure the box isn't empty.
            ctrl.SetValue("")   # clear invalid input
        event.Skip() # allow the event to be processed further


    grid = wx.GridSizer(9, 9, 5, 5)  # rows, cols, vgap, hgap
    for r in range(9):
        row_cells = []
        for c in range(9):
            txt = wx.TextCtrl(panel1, style = wx.TE_CENTER)
            txt.SetMaxLength(1)
            txt.SetMinSize((40,40))   # make each cell square-ish
            txt.Bind(wx.EVT_TEXT, only_digits)   # validate after text changes
            
            value_in_sudoku = puzzle[r][c]
            if value_in_sudoku != 0:
                txt.SetValue(str(value_in_sudoku))
                txt.Disable()
                txt.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
            row_cells.append(txt)


            grid.Add(txt, 1, wx.EXPAND)  #places the cell in the grid

    def go_back(event):
        panel1.Hide()
        # Recreate the initial buttons
        panel1.DestroyChildren()
        panel1.SetBackgroundColour('thistle')
        btn1 = button_create("Easy",250,150)
        btn2 = button_create("Medium",250,200)
        btn3 = button_create("Hard",250,250)

        btn1.Bind(wx.EVT_BUTTON,on_click)
        btn2.Bind(wx.EVT_BUTTON,on_click)
        btn3.Bind(wx.EVT_BUTTON,on_click)
        panel1.Show()
        Frame.Layout()


    btn_back=button_create("Back",10,515)
    btn_back.Bind(wx.EVT_BUTTON, go_back)


    #TIMER LOGIC
    start_time = time.time() #when the timer starts
    timer_text=wx.StaticText(panel1,label='Time: 00:00',pos=(480,5))
    timer_text.SetForegroundColour('Deep Thistle') #text color
    timer_text.SetFont(wx.Font(12,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    
    # store start time in a mutable list
    timer=wx.Timer(panel1) #creates a timer object associated with panel1

    def update_timer(event):
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        timer_text.SetLabel(f"Time: {mins:02d}:{secs:02d}")

    panel1.Bind(wx.EVT_TIMER, update_timer, timer)
    timer.Start(1000)  # update every 1 second
    
    #end timer 

    def on_submit(event):
        timer.Stop()
        final_time = int(time.time() - start_time)   # store total seconds
        

        final_panel(event,final_time,solution)
          
    btn_submit=button_create('Submit',460,515)
    btn_submit.Bind(wx.EVT_BUTTON,on_submit)


    # Put the grid inside the outer sizer with side margins
    outer_sizer.Add(grid, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 50)

    # Add bottom margin at the bottom
    outer_sizer.AddSpacer(50)

    panel1.SetSizer(outer_sizer)  # clear any existing sizer

    panel1.Layout()
    Frame.Layout()

#***********************************************************************

def final_panel(event,final_time,solution):
    panel1.DestroyChildren()
    panel1.SetBackgroundColour('thistle')

    # Show solved Sudoku grid
    solved_grid = wx.GridSizer(9, 9, 5, 5)  # 9x9 with spacing
    for r in range(9):
        for c in range(9):
            # Each cell from original_board

            value_in_sudoku = solution[r][c]
            val = str(value_in_sudoku) if value_in_sudoku != 0 else ""
            # Create a read-only text box for each cell
            txt = wx.TextCtrl(panel1, value=val,style=wx.TE_CENTER | wx.TE_READONLY)
            txt.SetMinSize((30, 30))
            txt.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            solved_grid.Add(txt, 1, wx.EXPAND)
            

    
    mins, secs = divmod(final_time, 60) #divmod-splits seconds into minutes and seconds.
    formatted_time = f"{mins:02d}:{secs:02d}" #format the time as mm:ss- makes it look like a stopwatch
    conclusion = wx.StaticText(
        panel1,
        label=f"Thank you for playing!\nYou took {formatted_time} to finish!\nHope you had a wonderful time!",pos=(150,400),
        style=wx.ALIGN_CENTER)
    #a StaticText widget on panel1 to show the thank-you message
    #creates the thank-you message and shows the time taken.
    #style=wx.ALIGN_CENTER centers the text horizontally

    conclusion.SetFont(wx.Font(12,wx.FONTFAMILY_SCRIPT,wx.FONTSTYLE_NORMAL,wx.BOLD,faceName='Times New Roman'))
    conclusion.SetForegroundColour('Classic Lavender') #text color

    # Outer sizer to hold grid + message
    outer_sizer = wx.BoxSizer(wx.VERTICAL)
    outer_sizer.AddSpacer(20)
    outer_sizer.Add(solved_grid, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 50)
    outer_sizer.AddSpacer(20)
    outer_sizer.Add(conclusion, 0, wx.ALIGN_CENTER | wx.ALL, 20)

    panel1.SetSizer(outer_sizer)
    panel1.Layout()
    Frame.Layout()

    
#***********************************************************************


Frame.Show()
app.MainLoop()