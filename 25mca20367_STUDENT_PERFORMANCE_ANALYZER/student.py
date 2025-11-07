"""
Advanced Student Performance Analyzer
With GUI, Database Integration, and Data Visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
from datetime import datetime
import pandas as pd

# Set seaborn style
sns.set_style("whitegrid")

class DatabaseManager:
    """Handle all database operations"""
    
    def __init__(self, db_name="student_performance.db"):
        self.db_name = db_name
        self.create_tables()
    
    def create_tables(self):
        """Create necessary database tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                roll_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                class TEXT,
                created_date TEXT
            )
        ''')
        
        # Marks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT,
                subject TEXT,
                marks REAL,
                max_marks REAL DEFAULT 100,
                exam_date TEXT,
                FOREIGN KEY (roll_no) REFERENCES students(roll_no)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_student(self, roll_no, name, age, class_name):
        """Add a new student to database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (roll_no, name, age, class, created_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (roll_no, name, age, class_name, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def add_marks(self, roll_no, subject, marks, exam_date=None):
        """Add marks for a student"""
        if exam_date is None:
            exam_date = datetime.now().strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO marks (roll_no, subject, marks, exam_date)
            VALUES (?, ?, ?, ?)
        ''', (roll_no, subject, marks, exam_date))
        conn.commit()
        conn.close()
        return True
    
    def get_all_students(self):
        """Retrieve all students"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY roll_no')
        students = cursor.fetchall()
        conn.close()
        return students
    
    def get_student_marks(self, roll_no):
        """Get all marks for a specific student"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT subject, marks, exam_date 
            FROM marks 
            WHERE roll_no = ?
            ORDER BY subject
        ''', (roll_no,))
        marks = cursor.fetchall()
        conn.close()
        return marks
    
    def get_all_marks(self):
        """Get all marks data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.roll_no, s.name, m.subject, m.marks
            FROM students s
            JOIN marks m ON s.roll_no = m.roll_no
            ORDER BY s.roll_no, m.subject
        ''')
        data = cursor.fetchall()
        conn.close()
        return data
    
    def delete_student(self, roll_no):
        """Delete a student and their marks"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM marks WHERE roll_no = ?', (roll_no,))
        cursor.execute('DELETE FROM students WHERE roll_no = ?', (roll_no,))
        conn.commit()
        conn.close()
        return True


class StudentPerformanceAnalyzer:
    """Main GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analyzer")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Create main UI
        self.create_ui()
    
    def create_ui(self):
        """Create the main user interface"""
        
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎓 Student Performance Analyzer", 
            font=("Arial", 20, "bold"),
            bg="#2c3e50", 
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_student_tab()
        self.create_marks_tab()
        self.create_view_tab()
        self.create_analysis_tab()
        self.create_visualization_tab()
    
    def create_student_tab(self):
        """Tab for adding students"""
        student_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(student_frame, text="📝 Add Student")
        
        # Form frame
        form_frame = tk.LabelFrame(
            student_frame, 
            text="Student Information", 
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=20
        )
        form_frame.pack(pady=30, padx=30, fill=tk.BOTH)
        
        # Roll Number
        tk.Label(form_frame, text="Roll Number:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.roll_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.roll_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Name
        tk.Label(form_frame, text="Name:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Age
        tk.Label(form_frame, text="Age:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.age_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.age_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Class
        tk.Label(form_frame, text="Class:", font=("Arial", 10), bg="white").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.class_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.class_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        add_btn = tk.Button(
            button_frame,
            text="Add Student",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10, 
            command=self.add_student
        )
        add_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10,
            command=self.clear_student_form
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
    
    def create_marks_tab(self):
        """Tab for adding marks"""
        marks_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(marks_frame, text="📊 Add Marks")
        
        # Form frame
        form_frame = tk.LabelFrame(
            marks_frame, 
            text="Student Marks", 
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=20
        )
        form_frame.pack(pady=30, padx=30, fill=tk.BOTH)
        
        # Roll Number
        tk.Label(form_frame, text="Roll Number:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.marks_roll_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.marks_roll_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Subject
        tk.Label(form_frame, text="Subject:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.subject_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.subject_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Marks
        tk.Label(form_frame, text="Marks (0-100):", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.marks_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.marks_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        add_marks_btn = tk.Button(
            button_frame,
            text="Add Marks",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            command=self.add_marks
        )
        add_marks_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10,
            command=self.clear_marks_form
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
    
    def create_view_tab(self):
        """Tab for viewing student data"""
        view_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(view_frame, text="👥 View Students")
        
        # Control frame
        control_frame = tk.Frame(view_frame, bg="white")
        control_frame.pack(pady=10, fill=tk.X)
        
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh",
            font=("Arial", 10),
            bg="#16a085",
            fg="white",
            padx=15,
            pady=5,
            command=self.refresh_student_list
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        delete_btn = tk.Button(
            control_frame,
            text="🗑️ Delete Selected",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            command=self.delete_selected_student
        )
        delete_btn.pack(side=tk.LEFT, padx=10)
        
        # Treeview for students
        tree_frame = tk.Frame(view_frame, bg="white")
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        y_scroll = tk.Scrollbar(tree_frame)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scroll = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create treeview
        self.student_tree = ttk.Treeview(
            tree_frame,
            columns=("Roll No", "Name", "Age", "Class", "Date"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        
        # Configure scrollbars
        y_scroll.config(command=self.student_tree.yview)
        x_scroll.config(command=self.student_tree.xview)
        
        # Define headings
        self.student_tree.heading("Roll No", text="Roll No")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Age", text="Age")
        self.student_tree.heading("Class", text="Class")
        self.student_tree.heading("Date", text="Created Date")
        
        # Define column widths
        self.student_tree.column("Roll No", width=100)
        self.student_tree.column("Name", width=200)
        self.student_tree.column("Age", width=80)
        self.student_tree.column("Class", width=100)
        self.student_tree.column("Date", width=150)
        
        self.student_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load initial data
        self.refresh_student_list()
    
    def create_analysis_tab(self):
        """Tab for statistical analysis"""
        analysis_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(analysis_frame, text="📈 Analysis")
        
        # Control buttons
        control_frame = tk.Frame(analysis_frame, bg="white")
        control_frame.pack(pady=10, fill=tk.X)
        
        analyze_btn = tk.Button(
            control_frame,
            text="📊 Generate Analysis",
            font=("Arial", 11, "bold"),
            bg="#8e44ad",
            fg="white",
            padx=20,
            pady=10,
            command=self.generate_analysis
        )
        analyze_btn.pack(pady=10)
        
        # Text area for analysis results
        self.analysis_text = scrolledtext.ScrolledText(
            analysis_frame,
            font=("Courier", 10),
            wrap=tk.WORD,
            height=25
        )
        self.analysis_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    
    def create_visualization_tab(self):
        """Tab for data visualization"""
        viz_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(viz_frame, text="📉 Visualizations")
        
        # Control frame
        control_frame = tk.Frame(viz_frame, bg="white")
        control_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(control_frame, text="Select Chart Type:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
        
        chart_types = [
            "Student Performance Bar Chart",
            "Subject-wise Average",
            "Grade Distribution",
            "Performance Heatmap",
            "Box Plot by Subject"
        ]
        
        self.chart_var = tk.StringVar(value=chart_types[0])
        chart_combo = ttk.Combobox(
            control_frame,
            textvariable=self.chart_var,
            values=chart_types,
            state="readonly",
            width=30,
            font=("Arial", 10)
        )
        chart_combo.pack(side=tk.LEFT, padx=10)
        
        generate_btn = tk.Button(
            control_frame,
            text="Generate Chart",
            font=("Arial", 10, "bold"),
            bg="#e67e22",
            fg="white",
            padx=15,
            pady=5,
            command=self.generate_visualization
        )
        generate_btn.pack(side=tk.LEFT, padx=10)
        
        # Canvas for matplotlib
        self.viz_canvas_frame = tk.Frame(viz_frame, bg="white")
        self.viz_canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    # Callback functions
    
    def add_student(self):
        """Add student to database"""
        roll_no = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        class_name = self.class_entry.get().strip()
        
        if not all([roll_no, name, age, class_name]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return
        
        if self.db.add_student(roll_no, name, age, class_name):
            messagebox.showsuccess("Success", f"Student {name} added successfully!")
            self.clear_student_form()
            self.refresh_student_list()
        else:
            messagebox.showerror("Error", f"Student with roll number {roll_no} already exists!")
    
    def add_marks(self):
        """Add marks to database"""
        roll_no = self.marks_roll_entry.get().strip()
        subject = self.subject_entry.get().strip()
        marks = self.marks_entry.get().strip()
        
        if not all([roll_no, subject, marks]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            marks = float(marks)
            if marks < 0 or marks > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Marks must be a number between 0 and 100!")
            return
        
        if self.db.add_marks(roll_no, subject, marks):
            messagebox.showinfo("Success", f"Marks added for {subject}!")
            self.clear_marks_form()
        else:
            messagebox.showerror("Error", "Failed to add marks!")
    
    def clear_student_form(self):
        """Clear student form fields"""
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
    
    def clear_marks_form(self):
        """Clear marks form fields"""
        self.marks_roll_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)
    
    def refresh_student_list(self):
        """Refresh the student list in treeview"""
        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        # Load students from database
        students = self.db.get_all_students()
        for student in students:
            self.student_tree.insert("", tk.END, values=student)
    
    def delete_selected_student(self):
        """Delete selected student from database"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
        
        item = self.student_tree.item(selected[0])
        roll_no = item['values'][0]
        name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            self.db.delete_student(roll_no)
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.refresh_student_list()
    
    def generate_analysis(self):
        """Generate statistical analysis"""
        self.analysis_text.delete(1.0, tk.END)
        
        # Get all data
        all_marks = self.db.get_all_marks()
        
        if not all_marks:
            self.analysis_text.insert(tk.END, "No data available for analysis!")
            return
        
        # Convert to numpy arrays for analysis
        data = {}
        for roll_no, name, subject, marks in all_marks:
            if roll_no not in data:
                data[roll_no] = {'name': name, 'marks': [], 'subjects': []}
            data[roll_no]['marks'].append(marks)
            data[roll_no]['subjects'].append(subject)
        
        # Calculate statistics
        output = "=" * 70 + "\n"
        output += " " * 20 + "STATISTICAL ANALYSIS\n"
        output += "=" * 70 + "\n\n"
        
        # Overall statistics
        all_marks_array = np.array([mark for _, _, _, mark in all_marks])
        output += f"Total Records: {len(all_marks)}\n"
        output += f"Total Students: {len(data)}\n\n"
        
        output += "OVERALL MARKS STATISTICS:\n"
        output += "-" * 70 + "\n"
        output += f"Mean: {np.mean(all_marks_array):.2f}\n"
        output += f"Median: {np.median(all_marks_array):.2f}\n"
        output += f"Standard Deviation: {np.std(all_marks_array):.2f}\n"
        output += f"Minimum: {np.min(all_marks_array):.2f}\n"
        output += f"Maximum: {np.max(all_marks_array):.2f}\n"
        output += f"25th Percentile: {np.percentile(all_marks_array, 25):.2f}\n"
        output += f"75th Percentile: {np.percentile(all_marks_array, 75):.2f}\n\n"
        
        # Student-wise analysis
        output += "STUDENT-WISE PERFORMANCE:\n"
        output += "-" * 70 + "\n"
        output += f"{'Roll No':<12} {'Name':<20} {'Avg':<8} {'Total':<8} {'Grade':<8}\n"
        output += "-" * 70 + "\n"
        
        for roll_no, info in sorted(data.items()):
            avg = np.mean(info['marks'])
            total = np.sum(info['marks'])
            grade = self.calculate_grade(avg)
            output += f"{roll_no:<12} {info['name']:<20} {avg:<8.2f} {total:<8.0f} {grade:<8}\n"
        
        output += "\n" + "=" * 70 + "\n"
        
        # Subject-wise analysis
        subjects_data = {}
        for roll_no, name, subject, marks in all_marks:
            if subject not in subjects_data:
                subjects_data[subject] = []
            subjects_data[subject].append(marks)
        
        output += "\nSUBJECT-WISE STATISTICS:\n"
        output += "-" * 70 + "\n"
        output += f"{'Subject':<20} {'Mean':<10} {'Std Dev':<10} {'Min':<10} {'Max':<10}\n"
        output += "-" * 70 + "\n"
        
        for subject, marks_list in sorted(subjects_data.items()):
            marks_arr = np.array(marks_list)
            output += f"{subject:<20} {np.mean(marks_arr):<10.2f} {np.std(marks_arr):<10.2f} "
            output += f"{np.min(marks_arr):<10.2f} {np.max(marks_arr):<10.2f}\n"
        
        output += "=" * 70 + "\n"
        
        self.analysis_text.insert(tk.END, output)
    
    def calculate_grade(self, avg):
        """Calculate grade from average"""
        if avg >= 90:
            return 'A+'
        elif avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        else:
            return 'F'
    
    def generate_visualization(self):
        """Generate selected visualization"""
        # Clear previous canvas
        for widget in self.viz_canvas_frame.winfo_children():
            widget.destroy()
        
        # Get data
        all_marks = self.db.get_all_marks()
        
        if not all_marks:
            messagebox.showwarning("Warning", "No data available for visualization!")
            return
        
        chart_type = self.chart_var.get()
        
        # Create figure
        fig = plt.figure(figsize=(10, 6))
        
        if chart_type == "Student Performance Bar Chart":
            self.plot_student_performance(all_marks, fig)
        elif chart_type == "Subject-wise Average":
            self.plot_subject_average(all_marks, fig)
        elif chart_type == "Grade Distribution":
            self.plot_grade_distribution(all_marks, fig)
        elif chart_type == "Performance Heatmap":
            self.plot_heatmap(all_marks, fig)
        elif chart_type == "Box Plot by Subject":
            self.plot_boxplot(all_marks, fig)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def plot_student_performance(self, all_marks, fig):
        """Bar chart of student average performance"""
        data = {}
        for roll_no, name, subject, marks in all_marks:
            if roll_no not in data:
                data[roll_no] = {'name': name, 'marks': []}
            data[roll_no]['marks'].append(marks)
        
        students = []
        averages = []
        for roll_no, info in sorted(data.items()):
            students.append(f"{roll_no}\n{info['name'][:10]}")
            averages.append(np.mean(info['marks']))
        
        ax = fig.add_subplot(111)
        colors = sns.color_palette("husl", len(students))
        bars = ax.bar(range(len(students)), averages, color=colors, edgecolor='black')
        
        ax.set_xlabel('Students', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Marks', fontsize=12, fontweight='bold')
        ax.set_title('Student Performance Overview', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(students)))
        ax.set_xticklabels(students, rotation=45, ha='right')
        ax.axhline(y=60, color='r', linestyle='--', label='Pass Line (60)')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
    
    def plot_subject_average(self, all_marks, fig):
        """Bar chart of subject-wise averages"""
        subjects_data = {}
        for roll_no, name, subject, marks in all_marks:
            if subject not in subjects_data:
                subjects_data[subject] = []
            subjects_data[subject].append(marks)
        
        subjects = list(subjects_data.keys())
        averages = [np.mean(subjects_data[s]) for s in subjects]
        
        ax = fig.add_subplot(111)
        colors = sns.color_palette("Set2", len(subjects))
        bars = ax.bar(subjects, averages, color=colors, edgecolor='black')
        
        ax.set_xlabel('Subjects', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Marks', fontsize=12, fontweight='bold')
        ax.set_title('Subject-wise Average Performance', fontsize=14, fontweight='bold')
        ax.set_xticklabels(subjects, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
    
    def plot_grade_distribution(self, all_marks, fig):
        """Pie chart of grade distribution"""
        data = {}
        for roll_no, name, subject, marks in all_marks:
            if roll_no not in data:
                data[roll_no] = []
            data[roll_no].append(marks)
        
        grades = {'A+': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for roll_no, marks_list in data.items():
            avg = np.mean(marks_list)
            grade = self.calculate_grade(avg)
            grades[grade] += 1
        
        # Filter out zero values
        labels = [k for k, v in grades.items() if v > 0]
        sizes = [v for v in grades.values() if v > 0]
        
        ax = fig.add_subplot(111)
        colors = sns.color_palette("pastel", len(labels))
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            explode=[0.05] * len(labels)
        )
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        ax.set_title('Grade Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
    
    def plot_heatmap(self, all_marks, fig):
        """Heatmap of student-subject performance"""
        # Create pivot table
        df = pd.DataFrame(all_marks, columns=['Roll No', 'Name', 'Subject', 'Marks'])
        pivot = df.pivot_table(values='Marks', index='Roll No', columns='Subject', aggfunc='mean')
        
        ax = fig.add_subplot(111)
        sns.heatmap(
            pivot, 
            annot=True, 
            fmt='.1f', 
            cmap='RdYlGn', 
            cbar_kws={'label': 'Marks'},
            ax=ax,
            linewidths=0.5,
            vmin=0,
            vmax=100
        )
        
        ax.set_title('Student-Subject Performance Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Subjects', fontsize=12, fontweight='bold')
        ax.set_ylabel('Roll No', fontsize=12, fontweight='bold')
        plt.tight_layout()
    
    def plot_boxplot(self, all_marks, fig):
        """Box plot for subject-wise marks distribution"""
        df = pd.DataFrame(all_marks, columns=['Roll No', 'Name', 'Subject', 'Marks'])
        
        ax = fig.add_subplot(111)
        sns.boxplot(data=df, x='Subject', y='Marks', palette='Set3', ax=ax)
        
        ax.set_title('Marks Distribution by Subject', fontsize=14, fontweight='bold')
        ax.set_xlabel('Subjects', fontsize=12, fontweight='bold')
        ax.set_ylabel('Marks', fontsize=12, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = StudentPerformanceAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
