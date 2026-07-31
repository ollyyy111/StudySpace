import tkinter as tk
import ttkbootstrap as ttk  # type: ignore
import json

def load_subjects():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
            return data.get("subjects",[])
    except FileNotFoundError:
        return[]
    except json.JSONDecodeError:
        return[]

def save_subjects(subjects):
    with open("config.json","w") as file:
        json.dump(
            {"subjects": subjects},
            file,
            indent=4
        )    

def add_subject(subjects, subject_name):
    subject_name = subject_name.strip().title()

    if not subject_name:
        return False

    if subject_name in subjects:
        return False
    
    subjects.append(subject_name)
    save_subjects(subjects)
    return True  

def handle_add_subject():
    global subjects 

    subject_name = subject_entry.get()

    if add_subject(subjects, subject_name):
        refresh_subjects()
        subject_entry.delete(0, tk.END)  

def refresh_subjects():
    for widget in subjects_display.winfo_children():
        widget.destroy()

    for subject in subjects:
        subject_label = ttk.Label(
            subjects_display,
            text=subject
        )                 
        subject_label.pack(anchor="w", padx=10, pady=2)

def main():
    global subjects
    global subject_entry
    global subjects_display

    app = ttk.Window(themename="cosmo")
    app.title("StudySpace")
    app.geometry("900x600")
    subjects = load_subjects() 
    

    title_label = ttk.Label(
        app,
        text="StudySpace",
        font=("Arial", 14)
    )
    title_label.pack(pady = (30 , 5))

    welcome_label = ttk.Label(
        app,
        text="Your personal study companion.",
        font=("Arial", 14)
    )  
    welcome_label.pack(pady = (0 , 25))

    progress_frame = ttk.Labelframe(
        app,
        text="Today's Progress",
        padding=20
    )
    progress_frame.pack(
        fill="x",
        padx=40,
        pady=10
    )

    subjects_frame = ttk.Labelframe(
        app,
        text="Subjects",
        padding=20
    )
    subjects_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=10
    )

    subject_entry = ttk.Entry(
        subjects_frame,
        width=30
    )
    subject_entry.pack(pady=10)

    add_subject_button = ttk.Button(
        subjects_frame,
        text="Add Subject",
        command=handle_add_subject
    )
    add_subject_button.pack(pady=5)

    subjects_display = ttk.Frame(subjects_frame)
    subjects_display.pack(fill="both", expand=True, pady=10)

    refresh_subjects()

    app.mainloop()

if __name__ == "__main__":
    main()   