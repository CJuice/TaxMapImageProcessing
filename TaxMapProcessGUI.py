# The root origin of the script can be found at http://www.tkdocs.com/tutorial/firstexample.html
print("Process running. Importing modules. Generating GUI.")
from tkinter import *
from tkinter import ttk
import logging
from UtilityClass import UtilityClassFunctionality
import TaxMapVariables as myvars


logging.basicConfig(filename=myvars.strLogFileName,level=logging.INFO)
UtilityClassFunctionality.printAndLog("{}: GUI Initiated".format(UtilityClassFunctionality.getDateTimeForLoggingAndPrinting()), UtilityClassFunctionality.INFO_LEVEL)

def runprocessStep1(*args):
    import TaxMapPRE_Processing
    try:
        TaxMapPRE_Processing.main(consolidatedimagepathStep1.get(), newreportfilefolderpathStep1.get())
    except Exception as e:
        print(e)
        pass
def runprocessStep2(*args):
    import TaxMapProcessing
    try:
        TaxMapProcessing.main(consolidatedimagepathStep2.get(), geodatabaseworkspaceStep2.get())
    except Exception as e:
        print(e)
        pass

root = Tk()
root.geometry("700x350")
root.title("TAX MAP PROCESS")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# NOTICE TEXT

ttk.Label(mainframe, text="*Clicking 'Run' moves control to py window*").grid(column=1, row=0, sticky=(E))

# STEP 1 TITLE
ttk.Label(mainframe, text="PRE-PROCESSING (step 1)").grid(column=2, row=1, sticky=(W, E))

# STEP 1 FORM
ttk.Label(mainframe, text="Consolidated Image Files Directory Path").grid(column=1, row=2, sticky=E)
consolidatedimagepathStep1 = StringVar()
consolidatedimagepathentryStep1 = ttk.Entry(mainframe, width=65, textvariable=consolidatedimagepathStep1)
consolidatedimagepathentryStep1.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text="New Report File Folder Directory Path").grid(column=1, row=3, sticky=E)
newreportfilefolderpathStep1 = StringVar()
newreportfilefolderpathentryStep1 = ttk.Entry(mainframe, width=65, textvariable=newreportfilefolderpathStep1)
newreportfilefolderpathentryStep1.grid(column=2, row=3, sticky=(W, E))

# STEP 1 BUTTON
ttk.Button(mainframe, text="Run Step 1", command=runprocessStep1).grid(column=2, row=4, sticky=E)

# STEP 2 INSTRUCTION
ttk.Label(mainframe, text="____________________________________________________________________").grid(column=2, row=5, sticky=(W, E))
ttk.Label(mainframe, text="Use below only if just step 2 needed. Assumes step 1 previously run.").grid(column=2, row=5, sticky=(W))
# ttk.Label(mainframe, text="").grid(column=2, row=4, sticky=(W, E))

# STEP 2 TITLE
ttk.Label(mainframe, text="PROCESSING (step 2)").grid(column=2, row=6, sticky=(W, E))

# STEP 2 FORM
ttk.Label(mainframe, text="Consolidated Image Files Directory Path").grid(column=1, row=7, sticky=E)
consolidatedimagepathStep2 = StringVar()
consolidatedimagepathentryStep2 = ttk.Entry(mainframe, width=65, textvariable=consolidatedimagepathStep2)
consolidatedimagepathentryStep2.grid(column=2, row=7, sticky=(W, E))

ttk.Label(mainframe, text="Destination ESRI Workspace (geodatabase) Path").grid(column=1, row=8, sticky=E)
geodatabaseworkspaceStep2 = StringVar()
consolidatedimagepathentryStep2 = ttk.Entry(mainframe, width=65, textvariable=geodatabaseworkspaceStep2)
consolidatedimagepathentryStep2.grid(column=2, row=8, sticky=(W, E))

# STEP 2 BUTTON
ttk.Button(mainframe, text="Run Step 2 ONLY", command=runprocessStep2).grid(column=2, row=9, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

consolidatedimagepathentryStep1.focus()

root.mainloop()