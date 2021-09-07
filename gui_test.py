from PaDataAnalyze import PA_Data_Analyze
import tkinter as tk

PA = PA_Data_Analyze()


window = tk.Tk()
window.title('PA Data Analyze')
window.geometry('960x960')

label_FileName = tk.Label(window, text=PA.DataFileName)
label_FileName.pack()

window.mainloop()