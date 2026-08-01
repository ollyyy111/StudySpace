import tkinter as tk
import ttkbootstrap as ttk  # type: ignore
import json


def load_subjects():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
            return data.get("subjects", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_subjects(subjects):
    with open("config.json", "w") as file:
        json.dump(
            {"subjects": subjects},
            file,
            indent=4
        )


def add_subject(subject_list, subject_name):
    subject_name = subject_name.strip().title()

    if not subject_name:
        return False

    if subject_name in subject_list:
        return False

    subject_list.append(subject_name)
    save_subjects(subject_list)
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
        create_subject_card(
            subjects_display,
            subject
        )

def delete_subject(subject_name):
    global subjects

    if subject_name in subjects:
        subjects.remove(subject_name)
        save_subjects(subjects)
        refresh_subjects()

def rename_subject(old_subject):
    rename_window = tk.Toplevel()
    rename_window.title("Rename Subject")
    rename_window.geometry("300x150")  
    rename_window.resizable(False, False)  

    ttk.Label(
        rename_window,
        text=f"Rename '{old_subject}'"
    ).pack(pady=10) 

    new_name_entry = ttk.Entry(rename_window, width=25)
    new_name_entry.pack(pady=5)
    new_name_entry.focus()

    def save_new_name():
        global subjects

        new_name = new_name_entry.get().strip().title()

        if not new_name:
            return

        if new_name in subjects:
            return

        index = subjects.index(old_subject)
        subjects[index] = new_name

        save_subjects(subjects) 
        refresh_subjects()

        rename_window.destroy()

    ttk.Button(
        rename_window,
        text="Save",
        command=save_new_name
    ).pack(pady=10)          

def create_subject_card(parent, subject):

    icons = {
        "Maths": "📐",
        "Mathematics": "📐",
        "Science": "🔬",
        "English": "📚",
        "History": "🏛️",
        "Computer": "💻"
    }

    icon = icons.get(subject, "📖")

    colors = {
        "Maths": "#FFE5B4",
        "Mathematics": "#FFE5B4",
        "Science": "#C8F7C5",
        "English": "#CDE7FF",
        "History": "#FFD6E8",
        "Computer": "#E5D4FF"
    }

    card_color = colors.get(subject, "#FFFFFF")

    card = tk.Frame(
        parent,
        bg=card_color,
        bd=1,
        relief="solid"
    )
    card.pack(
        fill="x",
        padx=10,
        pady=6,
        ipady=8
    )

    label = tk.Label(
        card,
        text=f"{icon} {subject}",
        bg=card_color,
        font=("Arial", 14, "bold")
    )
    label.pack(
        anchor="w",
        padx=10,
        pady=5
    )

    delete_button = ttk.Button(
        card,
        text="🗑️ Delete",
        command=lambda: delete_subject(subject)
    )
    delete_button.pack(
        anchor="e",
        padx=10,
        pady=5
    )

    rename_button = ttk.Button(
        card,
        text="✏️ Rename",
        command=lambda: rename_subject(subject)
    )
    rename_button.pack(
        anchor="e",
        padx=10,
        pady=5
    )


def main():
    global subjects
    global subject_entry
    global subjects_display

    app = ttk.Window(themename="cosmo")
    app.title("StudySpace")
    app.geometry("950x650")

    subjects = load_subjects()

    title_label = ttk.Label(
        app,
        text="StudySpace",
        font=("Arial", 14)
    )
    title_label.pack(pady=(30, 5))

    welcome_label = ttk.Label(
        app,
        text="Your personal study companion.",
        font=("Arial", 14)
    )
    welcome_label.pack(pady=(0, 25))

    progress_frame = ttk.LabelFrame(
        app,
        text="Today's Progress",
        padding=20
    )
    progress_frame.pack(
        fill="x",
        padx=40,
        pady=10
    )

    subjects_frame = ttk.LabelFrame(
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
    subject_entry.focus()

    add_subject_button = ttk.Button(
        subjects_frame,
        text="➕ Add Subject",
        command=handle_add_subject
    )
    add_subject_button.pack(pady=5)

    subjects_display = ttk.Frame(subjects_frame)
    subjects_display.pack(
        fill="both",
        expand=True,
        pady=10
    )


    refresh_subjects()

    app.mainloop()


if __name__ == "__main__":
    main()