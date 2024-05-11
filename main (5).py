import tkinter as tk
from grading_system import GradingSystem

def main():
    root = tk.Tk() # This create the app window
    root.resizable(False, False) # Making sure that the app is not resizable
    root.title("Grading App") # The app title
    app = GradingSystem(root)
    root.geometry("400x300") # The app window measurements
    root.mainloop()

if __name__ == "__main__": #
    main()
