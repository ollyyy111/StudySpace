import tkinter as tk
import ttkbootstrap as ttk  # type: ignore
import json
import time
from tkinter import messagebox
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
current_subject = None
active_subject = None 
subjects_display = None
subject_dropdown = None

APP_BG = "#F8F9FA"         
PROGRESS_BG = "#F0D2DA"    
STATS_BG = "#EEEAFD"        
GOALS_BG = "#FCD1F5"       
SUBJECTS_BG = "#F8F2EF"

TITLE_FONT = ("Arial",24, "bold")
HEADING_FONT = ("Arial",16, "bold")
NORMAL_FONT = ("Arial",12)
SMALL_FONT = ("Arial",10)
CARD_FONT = ("Arial",14, "bold")
TIMER_FONT = ("Arial",28, "bold")

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
    except json.JSONDecodeError:
        return[]

def save_goals(goals):
    with open("goals.json","w") as file: 
        json.dump(
            {"goals": goals},
            file,
            indent=4
        ) 

def update_goal_progress(subject, minutes):
    global goals

    hours = minutes / 60

    for goal in goals:
        if goal["subject"] == subject:
            goal["completed_hours"] += hours

    save_goals(goals)
    refresh_goals()

                                

def delete_goal(goal):
    global goals

    if goal in goals:
        confirm = messagebox.askyesno(
            "Delete Goal",
            f"Delete '{goal['goal']}'?"
        )
    if confirm:    
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
        try:
            old_goal["target_hours"] = int(new_target)
        except ValueError:
            return

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

        if subject_dropdown:
            subject_dropdown["values"] = subjects

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
        "Computer": "💻",
        "Accountancy": "🧾",
        "Business Studies": "💼"
    }

    icon = icons.get(subject, "📖")

    SUBJECT_COLORS = {
        "Maths": "#FFE5A5",              
        "Physics": "#BDE0FE",            
        "Chemistry": "#CDB4DB",          
        "Biology": "#B7E4C7",           
        "English": "#FFC8DD",            
        "History": "#DDB892",            
        "Geography": "#A9DEF9",         
        "Computer Science": "#CDEAC0",  
        "Accountancy": "#FFD6A5",      
        "Business Studies": "#FFCAD4",  
        "Economics": "#D0F4DE",          
        "Political Science": "#E4C1F9",  
        "Hindi": "#FFCFD2",             
        "Sanskrit": "#BDE0C8",          
        "Art": "#FDE2E4",                
        "Physical Education": "#C9E4DE" 
    } 

    DEFAULT_COLORS = [
        "#FAD2E1",  
        "#CDEAC0",  
        "#BDE0FE", 
        "#FFF1A8",  
        "#FFD6A5",  
        "#E4C1F9",  
        "#C9E4DE",
        "#F1C0E8",  
        "#CFBAF0",
        "#A9DEF9"  
    ]

    if subject in SUBJECT_COLORS:
        card_color = SUBJECT_COLORS[subject]
    else:
        index = abs(hash(subject)) % len(DEFAULT_COLORS)  
        card_color = DEFAULT_COLORS[index]  

    card = tk.Frame(
        parent,
        bg=card_color,
        bd=0,
        relief="flat"
    )
    card.pack(
        fill="x",
        padx=10,
        pady=8,
        ipady=12
    )

    label = tk.Label(
        card,
        text=f"{icon} {subject}",
        bg=card_color,
        fg="#333333",
        font=CARD_FONT
    )
    label.pack(
        anchor="w",
        padx=10,
        pady=5
    )

    delete_button = ttk.Button(
        card,
        text="Delete",
        command=lambda: delete_subject(subject)
    )
    delete_button.pack(
        anchor="e",
        padx=10,
        pady=5
    )

    rename_button = ttk.Button(
        card,
        text="Rename",
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
    global active_subject

    if not current_subject.get():
        return
    
    if not running:
        running = True
        start_time = time.time()
        active_subject = current_subject.get()



def pause_timer():
    global running
    global elasped_time

    if not running:
        return
    
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
    global active_subject
    active_subject = None  

def save_study_session():
    global active_subject
    global elasped_time

    if not active_subject:
        return

    try:
        with open("study_data.json","r") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "sessions":[]
        } 

    minutes = max(1, elasped_time // 60)

    session = {
        "subject" : active_subject, 
        "minutes" : minutes
    } 

    data["sessions"].append(session)

    with open("study_data.json", "w") as file:
        json.dump(
            data, 
            file,
            indent=4
        )

    update_goal_progress(
        active_subject,
        minutes
    ) 

def get_today_stats():
    try:
        with open("study_data.json", "r") as file:
            data = json.load(file)

    except(FileNotFoundError, json.JSONDecodeError):
        return{
            "minutes" : 0,
            "sessions" : 0
        }

    total_minutes = 0
    session_count = 0

    for session in data.get("sessions", []):
        total_minutes += session.get(
            "minutes",
            0
        ) 
        session_count += 1

    return{
        "minutes" : total_minutes,
        "sessions" : session_count
    }

def get_subject_stats(subject):
    try:
        with open("study_data.json", "r") as file:
            data = json.load(file)

    except(FileNotFoundError, json.JSONDecodeError):
        return{
            "minutes":0,
            "sessions":0       
        }

    total = 0 
    count = 0

    for session in data.get("sessions",[]):
        if session["subject"] == subject:
            total += session["minutes"]
            count += 1

    return{
        "minutes": total,
        "sessions": count
    }         
                   



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

    try:
        target = int(target)

    except ValueError:
        return

    if target <= 0:
        return    

    if not goal_name or not subject or not target:
        return
    goal = {
        "goal": goal_name,
        "subject":subject,
        "target_hours":target,
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

    card = tk.Frame(
        parent,
        bg=GOALS_BG,
        padx=10,
        pady=10
    )

    card.pack(
        fill="x",
        padx=10,
        pady=5
    )

    tk.Label( 
        card,
        text=f"🎯 {goal['goal']}",
        bg=GOALS_BG,
        fg="#333333",
        font=("Arial",13, "bold")
    ).pack(anchor="w")

    tk.Label(
        card,
        text=f"Subject:{goal['subject']}",
        bg=GOALS_BG,
        fg="#333333"
    ).pack(anchor="w")

    completed = goal.get(
        "completed_hours",
        0
    )

    target = goal.get(
        "target_hours",
        1
    )

    if target <= 0:
        percentage = 0

    else:
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

def close_app():
    global running

    if running:
        save_study_session()

    app.destroy()    

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
    global current_subject
    global subject_dropdown
     
    app = ttk.Window(themename="cosmo")
    app.configure(
        background = APP_BG
    )
    app.title("StudySpace")
    app.geometry("1000x1500")
    app.minsize(
        800,
        700
    )

    main_canvas = tk.Canvas(
        app,
        bg=APP_BG,
        highlightthickness=0
        )

    main_scrollbar = ttk.Scrollbar(
        app,
        orient="vertical",
        command=main_canvas.yview
    )
    main_frame = tk.Frame(
        main_canvas,
        bg=APP_BG
        )
    
    def update_scroll_region(event=None):
        main_canvas.configure(
            scrollregion=main_canvas.bbox("all")
        )
        
    main_frame.bind(
        "<Configure>",
         update_scroll_region
    )

    canvas_window = main_canvas.create_window(
        (0,0),
        window=main_frame,
        anchor="nw"
    )

    main_canvas.bind(
        "<Configure>",
        lambda e : main_canvas.itemconfig(
            canvas_window,
            width=e.width
        )    
    )

    main_canvas.configure(
        yscrollcommand=main_scrollbar.set
    )

    def on_mousewheel(event):
        main_canvas.yview_scroll(
            int(-1*(event.delta/120)),
            "units"
        )

    main_canvas.bind_all(
        "<MouseWheel>",
        on_mousewheel
    )    

    main_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    main_scrollbar.pack(
        side="right",
        fill="y"
    )



    subjects = load_subjects()
    goals = load_goals()

    current_subject = tk.StringVar()

    if subjects:
        current_subject.set(subjects[0])

 

    title_label = ttk.Label(
        main_frame,
        text="StudySpace",
        font=TITLE_FONT
    )
    title_label.pack(pady=(30, 5))


    welcome_label = ttk.Label(
        main_frame,
        text="Your personal study companion.",
        font=NORMAL_FONT
    )
    welcome_label.pack(pady=(0, 25))

    progress_frame = tk.LabelFrame(
        main_frame,
        text="Today's Progress",
        bg=PROGRESS_BG,
        fg="#333333",
        padx=20,
        pady=20,
        font=HEADING_FONT
    )
    progress_frame.pack(
        fill="x",
        padx=40,
        pady=10
    )

    stats_frame = tk.LabelFrame(
        main_frame,
        text="Statistics",
        bg=STATS_BG,
        fg="#333333",
        padx=20,
        pady=20,
        font=HEADING_FONT
    )

    stats_frame.pack(
        fill="x",
        padx=40,
        pady=10
    )

    today_stats = get_today_stats()

    stats_label = tk.Label(
        stats_frame,
        bg=STATS_BG,
        fg="#333333",
        text=f"""
🕛 Total Study:{today_stats['minutes']} minutes
📚 Sessions: {today_stats['sessions']}
""" ,
        font=("Arial",12)
    )
    stats_label.pack()

    goals_frame = tk.LabelFrame(
        main_frame,
        text="Study Goals",
        bg=GOALS_BG,
        fg="#333333",
        padx=20,
        pady=20,
        font=HEADING_FONT
        )
    goals_frame.pack(
        fill="x",
        padx=40,
        pady=10
    ) 

    ttk.Label(
        goals_frame,
        text="Goal Name"
    ).pack()
    
    goal_entry = ttk.Entry(
        goals_frame,
        width=10
    )
    goal_entry.pack(pady=5)

    ttk.Label(
        goals_frame,
        text="Subject"
    ).pack()
 
    goal_subject_entry = ttk.Entry(
        goals_frame,
        width=30
    )
    goal_subject_entry.pack(pady=5)

    ttk.Label(
        goals_frame,
        text="Target Hours"
    ).pack()
 
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
    
    timer_label = tk.Label(
        progress_frame,
        text="00:00:00",
        bg=PROGRESS_BG,
        fg="#333333",
        font=TIMER_FONT
    )
    timer_label.pack(pady=10)

    tk.Label(
        progress_frame,
        text="Current Subject",
        bg=PROGRESS_BG,
        fg="#333333",
        font=NORMAL_FONT
    ).pack()

    subject_dropdown = ttk.Combobox(
        progress_frame,
        textvariable=current_subject,
        values=subjects,
        state="readonly",
        width=25
    )
    subject_dropdown.pack(
        pady=25
    )

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
        text="Reset",
        command=reset_timer
    )
    reset_button.pack(
        side="left",
        padx=5
    )

    subjects_frame = tk.LabelFrame(
        main_frame,
        text="Subjects",
        bg=SUBJECTS_BG,
        fg="#333333",
        padx=20,
        pady=20,
        font=HEADING_FONT
    )
    subjects_frame.pack(
        fill="both",
        padx=40,
        pady=5
    )

    ttk.Label(
        subjects_frame,
        text="Add New Subject"
    ).pack()

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

    

    subjects_display = tk.Frame(
        subjects_frame,
        bg=SUBJECTS_BG
    )

    subjects_display.pack(
        fill="x"

    )

    refresh_subjects()

    update_timer()
    refresh_goals()
    app.protocol(
        "WM_DELETE_WINDOW",
        close_app
    )
    app.mainloop()


if __name__ == "__main__":
    main()