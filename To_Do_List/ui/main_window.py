import customtkinter as ctk
import darkdetect
from ui.components import TaskRow, TaskDetailModal
from models.task import Task
import database
from utils.helpers import COLORS

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lumina Tasks")
        self.geometry("1100x750")
        self.configure(fg_color=COLORS["background"])
        
        # Set theme early
        if darkdetect.isDark():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        # Initialize DB
        database.init_db()
        self.current_filter = "All"
        self.search_query = ""

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_content()
        
        # Load initial data
        self._set_filter("All")

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=COLORS["surface"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        # Logo
        logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Lumina Tasks", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"), 
            text_color=COLORS["primary"]
        )
        logo_label.grid(row=0, column=0, padx=24, pady=(32, 32), sticky="w")
        
        # Navigation Filters
        self.filter_buttons = {}
        filters = ["All", "Today", "Upcoming", "Completed"]
        for i, f in enumerate(filters):
            btn = ctk.CTkButton(
                self.sidebar_frame, text=f, anchor="w", fg_color="transparent", text_color=COLORS["text"],
                hover_color=COLORS["outline"], font=ctk.CTkFont(family="Inter", size=15),
                height=40, corner_radius=8,
                command=lambda f_type=f: self._set_filter(f_type)
            )
            btn.grid(row=i+1, column=0, padx=16, pady=4, sticky="ew")
            self.filter_buttons[f] = btn
            
        # Priority Labels
        ctk.CTkLabel(
            self.sidebar_frame, text="PRIORITY", 
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"), 
            text_color=COLORS["text_secondary"]
        ).grid(row=5, column=0, padx=24, pady=(32, 12), sticky="w")
        
        pri_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        pri_frame.grid(row=6, column=0, padx=20, sticky="ew")
        
        for pri, col_key in [("High", "priority_high"), ("Medium", "priority_medium"), ("Low", "priority_low")]:
            btn = ctk.CTkButton(
                pri_frame, text=pri, fg_color=COLORS[col_key], text_color="#ffffff",
                hover_color=COLORS["primary_hover"], height=32, width=64, corner_radius=8,
                font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
                command=lambda p=pri: self._set_filter(p)
            )
            btn.pack(side="left", padx=(4, 4))

        # Theme toggle at the bottom
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame, text="Dark Mode", command=self._toggle_theme, 
            fg_color=COLORS["outline"], progress_color=COLORS["primary"],
            font=ctk.CTkFont(family="Inter", size=14)
        )
        self.theme_switch.grid(row=8, column=0, padx=24, pady=32, sticky="s")
        if darkdetect.isDark():
            self.theme_switch.select()

    def _create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Top Bar
        top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 32))
        top_bar.grid_columnconfigure(1, weight=1)
        
        self.view_title = ctk.CTkLabel(
            top_bar, text="All Tasks", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold"), 
            text_color=COLORS["text"]
        )
        self.view_title.grid(row=0, column=0, sticky="w")
        
        self.search_entry = ctk.CTkEntry(
            top_bar, placeholder_text="Search tasks...", width=280, height=44, corner_radius=12,
            fg_color=COLORS["surface"], border_color=COLORS["outline"], border_width=2,
            font=ctk.CTkFont(family="Inter", size=14)
        )
        self.search_entry.grid(row=0, column=1, sticky="e")
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Scrollable Task List
        self.task_list = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.task_list.grid(row=1, column=0, sticky="nsew")
        self.task_list.grid_columnconfigure(0, weight=1)
        
        # FAB
        self.add_btn = ctk.CTkButton(
            self.main_frame, text="+", width=64, height=64, corner_radius=32,
            font=ctk.CTkFont(size=28, weight="bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            command=self._open_add_modal
        )
        # Using place for floating button
        self.add_btn.place(relx=1.0, rely=1.0, anchor="se")

    def _set_filter(self, filter_type):
        self.current_filter = filter_type
        
        if filter_type in ["High", "Medium", "Low"]:
            self.view_title.configure(text=f"{filter_type} Priority Tasks")
        else:
            self.view_title.configure(text=f"{filter_type} Tasks" if filter_type != "All" else "All Tasks")
        
        # Highlight active nav filter
        for name, btn in self.filter_buttons.items():
            if name == filter_type:
                btn.configure(fg_color=COLORS["outline"])
            else:
                btn.configure(fg_color="transparent")
                
        self.refresh_tasks()

    def _on_search(self, event):
        self.search_query = self.search_entry.get().strip()
        self.refresh_tasks()

    def _toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def refresh_tasks(self):
        # Clear existing
        for widget in self.task_list.winfo_children():
            widget.destroy()
            
        tasks = database.get_tasks(self.current_filter, self.search_query)
        
        if not tasks:
            empty_lbl = ctk.CTkLabel(
                self.task_list, text="No tasks found. Enjoy your day!", 
                font=ctk.CTkFont(family="Inter", size=16), text_color=COLORS["text_secondary"]
            )
            empty_lbl.pack(pady=80)
            return

        for task in tasks:
            row = TaskRow(
                self.task_list, task=task,
                on_edit=self._open_edit_modal,
                on_delete=self._delete_task,
                on_toggle=self._toggle_task
            )
            row.pack(fill="x", pady=6)

    def _open_add_modal(self):
        TaskDetailModal(self, None, self._save_task)
        
    def _open_edit_modal(self, task: Task):
        TaskDetailModal(self, task, self._save_task)
        
    def _save_task(self, task: Task):
        if task.id is None:
            database.add_task(task)
        else:
            database.update_task(task)
        self.refresh_tasks()
        
    def _delete_task(self, task: Task):
        database.delete_task(task.id)
        self.refresh_tasks()
        
    def _toggle_task(self, task: Task):
        database.toggle_complete(task.id, task.completed)
        self.refresh_tasks()
