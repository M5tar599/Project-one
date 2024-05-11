import tkinter as tk
from tkinter import messagebox
import csv # Importing csv library in order to use CSV file
from calculator import GradeCalculator # Importing the class GradeCalculator from the file calculator.py

class CSVManager:
    def __init__(self, filename='grades.csv'):
        self.filename = filename # filename attribute

    def append_grade(self, data): # appending grade entry
        with open(self.filename, 'a', newline='') as file: # Organizing the CSV file
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final", "Grade"])
            writer.writerow(data) # Writing the data to CSV file

    def save_all(self, students):
        with open(self.filename, 'w', newline='') as file: # Opening the file to write
            writer = csv.writer(file) # Creating CSV writer
            writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final", "Grade"]) # Header
            for name, details in students.items(): # Looping each student in the dictionary and writing their data
                writer.writerow([name] + details['scores'] + [details['final_score'], details['grade']]) # appending the details of the students to the CSV file


class StudentManager:
    def __init__(self, calculator, csv_manager):
        self.calculator = calculator # Grade calculation
        self.csv_manager = csv_manager # CSV Manager that handles the CSV operations
        self.students = {} # Students dictionary

    def submit_scores(self, name, scores):
        final_score = max(scores) if scores else 0 # Calculating final score depending on the best score
        grade = self.calculator.calculate_grade(final_score)
        self.students[name] = {'scores': scores + [0] * (4 - len(scores)), 'final_score': final_score, 'grade': grade}   # Updating the dictionary with new information
        self.csv_manager.append_grade([name] + self.students[name]['scores'] + [final_score, grade])   # Appending the data to the CSV file

    def save_students(self): # Saving the data to the CSV file
        self.csv_manager.save_all(self.students)

class GUIManager:
    def __init__(self, root, student_manager):
        self.root = root # root window
        self.student_manager = student_manager # managing students data
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Enter student's name:").grid(row=0, column=0) # Asking for student name
        self.name_entry = tk.Entry(self.root) # Setting the entry boxes
        self.name_entry.grid(row=0, column=1) # Adjusting the measurements

        tk.Label(self.root, text="Enter number of attempts (1-4):").grid(row=1, column=0) # Asking for the number of attempts
        self.attempts_entry = tk.Entry(self.root) # Creating attempts entry box or grid
        self.attempts_entry.grid(row=1, column=1) # Adjusting the measurements
        vcmd = (self.root.register(self.on_attempts_change), '%P')
        self.attempts_entry.configure(validate='key', validatecommand=vcmd)

        add_button = tk.Button(self.root, text="Add", command=self.add_student) # Creating an add button
        add_button.grid(row=3, column=0, columnspan=2) # Adjusting the measurements of the add button

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_entries) # Creating a clear button
        clear_button.grid(row=4, column=0) # Adjusting the measurements of the clear button

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy) # Creating an exit button
        exit_button.grid(row=4, column=1) # Adjusting the measurements of the exit button

        self.score_frame = tk.Frame(self.root) # The Grids or boxes of the number of attempts
        self.score_frame.grid(row=2, column=0, columnspan=2)
        self.score_entries = []

    def on_attempts_change(self, value): # Attempts entry validation
        if value.isdigit() and 1 <= int(value) <= 4: # Making sure the user have a maximum of 4 attempts
            self.create_score_entries(int(value)) #
            return True
        elif value == "":
            self.clear_score_entries()
            return True
        return False

    def create_score_entries(self, num_attempts): # Creating the score entries depending on the number of attempts
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        self.score_entries = []
        for i in range(num_attempts):
            tk.Label(self.score_frame, text=f'Score {i + 1}:').grid(row=i, column=0)
            entry = tk.Entry(self.score_frame)
            entry.grid(row=i, column=1)
            self.score_entries.append(entry)

    def clear_score_entries(self): # This will clear everything that is on the score entries
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        self.score_entries = []

    def add_student(self): # Adding the student with the scores
        name = self.name_entry.get().strip()
        attempts = self.attempts_entry.get()
        if not name or name.isdigit() or not attempts.isdigit() or not 1 <= int(attempts) <= 4:
            messagebox.showerror("Error", "Invalid input. Please check the name and number of attempts.")
            return

        scores = [int(entry.get()) for entry in self.score_entries if entry.get().isdigit() and 0 <= int(entry.get()) <= 100]
        if len(scores) != int(attempts):
            messagebox.showerror("Error", "Please enter valid scores for all attempts.")
            return

        self.student_manager.submit_scores(name, scores)
        self.clear_entries()

    def clear_entries(self): # This will clear everything on the entry boxes
        self.name_entry.delete(0, tk.END)
        self.attempts_entry.delete(0, tk.END)
        self.clear_score_entries()

class GradingSystem:
    def __init__(self, root):
        self.root = root
        self.calculator = GradeCalculator()
        self.csv_manager = CSVManager()
        self.student_manager = StudentManager(self.calculator, self.csv_manager)
        self.gui_manager = GUIManager(root, self.student_manager)
