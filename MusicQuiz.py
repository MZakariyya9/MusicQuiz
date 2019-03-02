############################################################################################################################################################################################
#Miscellaneous
import string       # Used during checks to strip special characters
import random       # Generation of random song number
import datetime     # Progress saving
import hashlib      # Password encryption
############################################################################################################################################################################################
#SETUP#

import os, sys
try:os.mkdir('Dependencies')                                                                                # Creates new directory for dependencies if it doesn't exist
except FileExistsError: pass
path = (os.path.dirname(os.path.abspath(__file__))+'\\Dependencies\\')                                      # Retrieves directory, appends Dependencies to it
os.chdir(path)                                                                                              # Changes working directory to 'Dependencies' - program looks for files in path
sys.path.append(path)                                                                                       # Appends path to sys - to import modules

try:from setup import *                                                                                     #Imports module
except:
    from urllib.request import urlretrieve
    try:urlretrieve('https://raw.githubusercontent.com/MZakariyya9/MusicQuiz/master/setup.py','setup.py')   #Downloads if it doesn't exist
    except:
        print("Please allow outbound connections to raw.githubusercontent.com")                             #Error if it can't
        raise SystemExit
    else:from setup import *

############################################################################################################################################################################################
#GUI FRAME SWITCHER#
import tkinter as tk
from tkinter import messagebox

class MusicQuiz(tk.Tk):
    def __init__(self):                                                     # Constructor
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(PlayGame)                                         # Switches to first frame

        tk.Tk.iconbitmap(self,default='music.ico')                          # Application favicon
        tk.Tk.wm_title(self, "Music Quiz")                                  # Application title
        tk.Tk.geometry(self,"900x600")                                      # Frame size
        tk.Tk.resizable(self, False, False)                                 # Locks resizing x,y

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()                                           # Destroys current frame
        self._frame = new_frame                                             # Replaces with new one
        self._frame.pack(expand=True,fill="both")                           # Frame fills entire window
        
############################################################################################################################################################################################
#PLAY GAME SCREEN#
class PlayGame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#1f2431")
        
#Title - MUSIC QUIZ 
        title = tk.Canvas(self,width=450,height=200,bg="#1f2431")
        title.create_text(225,100,fill="white",font="Verdana 35 bold",
                          text="MUSIC QUIZ")
        title.pack(pady=(90,50))
        
#Play Game
        def Button(text,switch,position,padx):                              # Button generator (text , frame to switch to , position , padding)
            tk.Button(self, bg="white", fg="#1f2431", text=text, font="Arial 20 bold", bd=0, command = lambda: master.switch_frame(switch)).pack(padx=padx,side=position)
            
        Button("PLAY GAME",UserAuthentication,"top",0)
        Button("HOW TO PLAY",HowToPlay,"left",(180,0))
        Button("LEADERBOARD",Leaderboard,"left",(10,0))

