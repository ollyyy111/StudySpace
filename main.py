import tkinter as tk
import ttkbootstrap as ttk  # type: ignore
import json
import time
running = False
start_time = None
elasped_time = 0
app = None
timer_label = None
goals = []
goal_entry = None
goal_subject_entry = None
goal_target_entry = None 
goals_display = None 


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

def load_goals():
    try:
        with open("goals.json","r") as file:
            data=json.load(file)
            return data.get("goals",[]) 
    except FileNotFoundError:
        return[]

def save_goals(goals):
    with open("goals.json","w") as file: 
        json.dump(
            {"goals": goals},
            file,
            indent=4
        )             

def delete_goal(goal):
    global goals

    if goal in goals:
        goals.remove(goal)
        save_goals(goals)
        refresh_goals()

def edit_goal(old_goal):
    edit_window = tk.Toplevel()

    edit_window.title("Edit Goal")
    edit_window.geometry("300x250")
    edit_window.resizable(False, False)

    ttk.Label(
        edit_window,
        text="Goal Name"
    ).pack(pady=5)

    name_entry = ttk.Entry(edit_window, width=25)
    name_entry.pack()

    name_entry.insert(
        0,
        old_goal["goal"]
    ) 

    ttk.Label(
        edit_window,
        text="Subject"
    ).pack(pady=5)

    subject_entry_edit = ttk.Entry(
        edit_window,
        width=25
    )
    subject_entry_edit.pack()
    subject_entry_edit.insert(
        0,
        old_goal["subject"]
    )

    ttk.Label(
        edit_window,
        text="Target Hours"
    ).pack(pady=5)

    target_entry = ttk.Entry(
        edit_window,
        width=25
    )
    target_entry.pack()
    target_entry.insert(
        0,
        str(old_goal["target_hours"])
    )

    def save_edit():

        new_name = name_entry.get().strip()
        new_subject = subject_entry_edit.get().strip().title()
        new_target = target_entry.get().strip()

        if not new_name or not new_subject or not new_target:
            return

        old_goal["goal"] = new_name
        old_goal["subject"] = new_subject
        old_goal["target_hours"] = int(new_target)

        save_goals(goals)
        refresh_goals()

        edit_window.destroy()

    ttk.Button(
        edit_window,
        text="Save",
        command=save_edit
    ).pack(pady=15)    

       

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


def start_timer():
    global running
    global start_time

    if not running:
        running = True
        start_time = time.time()

def pause_timer():
    global running
    global elasped_time

    if running:
        elasped_time += int(time.time() - start_time)
        running = False
        save_study_session()
     

def reset_timer():
    global running
    global start_time 
    global elasped_time

    running = False
    start_time = None
    elasped_time = 0

    timer_label.config(
        text="00:00:00"
    )  

def save_study_session():
    data={
        "total_seconds": elasped_time
    }  
    with open("study_data.json","w")as file:
        json.dump(data, file, indent=4)


def update_timer():
    global elasped_time
    if running:
        current_time = int(time.time() - start_time + elasped_time)

        hours = current_time//3600
        minutes = (current_time%3600)//60
        seconds = current_time%60

        timer_label.config(
            text=f"{hours:02}:{minutes:02}:{seconds:02}"
        )

    app.after(1000, update_timer)

def add_goal():
    global goals

    goal_name = goal_entry.get().strip()
    subject = goal_subject_entry.get().strip().title()
    target = goal_target_entry.get().strip()

    if not goal_name or not subject or not target:
        return
    goal = {
        "goal": goal_name,
        "subject":subject,
        "target_hours":int(target),
        "completed_hours":0
    }
    goals.append(goal)
    save_goals(goals)
    refresh_goals()

    goal_entry.delete(0, tk.END)
    goal_subject_entry.delete(0, tk.END)
    goal_target_entry.delete(0, tk.END)

def refresh_goals():
    for widget in goals_display.winfo_children():
        widget.destroy()

    for goal in goals:
        create_goal_card(
            goals_display,
            goal
        )    

