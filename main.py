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
    subject_name = subject_name.strip()

    if not subject_name:
        return False

    subjects.append(subject_name)
    save_subjects(subjects)
    return True          

def main():
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

    app.mainloop()

if __name__ == "__main__":
    main()   