############################################################################################################################################################################################
class HowToPlay(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white")
        
#Title - HOW TO PLAY
        title = tk.Canvas(self,width=450,height=75,bg="white",highlightbackground="#1f2431")
        title.create_text(225,37.5,fill="#1f2431",font="Verdana 26 bold", text="HOW TO PLAY")
        title.pack(pady=25)

#
        tk.Label(self,text='''The ARTIST is displayed at the top.
You are given the first letter of each word in the song name.
\nYour aim is to enter the rest of the letters correctly for each word.
HINT: The entry width usually corresponds to the length of the word.
\nYou have two guesses;
   - Guess correctly the first time --> 3 points
   - Guess correctly the second time --> 1 point
...or it's game over.
\nLIVES reset to 2 on a new song.
LIVES and SCORE counters are present on the bottom left and right sides respectively.
\nThat's it. Good luck!''',font="Verdana 11",bg="white").pack(pady=30)
        
        backb = tk.Button(self, bg="#1f2431", fg="white", text="BACK", font="Arial 14 bold", bd=0, command = lambda: master.switch_frame(PlayGame)).pack()  #Return button

############################################################################################################################################################################################
#SIGNIN/SIGNUP SCREEN#
class UserAuthentication(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#1f2431")

#Real-time Validation
        var1 = tk.StringVar()                               # Holds value of string (input field)
        max_len = 16                                        # Defines length username is spliced to
        def on_write(*args):                                # Called on write
            x = var1.get()                                  # Retrieves string variable (var1 is defined when creating entry field)
            if len(x)>max_len:
                var1.set(x[:max_len].strip().lower())       # Splices (if greater than 16), removes whitespace, forces lowercase
            else:
                var1.set(x.strip())
                if x != "Enter here...":
                    var1.set(x.lower().strip())
        var1.trace_variable("w",on_write)                   # Traces variable on "w" - calls function on_write
        
        var2 = tk.StringVar()
        max_len2 = 22
        def on_write2(*args):
            y = var2.get()
            if len(y)>max_len2:
                var2.set(y[:max_len2].strip())              # Not forced to lowercase
            else:
                var2.set(y.strip())
        var2.trace_variable("w",on_write2)

#Extras
        def on_entry_click(event):                          # Called when entry field is clicked
            if event.widget.cget("fg") == "grey":           # Checks colour of event that called it (in this case - entry click)
               event.widget.delete(0, "end")                # Deletes characters from 0 to end (placeholder values)
               event.widget.insert(0, '')                   # Ensures field is empty
               event.widget.config(fg = "#1f2431")          # Changes text colour to blue (writing font)
            if password_entry.cget("fg") == "grey":         # On clicking username field, output field at bottom should all be green - this is not the case
                rh1.configure(text=msg,fg="green")          # as placeholder value ("Enter password...") only satisfy two criteria (the rest of the text stay red)
                rh4.configure(text=tick+msg3,fg="green")    # Cheat -> force other text to green as well
        def on_focusout(event):
            if event.widget.get() == '':
                event.widget.insert(0, "Enter here...")     # Replaces placeholder values on focus out
                event.widget.config(fg = "grey")            # Changes text back to grey.

        master.bind("<Return>", lambda event: Authenticate(username_entry.get(),password_entry.get()))          #Binds 'Enter' key to login button (alternative)

#Title - SIGN IN
        title = tk.Canvas(self,width=300,height=75,bg="#1f2431")
        title.create_text(150,37.5,fill="white",font="Verdana 26 bold", text="SIGN IN")
        title.pack(pady=(12.5,40))

#Username Field
        username_text = tk.Label(self,text="Username",bg="#1f2431",bd=0, fg="white", font="Verdana 14 bold")
        username_text.pack(pady=(10,5))
#                                                                                                       var1 - StringVar traceable
        username_entry = tk.Entry(self,bd=0,font="Verdana 14", fg="#1f2431", selectbackground="#1f2431",textvariable=var1, selectforeground="white")
        username_entry.insert(0, "Enter here...")                       # Inserts placeholder values
        username_entry.bind("<FocusIn>", on_entry_click)                # Call on focus change
        username_entry.bind("<FocusOut>", on_focusout)
        username_entry.bind('<Control-v>', lambda e: 'break')           # Disables pasting text as this allows entering of whitespace
        username_entry.config(fg = 'grey')                              # Default (focus out) text colour
        username_entry.pack()

#Password Field
        password_text = tk.Label(self,text="Password",bg="#1f2431",bd=0, fg="white", font="Verdana 14 bold")
        password_text.pack(pady=(40,5))
#                                                                                                                                               var2 - traceable
        password_entry = tk.Entry(self,bd=0, font="Verdana 14", fg="#1f2431", selectbackground="#1f2431", show="•", selectforeground="white", textvariable=var2)
        password_entry.insert(0, "Enter here...")
        password_entry.bind("<FocusIn>", on_entry_click)
        password_entry.bind("<FocusOut>", on_focusout)
        password_entry.bind('<Control-v>', lambda e: 'break')
        password_entry.config(fg = 'grey')
        password_entry.pack()
        
#Login                                                                                                          button calls Authenticate function, passes username and password fields
        login = tk.Button(self, bg="white", fg="#1f2431", text="LOGIN", font="Verdana 14 bold", bd=0, command = lambda:Authenticate(username_entry.get(),password_entry.get()))
        login.pack(pady=(40,10))
        
#Register
        register_extra = tk.Label(self, text="Don't have login details? Register above!", bg="#1f2431", font="Verdana 9", fg="white").pack(pady=(20,0))
        register = tk.Button(self, bg="white", fg="#1f2431", text="REGISTER", font="Verdana 14 bold", bd=0, command = lambda: Register(username_entry.get(),password_entry.get())).pack(pady=(5,0))

#Messages
        msg = "A strong password contains:"                 #Defines possible text on output at the bottom
        msgalt = "Your password contains:"
        msg1 = "8+ characters"
        msg2 = "A combination of case"
        msg3 = "Special character[/s] and [a] numbers[/s]"
        tick = "✔ "
        cross = "✖ "
        rhc = tk.Canvas(self, bg="white")
        rh1 = tk.Label(rhc, text = (msg), bd=0, font="Verdana 9",bg="white", fg="green")
        rh2 = tk.Label(rhc, text = (tick+msg1), bd=0, font="Verdana 9",bg="white", fg="green")
        rh3 = tk.Label(rhc, text = (tick+msg2), bd=0, font="Verdana 9",bg="white", fg="green")
        rh4 = tk.Label(rhc, text = (tick+msg3), bd=0, font="Verdana 9",bg="white", fg="green")
        rhc.pack(pady=(12.5,0),fill="both")
        rh1.place(x=340,y=3)
        rh2.place(x=340,y=23)
        rh3.place(x=340,y=41)
        rh4.place(x=340,y=59)
        
#Authenticate
        def newsave():
            global songnumber, lives, score, played, uname      # Used in next class - need to be globalised
            songnumber = random.randint(1,400)
            uname = username_entry.get()
            played = []                                         # List containing songs already played
            played.append(songnumber)                           # Generated songs are appended to it
            lives = 2
            score = 0
            master.switch_frame(Game)                           # Switch to main game
            
        def Authenticate(username,password):
            if username=="Enter here..." or username=="" or password=="Enter here..." or password=="":                                  # Check for empty fields
                rhc.pack_forget()
                rh_new = tk.Label(self, text = "Missing entries!", font="Verdana 9",bg="white", justify="center", fg="red", height=20)  # Output message below
                self.after(2000, lambda: rh_new.pack_forget())
                rh_new.pack(pady=(12.5,0),fill="both")
                rhc.pack(pady=(12.5,0),fill="both")
            else:
                encrypted_password = hashlib.md5(password.encode('utf-8')).digest()                             # Encrypted password to compare to database
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",                       # Check database for matching entries
                       (username,encrypted_password))
                if cursor.fetchone():                                                                           # IF found
                    master.unbind("<Return>")                                                                   # Disable 'Enter' key
                    cursor.execute("SELECT username FROM saves WHERE username = ?",(username,))                 # Check if saves exist
                    if cursor.fetchone():                                                                       # IF found
                        global uname                                                                            # Username is used to look for saves in next class
                        uname = username
                        master.switch_frame(LoadSaves)
                    else:
                        newsave()                                                                               # ELSE create a new save
                else:
                    rhc.pack_forget()                                                                           # IF no matching entry found
                    rh_new = tk.Label(self, text = "Incorrect username or password.\nTry again or register.",   # Incorrect entries or no such user
                                font="Verdana 9",bg="white", justify="center",
                                fg="red", height=20)
                    self.after(2000, lambda: rh_new.pack_forget())
                    rh_new.pack(pady=(12.5,0),fill="both")
                    rhc.pack(pady=(12.5,0),fill="both")
        
#New Registration
        def Register(username,password):
            if username=="Enter here..." or username=="" or password=="Enter here..." or password=="":                                  # Check for missing entries
                rhc.pack_forget()
                rh_new = tk.Label(self, text = "Missing entries!", font="Verdana 9",bg="white", justify="center", fg="red", height=20)
                self.after(2000, lambda: rh_new.pack_forget())
                rh_new.pack(pady=(12.5,0),fill="both")
                rhc.pack(pady=(12.5,0),fill="both")
            else:
                cursor.execute("SELECT * FROM users WHERE username = ?",(username,))                                                    # Check if username already exists
                if cursor.fetchone():
                    rhc.pack_forget()
                    rh_new = tk.Label(self, text = "You have already registered!\nTry logging in.", font="Verdana 9",bg="white", justify="center", fg="red", height=20)
                    self.after(2000, lambda: rh_new.pack_forget())                                                                      # Tell user that username exists
                    rh_new.pack(pady=(12.5,0),fill="both")
                    rhc.pack(pady=(12.5,0),fill="both")                                                                                 # (BELOW) Check if all requirements are met
                elif len(password)>=8 and (any(l.isupper() for l in password) and any(l.islower() for l in password)) and (any(l in string.punctuation for l in password) and any(l.isdigit() for l in password)):
                    encrypted_password = hashlib.md5(password.encode('utf-8')).digest()                                                 # Encrypt password
                    cursor.execute("INSERT INTO users VALUES (?,?)",(username,encrypted_password))                                      # Submit entries to database
                    details.commit()
                    master.unbind("<Return>")
                    global uname                                                                                                        # For later use
                    uname = username
                    newsave()                                                                                                           # Create new save
                else:
                    rhc.pack_forget()
                    rh_new = tk.Label(self, text = "Password not strong enough.\nTry again", font="Verdana 9",bg="white", justify="center", fg="red", height=20)    # ELSE password
                    self.after(2000, lambda: rh_new.pack_forget())                                                                                                  # requirements not met
                    rh_new.pack(pady=(12.5,0),fill="both")
                    rhc.pack(pady=(12.5,0),fill="both")

#Real-time Validation
        def validate(*args):                                                                    # Real-time validation - called on write
            rh1.configure(text=(msgalt),fg="black")                                             # Set default values - all red
            rh2.configure(text=(cross+msg1),fg="red")
            rh3.configure(text=(cross+msg2),fg="red")
            rh4.configure(text=(cross+msg3),fg="red")

            y = var2.get()
            y = y[:max_len2].strip()

            if len(y)>=8:                                                                       # Set output text dependent on the requirements met
                rh2.configure(text=(tick+msg1),fg="green")
            if (any(l.isupper() for l in y) and (any(l.islower() for l in y))):
                rh3.configure(text=(tick+msg2),fg="green")
            if (any(l in string.punctuation for l in y) and any(l.isdigit() for l in y)):
                rh4.configure(text=(tick+msg3),fg="green")
            if len(y)>=8 and (any(l.isupper() for l in y) and any(l.islower() for l in y)) and (any(l in string.punctuation for l in y) and any(l.isdigit() for l in y)):
                rh1.configure(fg="green")
        var2.trace_variable("w",validate)                                                       # Call on write -> no need for while loop; called on each character entered
        

############################################################################################################################################################################################
#SAVES SCREEN
class LoadSaves(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#1f2431")

#Title - SAVES
        title = tk.Canvas(self,width=300,height=75,bg="#1f2431")
        title.create_text(150,37.5,fill="white",font="Verdana 26 bold",
                          text="SAVES")
        title.pack(pady=25)
        
#Display Saves
        cursor.execute("SELECT listno,songnumber,lives,played,score,time,date FROM saves WHERE username = ?",(uname,))          # Import all saves

#Label (Bold and Standard)
        def boldstandard(bold,standard,row,width):                                                                              # Function returns text in two parts - bold and regular
            tk.Label(box,text=bold,fg="#1f2431",font="Verdana 12 bold", bg="white").pack(side=tk.LEFT,padx=(15,0))              # as tkinter lacks this functionality
            tk.Label(box,text=(standard,),fg="#1f2431",font="Verdana 12",width=width, bg="white").pack(side=tk.LEFT)

#Scrollbar
        scrollable = tk.Canvas(self,bg="white",height=465)                  # Canvas to hold scrollbar
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)                 # Scrollbar type - vertical
        vscrollbar.pack(fill="y", side=tk.RIGHT)                            # Position - right
        vscrollbar.config(command=scrollable.yview)                         # Position (view of canvas) affected by scrollbar
        scrollable.config(yscrollcommand=vscrollbar.set)                    # Command on scroll -> Set position (view of canvas)
        scrollable.pack(fill="both")
        mainframe=tk.Frame(scrollable,bg="white")                           # Frame to hold scrollable canvas
        scrollable.create_window(0, 0, anchor = "nw", window=mainframe)     # Add canvas to main frame
        
#Create Canvases for each row found         
        calc_scroll = 0                                                     # Counter calculates estate needed by all listboxes
        for row in cursor:
            listno, songnumber, lives, played, score, time, date = row      # Data needed for each listbox
            box = tk.Canvas(mainframe,bg="white")
            boldstandard("Score:",score,0,4)                                # Text - bold and regular
            boldstandard("Lives:",lives,1,1)
            boldstandard("Date:",date,2,9)
            boldstandard("Time:",time,3,5)
            tk.Button(box, bg="#1f2431", fg="white", text="SELECT", font="Verdana 12 bold", bd=0, width=7, command = lambda n = listno, row = row: loadsave(n,row)).pack(padx=(15,0))
            tk.Button(box, bg="#1f2431", fg="white", text="DELETE", font="Verdana 12 bold", bd=0,width=7, command = lambda n = listno: delsave(n)).pack(padx=(15,0))
            box.pack(pady=(15,0),padx=70)                                                   # Data needed from each listbox (for selection, delete) is passed on to function
            calc_scroll = calc_scroll+1                                                     # when button is clicked (command = ). Data has to be saved in n as it cannot be passed
                                                                                            # regularly due to the button being created inside for loop
        scrollable.config(scrollregion=(0,0,0,calc_scroll*95+200))          # Set size of canvas accordingly

#Create New Save Option            
        new_save = tk.Label(mainframe, text="Want to start a new game? Click the button below.", bg="white",fg="#1f2431",font="Verdana 9").pack(pady=(17.5,0),padx=240)
        nsb = tk.Button(mainframe, bg="#1f2431", fg="white", text="NEW SAVE", font="Verdana 14 bold", bd=0, command = lambda: newsave()).pack(pady=(10,0))

#Selection / loading functionality
        def loadsave(saveno,row):                                           # Import save
            global listno, songnumber, lives, played, score                 # Data actually needed
            listno, songnumber, lives, played, score, time, date = row      # All data
            playedtemp = played.split(",")                                  # Split played songs list (stored as string - needs converting)
            played = []
            for n in playedtemp:
                n = int(n)                                                  # Convert each item in list to integer
                played.append(n)
            self.after(0, lambda: master.switch_frame(Game))

        def delsave(saveno):
            if messagebox.askyesno("Delete","Are you sure?\nThis score wont end up on the leaderboard"):    # Popup - confirms delete
                cursor.execute("DELETE FROM saves WHERE listno = ?",(saveno,))                              # Delete respective save
                details.commit()
                master.switch_frame(LoadSaves)
        def newsave():
            global songnumber, lives, score, played                                                         # Option to create new save
            songnumber = random.randint(1,400)
            played = []
            played.append(songnumber)
            lives = 2
            score = 0
            master.switch_frame(Game)

############################################################################################################################################################################################
#Game Loop
class Game(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white")

#Extras        
        def hoveron(event):                                 # Colour change on hover
            event.widget["background"] = "lightgrey"
        def hoveroff(event):
            event.widget["background"] = "white"
                                                                                                                            #   FIRST RUN               SECOND RUN
        def split(arr, size):                               # splits list into groups of size (created 2d,3d etc. lists)    |   e.g.    split(arr = ['I', 'K', 'Y', 'W', 'T'] , size = 2)
            arrs = []                                       # new list of split items                                       |
            while len(arr) > size:                          # runs until lists are in groups of size (or remainders)        |
                pice = arr[:size]                           # get first [size] items                                        |   pice = ['I', 'K']       pice = ['Y', 'W']
                arrs.append(pice)                           # add to new list                                               |   arrs = [['I', 'K']]     arrs = [['I', 'K'], ['Y', 'W']]
                arr   = arr[size:]                          # update list w/ first [size] items removed                     |   arr = ['Y', 'W', 'T']   arr = ['T']
            arrs.append(arr)                                # add remainder to new list                                     |                           arrs = [['I', 'K'], ['Y', 'W'], ['T']]
            return arrs

        # Couldn't disable messagebox protocol when user has moved onto next class -> this causes an error when trying to exit (e.g. when on Game Over frame)
        def ask(*args):                                         # *args --> function is allowed to run if nothing is passed such as in the case of another class (e.g. GameOver)
            try: args[0]                                        # Checks if any variable has been passed (this is only possible in this class)
            except: master.destroy()                            # As it is only possible in this class, the only other possibility is the request is from another class, hence frame is destroyed
            else:                                               # ELSE
                if messagebox.askyesno(args[0],args[1]):        # It goes through normal procedure
                    details.commit()
                    details.close()
                    master.destroy()
        
        master.bind("<Return>", lambda event: check())          # Binds 'Enter' key to Submit
        master.protocol("WM_DELETE_WINDOW",lambda: ask("Quit","Are you sure?\nProgress will not be saved..."))  # Confirms exit without save

#Fetch songs
        cursor.execute("SELECT artistname,songname FROM songs WHERE listno=?",(str(songnumber),))   # Fetch song details for required song
        artistname,songname = cursor.fetchone()
        songname = songname.translate(str.maketrans(outtab,intab))                                  # Descramble

#Add to Leaderboard
        def addtoleaderboard():
            global uname,listno

            cursor.execute("SELECT * FROM leaderboard WHERE username = ?",(uname,))                 # Check if username already exists

            try: tempname,tempscore = cursor.fetchone()                                             # Save as temp if it does
            except TypeError: insert = True                                                         # If it doesn't allow 'Insert' into db
            else:
                if tempscore<score: insert=True                                                     # IF newer score is greater, allow 'Insert'
                else: insert=False                                                                  # ELSE do not insert
                                
            if insert==True:
                cursor.execute("REPLACE INTO leaderboard (username,score) VALUES (?,?)",(uname,score))  #Insert

            try: cursor.execute("DELETE FROM saves WHERE listno = ?",(listno,))                     # Delete matching savegame from db if it exists
            except NameError: pass                                                                  # Pass if it doesn't
            details.commit()
            master.unbind("<Return>")
            master.protocol("WM_DELETE_WINDOW",ask)                                                 # Remove parameters -> messagebox wont work

#Check
        def check():                                                                                # Called when user submits; no parameters - fetched from field
            wordsentered = []
            for i in range (calcentries):                                                           # calcentries - number of input fields (one letter words are not counted)
                entry = wordentries[i].get()                                                        # Fetch each entry
                entry = entry.translate(str.maketrans("","",string.punctuation)).lower()            # Remove whitespace, special characters. Make lowercase
                wordsentered.append(entry)                                                          # Append to new (santised) list
            if any(word is "" for word in wordsentered):                                            # Check for empty fields
                missing = tk.Label(base,bg="white",text="Missing Entries",fg="red",font="Verdana 9 bold")   # Inform user
                self.after(500, lambda:missing.destroy())
                missing.pack(pady=5)
            else:                                                                                   # ELSE
                correctwords = []                                                                   # List of words that would match a correct input
                
                for word in words:
                    word = word.translate(str.maketrans("","",string.punctuation)).lower()          # Remove whitespace, special characters. Make lowercase
                    word = word[1:]                                                                 # Remove first letter
                    correctwords.append(word)
                try:
                    for i in range(len(correctwords)):                                              # Removes any empty items in list (from one letter words where first letter would be
                        correctwords.remove("")                                                     # removed leaving an empty item)
                except ValueError:pass
                
                global score,lives                                                                  # Variables have to be globalised again inside function to work (fetches variables)
                if correctwords == wordsentered:
                    if lives == 2:                                                                  # Two lives left = First guess = +3 points
                        score += 3
                    elif lives == 1:                                                                # One live left = Second guess = +1 point
                        score +=1
                        lives = 2                                                                   # Reset lives to 2 for next session
                    NewSession()
                else:
                    lives -= 1                                                                      # Incorrect - 1
                    liveslabel.configure(text=("LIVES:",lives))                                     # Refresh lives counter
                    if lives == 0:                                                                  # Game Over
                        addtoleaderboard()
                        master.switch_frame(GameOver)                                               # IF statement is used as a WHILE loop would repeat without asking the user for
                                                                                                    # their second guess - check is called on button click
#New Session
        def NewSession():
            global songnumber,played
            generated = False                                                                       # Validation loop
            while not generated:
                generated = True
                songnumber = random.randint(1,400)                                                  # Generates previously unplayed random integer
                if len(played) == 400:                                                              # Incase all songs have been played
                    addtoleaderboard()                                                              # Add score to leaderboard (where save will also be deleted)
                    master.switch_frame(Ended)
                elif songnumber in played:
                    generated = False
            played.append(songnumber)
            master.switch_frame(Game)

#Save and Exit
        def saveandexit():
            global listno, songnumber, lives, played, score, uname      
            played = ",".join(str(n) for n in played)                                               # Convert to string to store in db
            dateandtime = datetime.datetime.now()                                                   # Date and time to distinguish saves
            date = dateandtime.strftime("%d/%m/%Y")
            time = dateandtime.strftime("%H:%M")

            try:                                                                                    # Try updating save
                cursor.execute('''REPLACE INTO saves (listno, username,songnumber,lives,played,score,date,time) VALUES (?,?,?,?,?,?,?,?)''',(listno,uname,songnumber,lives,played,score,date,time))
            except NameError:                                                                       # ELSE create new save (listno is created by db)
                cursor.execute('''INSERT INTO saves (username,songnumber,lives,played,score,date,time) VALUES (?,?,?,?,?,?,?)''',(uname,songnumber,lives,played,score,date,time))

            details.commit()
            details.close
            master.destroy()
            raise SystemExit
            
#Entry/info screen
        base = tk.Canvas(self,bg="white", height=450)               # Holds artist label, artist name and entries boxes

        artistname_label = tk.Label(base, bg="white", fg="#1f2431",font="Verdana 24 bold", text="ARTIST:").pack(expand=True)    # Artist Title
        artistname_label2 = tk.Label(base, bg="white", fg="#1f2431",font="Verdana 24", text=artistname).pack(expand=True)       # Artist Name

        words = songname.split(" ")                         # Split into words
        letters = []                                        # List of letters for boxes containing entries
        entrywidths = []                                    # List of integers defining width of each entry in order
        for word in words:
            entrywidthcalc = len(word)                      # Get word length (rough estimate for entry width)
            entrywidths.append(entrywidthcalc)              # Append to list
            letter = word[0]                                # Get first letter
            if letter=="(":                                 # Incase it is a bracket
                letter = letter+word[1]                     # Get bracket+second letter
                endbracket = True                           # Remember to put end bracket
            else:
                word = word.strip(string.punctuation)       # In other cases, remove special characters
                letter = word[0]                            # First letter stays the same
            letters.append(letter)
        letters = split(letters,2)                          # Function splits into 2D list
        wordentries = []                                    # Stores users entry as tkinter object - fetched via StringVar
        calcentries = 0                                     # Number of entries that can be fetched
        possibleruns = len(words)                           # Number of times to run loop
        runs=0

        for row in letters:
            container = tk.Canvas(base,bg="white",highlightthickness=0)     # Create container to hold all entries                              
            for letter in row:
                runs += 1
                box = tk.Canvas(container,bg="white")                       # Canvas to hold each entry
                firstletter = tk.Label(box, bg="white", fg="#1f2431", font="Verdana 18 bold",text=letter)
                firstletter.pack(side=tk.LEFT,padx=10,pady=2)               # Add first letter to canvas

                if letter in (list(string.ascii_uppercase)) or letter in (list(string.ascii_lowercase)):
                    try: (words[runs-1])[1]                                 # Check if second letter exists in word
                    except IndexError:                                      # IF not
                        create_entry=False                                  # Don't create entry field for canvas
                        box.configure(highlightthickness=0)
                        firstletter.pack_forget()
                        firstletter.pack()
                    else:create_entry=True                                  # IF yes -> Create entry field
                elif letter=="&":                                           # Check for & signs - not checked in one letter words -> neeeds to be done separately
                    create_entry=False
                    box.configure(highlightthickness=0)
                    firstletter.pack_forget()
                    firstletter.pack()

                else:
                    create_entry=True                                       # Otherwise, create entry field
                    
                if create_entry == True:
                    var = tk.StringVar()                                    # IF so, create var which can be fetched
                    calcentries += 1                                        # Increment number of entries created that can be fetched
                    tk.Entry(box,font="Verdana 18",fg="#1f2431",textvariable = var,selectbackground="#1f2431", bd=0, width=entrywidths[runs-1],selectforeground="white").pack(side=tk.LEFT,padx=(0,2),pady=2)
                    wordentries.append(var)                                 # Append entry to list of objects to later be fetched
                    
                try: endbracket                                             # Check if endbracket needs to be added
                except UnboundLocalError: pass
                else:
                    if endbracket == True and runs == possibleruns:         # IF endbracket needs to be created and this is the last run
                        tk.Label(box, bg="white", fg="#1f2431", font="Verdana 18 bold",text=")").pack(side=tk.RIGHT,padx=10,pady=2) # Create bracket

                box.pack(expand=True,side="left",padx=20)
            container.pack(expand=True)
                          
        base.pack(fill="both",padx=20,pady=20)
        base.pack_propagate(False)
        
#Score/Lives Counter + Submit/Save and Exit buttons
        below = tk.Canvas(self,bg="#1f2431",height=110,highlightthickness=0)                                    # Canvas holding buttons and counters
        liveslabel = tk.Label(below,bg="#1f2431", fg="white", font="Verdana 18 bold",text=("LIVES:",lives))     # Lives Label
        liveslabel.pack(side="left",padx=20)
        sub = tk.Button(below,bg="white",text="SUBMIT", bd=0, highlightcolor="lightgrey",fg="#1f2431",font="Verdana 18 bold",command=check)             #Submt button, calls check function
        sav = tk.Button(below,bg="white",text="SAVE AND EXIT",bd=0, highlightcolor="lightgrey",fg="#1f2431",font="Verdana 18 bold",command=saveandexit) #Save button, calls saveandexit
        sub.bind("<Enter>", hoveron)                            # Calls hover functionality
        sub.bind("<Leave>", hoveroff)
        sub.pack(fill="both",side="left",expand=True)
        sav.bind("<Enter>", hoveron)
        sav.bind("<Leave>", hoveroff)
        sav.pack(fill="both",side="left",expand=True)
        scorelabel = tk.Label(below,bg="#1f2431",fg="white", font="Verdana 18 bold",text=("SCORE:",score))      # Score Label
        scorelabel.pack(side="right",padx=20)
        below.pack(fill="both")
        below.pack_propagate(False)

############################################################################################################################################################################################
class GameOver(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white")

#Extras
        def hoveron(event):                     # Colour change on hover
            event.widget["bg"] = "#1f2431"
            event.widget["fg"] = "white"
        def hoveroff(event):
            event.widget["bg"] = "white"
            event.widget["fg"] = "#1f2431"

#Title - GAMEOVER
        title = tk.Canvas(self,width=450,height=200,bg="white",highlightbackground="#1f2431")
        title.create_text(225,100,fill="#1f2431",font="Verdana 35 bold",text="GAME OVER")
        title.pack(pady=(100,50))

#PLAY AGAIN - BUTTON
        playagain = tk.Button(self, bg="white", fg="#1f2431", text="PLAY AGAIN",font="Arial 20 bold", relief ="flat",command = lambda: master.switch_frame(PlayGame))
        playagain.bind("<Enter>", hoveron)
        playagain.bind("<Leave>", hoveroff)
        playagain.pack(pady=(0,20))

#VIEW LEADERBOARD - BUTTON
        leaderboardb = tk.Button(self, bg="white", fg="#1f2431", text="VIEW LEADERBOARD",font="Arial 20 bold", relief = "flat",command = lambda: master.switch_frame(Leaderboard))
        leaderboardb.bind("<Enter>", hoveron)
        leaderboardb.bind("<Leave>", hoveroff)
        leaderboardb.pack()

        tk.Label(self,bg="white",text="Score:",font="Verdana 14 bold").place(x=405,y=550)
        tk.Label(self,bg="white",text=score,font="Verdana 14").place(x=495,y=550)
        
############################################################################################################################################################################################
class Leaderboard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white")
        
#Title - LEADERBOARD
        title = tk.Canvas(self,width=450,height=75,bg="white",highlightbackground="#1f2431")
        title.create_text(225,37.5,fill="#1f2431",font="Verdana 26 bold",text="LEADERBOARD")
        title.pack(pady=25)
        
#Canvas
        def scrollboth(*args):                      # Should be scroll all three
            listbox.yview(*args)                    # Combines 3 listboxes to scroll at the same time using scrollbar
            listbox1.yview(*args)
            listbox2.yview(*args)

        def showmore():                             # Shows all scores
            scorelist_fiveremoved = scorelist[5:]   # Gets the rest of the scores
            i = 5                                   # Counter - number of scores in list
            for row in scorelist_fiveremoved:
                i += 1
                username,score = row
                listbox.insert(tk.END, i)           # Insert position
                listbox1.insert(tk.END, username)   # Insert username
                listbox2.insert(tk.END, score)      # Insert score
            scrollbar.pack(side=tk.RIGHT, fill="y") # Packs scrollbar onto frame
            master.bind("Up",scrollboth)
            showb.config(text="SHOW LESS", command = showless)  # Change button text to Show Less

        def showless():
            listbox.delete(5,len(scorelist))    # Delete all except first 5 on all listboxes
            listbox.yview_moveto(0)             # Move to start on all
            
            listbox1.delete(5,len(scorelist))
            listbox1.yview_moveto(0)
            
            listbox2.delete(5,len(scorelist))
            listbox2.yview_moveto(0)
            
            showb.config(text="SHOW MORE", command=showmore)    # Change button text to Show More
            scrollbar.pack_forget()
#
        canvas = tk.Canvas(self,bg="white",height=140,width=425,highlightthickness=0)   # Canvas holds listbox and scrollbar in center
#
        scrollbar = tk.Scrollbar(canvas, command=scrollboth)
#

        listbox = tk.Listbox(canvas,yscrollcommand=scrollbar.set, font="Verdana 14 bold", width=5,activestyle="none",bd=0,highlightthickness=0,selectbackground="white",selectforeground="black")        
        listbox1 = tk.Listbox(canvas,yscrollcommand=scrollbar.set, font="Verdana 14", width=15,activestyle="none",bd=0,highlightthickness=0,selectbackground="white",selectforeground="black")
        listbox2 = tk.Listbox(canvas,yscrollcommand=scrollbar.set, font="Verdana 14", width=5,activestyle="none",bd=0,highlightthickness=0,selectbackground="white",selectforeground="black")

        startb = tk.Button(self, bg="#1f2431", fg="white", font="Verdana 14 bold",text="START",bd=0,command=lambda:master.switch_frame(PlayGame)) # Back to beginning button
#
        cursor.execute('''SELECT * FROM leaderboard ORDER BY score DESC''')     # Fetch scorelist in descending order
        scorelist = cursor.fetchall()                                           # Store
        
        if scorelist:                                                           # If scorelist could be fetched
            listlength = len(scorelist)
            if listlength < 5:                                                  # IF list is shorter than 5 - show length(list) items
                minindex = listlength
            else:                                                               # ELSE show top 5
                minindex = 5
            for i in range(minindex):                                           # Loop through scorelist, insert position, username and score into listboxes
                username,score = scorelist[i]
                listbox.insert(tk.END, i+1)
                listbox1.insert(tk.END, username)
                listbox2.insert(tk.END, score)
#
            heading1 = tk.Label(self, text="USERNAME", font="Verdana 14 bold",bg="white").place(x=327,y=155)    #Username, Score headings
            heading2 = tk.Label(self, text="SCORE", font="Verdana 14 bold",bg="white").place(x=553,y=155)

            listbox.pack(side="left", fill="both")
            listbox1.pack(side="left", fill="both")
            listbox2.pack(side="left", fill="both")
#
            canvas.pack(pady=65,padx=(30,0))
            canvas.pack_propagate(False)
#
            if listlength > 5:                                                                  # Create Show More button if there are more than 5 items in list
                showb = tk.Button(self, bg="#1f2431", fg="white", font="Verdana 14 bold",
                                  text="SHOW MORE",bd=0,command=showmore)
                showb.pack()
            else:
                pass
        else:
            tk.Label(canvas, text="No Scores Found!",fg="red", bg="white",      # ELSE (if scorelist doesn't exist) - No scores found
                     font="Verdana 20 bold").pack()
            canvas.pack(pady=65)
            canvas.pack_propagate(False)

        startb.pack(pady=20)
        canvas = tk.Canvas(self,bg="white",highlightthickness=0).pack()
############################################################################################################################################################################################
class Ended(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white")
        
        master.destroy()                                                    # Destroy GUI window

        print("Wow, you've played all the songs. Well Done!")               # Print message using CLI
        print('''You may be able to play an updated version by deleting the
current songs.csv file''')

        raise SystemExit                                                    # End game
############################################################################################################################################################################################
#App Loop#
if __name__ == "__main__":
    app = MusicQuiz()
    app.mainloop()
    details.close

############################################################################################################################################################################################
#https://stackoverflow.com/a/49325719
#boilerplate for frame switching functionionality

#https://chart2000.com/about.htm
#chart2000-song-2010-decade-0-3-0046.csv
#chart2000-song-2000-decade-0-3-0046.csv
#songs list
