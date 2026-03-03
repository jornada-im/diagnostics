
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os

# Hide the root tkinter window
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', True)  # Dialog appears on top

# Ask the user for the root path - usually in the Field Crew/IM Sharepoint root
directory = Path(filedialog.askdirectory(title="Select the reporting directory",
                                          initialdir="~"))
print(f"Selected: {directory}")


#Set the path to EDI changes
changes_path = os.path.join(directory, 'edi', 'changes_rq')
#Set the path to EDI audits
audit_path = os.path.join(directory, 'edi', 'audit_rq')
# Set path for output tables
output_table_path = os.path.join(directory, 'report_tables')
# Set path for output figures
output_figure_path = os.path.join(directory, 'report_figures')