def create_goal_card(parent, goal):

    card = ttk.Frame(
        parent,
        padding=10
    )

    card.pack(
        fill="x",
        padx=10,
        pady=5
    )

    ttk.Label( 
        card,
        text=f"🎯 {goal['goal']}",
        font=("Arial",13, "bold")
    ).pack(anchor="w")

    ttk.Label(
        card,
        text=f"Subject:{goal['subject']}"
    ).pack(anchor="w")

    completed = goal.get(
        "completed_hours",
        0
    )

    target = goal.get(
        "target_hours",
        1
    )

    percentage = int(
        (completed / target) * 100
    )

    if percentage >= 100:
        status = "🟢 Completed"
    else:
        status = "🟡 In Progress"    

    ttk.Label(
        card,
        text=f"Progress: {percentage}%"
    ).pack(anchor="w")

    progress_bar = ttk.Progressbar(
        card,
        length=300,
        value=percentage
    )
    progress_bar.pack(
        anchor="w",
        pady=5
    )

    ttk.Label(
        card,
        text=f"{completed} / {target} hours"
    ).pack(anchor="w")

    ttk.Label(
        card,
        text=status
    ).pack(anchor="w")

    button_frame = ttk.Frame(card)
    button_frame.pack(
        anchor="e",
        pady=5
    )

    edit_button = ttk.Button(
        button_frame,
        text="✏️ Edit",
        command=lambda: edit_goal(goal)
    )

    edit_button.pack(
        side="left",
        padx=5
    )

    delete_button = ttk.Button(
        button_frame,
        text="🗑️ Delete",
        command=lambda: delete_goal(goal)
    )
    delete_button.pack(
        side="left",
        padx=5
    )

def main():
    global subjects
    global subject_entry
    global subjects_display
    global app
    global timer_label
    global goals
    global goal_entry
    global goal_subject_entry
    global goal_target_entry
    global goals_display
     
    app = ttk.Window(themename="cosmo")
    app.title("StudySpace")
    app.geometry("1000x1500")

    subjects = load_subjects()
    goals = load_goals()

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

    goals_frame = ttk.LabelFrame(
        app,
        text="Study Goals",
        padding=20
        )
    goals_frame.pack(
        fill="x",
        padx=40,
        pady=10
    ) 

    goal_entry = ttk.Entry(
        goals_frame,
        width=10
    )
    goal_entry.pack(pady=5)

    goal_subject_entry = ttk.Entry(
        goals_frame,
        width=30
    )
    goal_subject_entry.pack(pady=5)

    goal_target_entry = ttk.Entry(
        goals_frame,
        width=30
    )
    goal_target_entry.pack(pady=5)

    add_goal_button = ttk.Button(
        goals_frame, 
        text="➕ Add Goal",
        command=add_goal
    )
    add_goal_button.pack(pady=5)    

    goals_display = ttk.Frame(goals_frame)
    goals_display.pack(
        fill="x",
        pady=5
    )
    
    timer_label = ttk.Label(
        progress_frame,
        text="00:00:00",
        font=("Arial",24, "bold")
    )
    timer_label.pack(pady=10)

    button_frame = ttk.Frame(progress_frame)
    button_frame.pack(pady=10)

    start_button = ttk.Button(
        button_frame,
        text="▶️ Start",
        command=start_timer
    )
    start_button.pack(
        side="left",
        padx=5
    )

    pause_button = ttk.Button(
        button_frame,
        text="⏸️ Pause",
        command=pause_timer
    )
    pause_button.pack(
        side="left",
        padx=5
    )

    reset_button = ttk.Button(
        button_frame,
        text="🔀 Reset",
        command=reset_timer
    )
    reset_button.pack(
        side="left",
        padx=5
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
        pady=5
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

    canvas = tk.Canvas(
        subjects_frame,
        height=250
    )
    scrollbar = tk.Scrollbar(
        subjects_frame,
        orient="vertical",
        command=canvas.yview
    )

    subjects_display = ttk.Frame(canvas)
    def update_scroll(e):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    subjects_display.bind(
        "<Configure>",
        update_scroll
            
        )   

    canvas_frame = canvas.create_window(
        (0,0),
        window=subjects_display,
        anchor="nw"
    )  

    canvas.configure(
        yscrollcommand=scrollbar.set
    ) 

    canvas.pack(
        side="left",
        fill="both",
        expand=True,
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(
            canvas_frame,
            width=e.width

        )
    )

    refresh_subjects()

    update_timer()
    refresh_goals()
    app.mainloop()


if __name__ == "__main__":
    main()