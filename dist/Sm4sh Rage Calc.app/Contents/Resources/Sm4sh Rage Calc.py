# All code by DuckDuckPony (Bryan Becker) 2016. Formulas taken from www.ssbwiki.com. 

from Tkinter import *
import math
from charDict import weights

master = Tk()
master.configure(bg="#242424")
master.title("Smash 4 Rage Calculator")

#create labels
notesLabel = Label(master, text="Welcome to the Smash 4 Rage Calculator! This is a tiny utility that lets you know what percentage is being simulated on your opponent when you hit them while under the effects of rage. For example, if you hit Mario with Pac-Man's F-air while he has 130% damage, and you have 110%, the knockback he receives is the nearly the same as if you hit him at 147% while you had no rage at all. \nSince testing effects of rage requires you to be outside of training mode and is therefore super time consuming, this could be helpful for determining whether or not kill confirms or combos are still true at certain percents/amounts of rage. \nAll move data can be found on http://kuroganehammer.com/Smash4.", bg="#242424", fg="#fdb3b3", highlightbackground="#2d2d2d", wraplength=950, justify=CENTER).grid(row=0, columnspan=4, sticky=W, pady=10, padx=15)

charLabel = Label(master, text="Opponent's Character:", bg="#242424", fg="#a6d0f0", highlightbackground="#2d2d2d").grid(row=1, sticky=W, pady=5, padx=15)
damageLabel = Label(master, text="Opponent's Percentage:", bg="#242424", fg="#a6d0f0", highlightbackground="#2d2d2d").grid(row=2, sticky=W, pady=5, padx=15)
selfdamageLabel = Label(master, text="Your Percentage:", bg="#242424", fg="#a6d0f0", highlightbackground="#2d2d2d").grid(row=3, sticky=W, pady=5, padx=15)
attackDamageLabel = Label(master, text="Attack's Damage:", bg="#242424", fg="#a6d0f0", highlightbackground="#2d2d2d").grid(row=4, sticky=W, pady=5, padx=15)
attackDescLabel = Label(master, text="On KuroganeHammer.com, this is Base Dmg. value.", bg="#242424", fg="#ffe699", highlightbackground="#2d2d2d").grid(row=4, column=3, sticky=W, pady=5, padx=15)
kbGrowthLabel = Label(master, text="Knockback Growth:", bg="#242424", fg="#a6d0f0", highlightbackground="#2d2d2d").grid(row=5, sticky=W, pady=5, padx=15)
kbGrowthDescLabel = Label(master, text="On KuroganeHammer.com, this is KBG value, divided by 100 (ex. KBG of 90, put 0.9).", bg="#242424", fg="#ffe699", highlightbackground="#2d2d2d").grid(row=5, column=3, sticky=W, pady=5, padx=15)
kbBaseLabel = Label(master, text="Base Knockback:", bg="#242424", fg="#a6d0f0", highlightbackground="#2d2d2d").grid(row=6, sticky=W, pady=5, padx=15)
kbBaseDescLabel = Label(master, text="On KuroganeHammer.com, this is BKB/WBKB value.", bg="#242424", fg="#ffe699", highlightbackground="#2d2d2d").grid(row=6, column=3, sticky=W, pady=5, padx=15)
resultLabel = Label(master, text="", bg="#363636", fg="#a6d0f0", highlightbackground="#2d2d2d")
resultLabel.grid(row=8, sticky=W, padx=15, columnspan=2, pady=5)
copyLabel = Label(master, text="All code by DuckDuckPony, using Python/Tkinter. Formulas for knockback/rage found on www.ssbwiki.com. Follow me on Twitter @DuckDuckBryan. Thanks for checking this out!", bg="#242424", fg="#9fffcc", highlightbackground="#2d2d2d", wraplength=950, justify=CENTER, font=("TkDefaultFont", 10)).grid(row=9, columnspan=4, sticky=W, pady=10, padx=15)

#create entries
oDamEnt = Entry(master, highlightbackground="#363636")
sDamEnt = Entry(master, highlightbackground="#363636")
aDamEnt = Entry(master, highlightbackground="#363636")
kbGrowthEnt = Entry(master, highlightbackground="#363636")
kbBaseEnt = Entry(master, highlightbackground="#363636")

oDamEnt.grid(row = 2, column = 1, sticky=W)
sDamEnt.grid(row = 3, column = 1, sticky=W)
aDamEnt.grid(row = 4, column = 1, sticky=W)
kbGrowthEnt.grid(row = 5, column = 1, sticky=W)
kbBaseEnt.grid(row = 6, column = 1, sticky=W)

# adjust window size
master.minsize(width=1000,height=450)

# grid settings
master.grid_columnconfigure(0, weight=1)
master.grid_columnconfigure(1, weight=1)
master.grid_columnconfigure(2, weight=1)

# create popup menu for character choices
var = StringVar(master)
var.set("(Select Character)") # initial value

