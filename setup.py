import os, csv, sqlite3

details = sqlite3.connect(':memory:')       # Creates db in RAM
details = sqlite3.connect('details.db')     # Creates/opens file named details.db
cursor = details.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS saves(listno INTEGER primary key, username TEXT,songnumber INTEGER, lives INTEGER, played TEXT, score INTEGER, time TEXT,date TEXT)
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs(listno INTEGER, artistname TEXT, songname TEXT)
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard(username TEXT UNIQUE, score INTEGER)
''')                                        # Creates required tables


from urllib.request import urlretrieve      # Looks for files, downloads them
def filecheck(filename,url):
    try: file = open(filename,'r')
    except FileNotFoundError:
        print("Downloading...")
        try: urlretrieve(url,filename)
        except Exception:
            print("\nPlease allow outbound connections to raw.githubusercontent.com")
            raise SystemExit
        else: print("Done\n")
        
filecheck('music.ico','https://raw.githubusercontent.com/MZakariyya9/MusicQuiz/master/music.ico')
filecheck('songs.csv','https://raw.githubusercontent.com/MZakariyya9/MusicQuiz/master/songs.csv')

try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)      # Removes blur
except:                                                 # Older versions of Python do not have 'SetProcessDpiAwareness'
    print('''Error: Outdated version of ctypes
For intended experience, please update Python/ctypes and restart the program\n''')

    qctypes = ''                                        # Asks user if they'd like to download t
    while qctypes not in ('Y','N'):
        qctypes = input("Would you like to download ctypes? Y/N: ").upper()

    if qctypes == 'Y':
        filecheck('ctypes.zip','https://raw.githubusercontent.com/MZakariyya9/MusicQuiz/master/ctypes.zip')
        import zipfile
        with zipfile.ZipFile('ctypes.zip','r') as ctypeszip:
            try:ctypeszip.extractall()                  # Downloaded file is extracted
            except PermissionError:                     # In case permissions do not allow extraction
                print("Permision Error: couldn't extract files")
                ctypeszip.close()
                import shutil
                shutil.rmtree((os.path.dirname(os.path.abspath(__file__)))+'\\ctypes')  # Extracted folder is deleted
            else:
                ctypeszip.close()
                os.remove('ctypes.zip')                 # IF successfully extracted, zip file is deleted
        print("\n[Extract and] copy the ctypes folder in 'Dependencies' to the 'Libs' folder in\nyour Python directory")
    else: print("OK")
#

file = open('songs.csv','r')
songlist = csv.reader(file)                             # Reads songs file
cursor.execute("DELETE FROM songs")                     # Deletes old data incase it is corrupted

intab = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"      # Decryption key of sorts
outtab = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

try:
    for row in songlist:                                            # Loops over songs, inserts into db
        cursor.execute("INSERT INTO songs VALUES (?,?,?)",row)
except:
    print("File may be corrupted. Please delete songs.csv in 'Dependencies'") # In case songs.csv file itself is corrupted
    raise SystemExit
    
file.close()
details.commit()