option = OptionMenu(master, var, "Bayonetta", "Bowser", "Bowser Jr.", "Captain Falcon", "Charizard", "Cloud", "Corrin", "Dank Pit", "Diddy Kong", "Dankey Kang", "Dr. Mario", "Duck Hunt", "Falco", "Fox", "Game & Watch", "Ganondorf", "Greninja", "Ike", "Jigglypuff", "King DeDeDe", "Kirby", "Link", "Little Mac", "Lucario", "Lucas", "Lucina", "Luigi", "Mario", "Marth", "Megaman", "Metaknight", "Mewtwo", "Mii Fighters", "Ness", "Olimar", "PAC-Man", "Palutena", "Peach", "Pikachu", "Pit", "R.O.B.", "Robin", "Rosalina & Luma", "Roy", "Ryu", "Samus", "Sheik", "Shulk", "Sanic", "Toon Link", "Villager", "Wario", "Wii Fit Trainer", "Yoshi", "Zorlda", "Zero Suit Samus")
option.configure(bg="#242424", highlightbackground="#2d2d2d")
option.grid(row = 1, column = 1, sticky=W)

# functions
  
# this function takes the selection from the popup menu and matches it to a character name / weight from the charDict file

def getCharacter():
    character = var.get()
    charWeight = character.lower()
    for w in weights:
    	if w == charWeight:
    		charWeight = weights[w]
    		break  
    return charWeight
  
# function formulae for calculating knockback. 
# if between 35 and 150, apply rage multiplier.
# if over 150, just apply max rage (1.15)
# if under, 35, don't apply rage at all

def knockbackCalc(p, w, r, d, s, b):
	if r > 35 and r <= 150:
		r = 1 + ((r-35) * .15) / 115
		kb = ((((p / 10.0 + ((p * d) / 20.0)) * ((200.0 / (w + 100.0)) * 1.4) + 18.0) * s) + b) * r
	elif r > 150:
		r = 1.15
		kb = ((((p / 10.0 + ((p * d) / 20.0)) * ((200.0 / (w + 100.0)) * 1.4) + 18.0) * s) + b) * r
	else:
		kb = ((((p / 10.0 + ((p * d) / 20.0)) * ((200.0 / (w + 100.0)) * 1.4) + 18.0) * s) + b)
	
	return kb
    
# the following function is used to calculate the knockback of a move with no rage multiplier
# this is used later to compare the rage-affected move to its non-rage equivalent

def noRageCalc(p, w, d, s, b):
    	kb = ((((p / 10.0 + ((p * d) / 20.0)) * ((200.0 / (w + 100.0)) * 1.4) + 18.0) * s) + b)
    	return kb
        
# this function handles all of the I/O, as well as performing calculations and comparisons of knockback/percents

def printKnockback():
    
    # get attributes from entries, error handling
    try:
        d = float(aDamEnt.get())
        s = float(kbGrowthEnt.get())
        b = float(kbBaseEnt.get())
        percent = int(oDamEnt.get())
        rage = int(sDamEnt.get())
    except ValueError:
        resultLabel.configure(text="Please enter some valid numbers. Work with me here.")
        return 0
    try:
        w = float(getCharacter())
    except ValueError:
        resultLabel.configure(text="Please select a valid character.")
        return 0
    
    # calculate knockback
    calculatedKnock = knockbackCalc(percent, w, rage, d, s, b)
        #print calculatedKnock
    
    # put each knockback value into a list
    kbList = []
    for p in range(0,1000):
        kbList.append(noRageCalc(p, w, d, s, b))
    
    # compare the rage-calculated knockback to the list of non-rage knockbacks to determine which kb percent this one is closest to
    affectedKnockback = min(kbList, key=lambda x:abs(x-calculatedKnock))
    affectedPercent = (kbList.index(affectedKnockback)) - 1 # match calculated knockback with index of non-rage knockback (index-1 will be the percent of that knockback)
    
    if rage > 35:
        if affectedPercent == (percent - 1) or affectedPercent == percent:
            print("Rage's affect on knockback is negligible at these percents.")
            resultLabel.configure(text="Rage's affect on knockback is negligible at these percents.")
        elif affectedPercent > 996:
            resultLabel.configure(text="This is equivalent to hitting your opponent at maximum percentage.")
        else:
            print("This is equivalent to hitting your opponent at " + str(affectedPercent) + "%.")
            resultLabel.configure(text="This is equivalent to hitting your opponent at " + str(affectedPercent) + "%.")
    else:
        print("This move is unaffected by rage at these percents.")
        resultLabel.configure(text="This move is unaffected by rage at these percents.")
    
    d = 0
    s = 0
    b = 0
    percent = 0
    rage = 0
    
    return 0

#dis a button

button = Button(master, text="Calculate Equivalent Percent", command=printKnockback, highlightbackground="#242424")
button.grid(row = 7, columnspan = 2, pady=5)

mainloop()

# discontinued functions

	
# def kbVariation(w):
  #  	n = noRageCalc(50, w, d, s, b)
  #  	l = noRageCalc(51, w, d, s, b)
  #  	diff = math.fabs(n-l)
  #  	return diff
  
  # difference = kbVariation(98) (this went into printKnockback)
