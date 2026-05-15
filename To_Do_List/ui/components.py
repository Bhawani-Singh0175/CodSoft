import customtkinter as ctk
from utils.helpers import COLORS, format_date
from models.task import Task
from typing import Callable, Optional
from datetime import datetime

class TaskRow(ctk.CTkFrame):
    def __init__(self, master, task: Task, on_edit: Callable, on_delete: Callable, on_toggle: Callable, **kwargs):
        super().__init__(master, fg_color=COLORS["surface"], corner_radius=12, **kwargs)
        self.task = task
        self.on_edit_cb = on_edit
        self.on_delete_cb = on_delete
        self.on_toggle_cb = on_toggle
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        
        # Checkbox
        self.checkbox_var = ctk.BooleanVar(value=task.completed)
        self.checkbox = ctk.CTkCheckBox(
            self, text="", variable=self.checkbox_var, width=24,
            command=self._on_toggle,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            border_color=COLORS["outline"]
        )
        self.checkbox.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="w")
        
        # Task Details (Title and Labels)
        details_frame = ctk.CTkFrame(self, fg_color="transparent")
        details_frame.grid(row=0, column=1, sticky="ew", padx=8)
        
        title_color = COLORS["text_secondary"] if task.completed else COLORS["text"]
        title_font = ctk.CTkFont(family="Inter", size=16, weight="bold" if not task.completed else "normal", overstrike=task.completed)
        self.title_label = ctk.CTkLabel(details_frame, text=task.title, font=title_font, text_color=title_color)
        self.title_label.pack(anchor="w")
        
        # Labels and Priority
        metadata_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        metadata_frame.pack(anchor="w", fill="x", pady=(4, 0))
        
        priority_color = COLORS.get(f"priority_{task.priority.lower()}", COLORS["primary"])
        self.priority_badge = ctk.CTkLabel(
            metadata_frame, text=f"  {task.priority}  ", font=ctk.CTkFont(family="Inter", size=10, weight="bold"),
            fg_color=priority_color, text_color="#ffffff", corner_radius=4
        )
        self.priority_badge.pack(side="left", padx=(0, 8))
        
        if task.labels:
            self.labels_badge = ctk.CTkLabel(
                metadata_frame, text=f"  {task.labels}  ", font=ctk.CTkFont(family="Inter", size=10),
                fg_color=COLORS["outline"], text_color=COLORS["text"], corner_radius=4
            )
            self.labels_badge.pack(side="left")
            
        # Due Date
        date_str = format_date(task.due_date)
        self.date_label = ctk.CTkLabel(self, text=date_str, font=ctk.CTkFont(family="Inter", size=12), text_color=COLORS["text_secondary"])
        self.date_label.grid(row=0, column=2, padx=16)
        
        # Actions
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=0, column=3, padx=(0, 16))
        
        self.edit_btn = ctk.CTkButton(
            actions_frame, text="Edit", width=40, height=28,
            fg_color="transparent", hover_color=COLORS["outline"], text_color=COLORS["primary"],
            command=self._on_edit
        )
        self.edit_btn.pack(side="left", padx=(0, 4))
        
        self.delete_btn = ctk.CTkButton(
            actions_frame, text="Delete", width=40, height=28,
            fg_color="transparent", hover_color=COLORS["outline"], text_color=COLORS["error"],
            command=self._on_delete
        )
        self.delete_btn.pack(side="left")

    def _on_toggle(self):
        self.task.completed = self.checkbox_var.get()
        self.on_toggle_cb(self.task)
        
    def _on_edit(self):
        self.on_edit_cb(self.task)
        
    def _on_delete(self):
        self.on_delete_cb(self.task)

class TaskDetailModal(ctk.CTkToplevel):
    def __init__(self, master, task: Optional[Task], on_save: Callable):
        super().__init__(master)
        self.title("Add Task" if not task else "Edit Task")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["background"])
        
        self.on_save = on_save
        self.task = task
        
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._populate_data()
        
    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=24, pady=24)
        
        # Title
        ctk.CTkLabel(main_frame, text="Task Title", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.title_entry = ctk.CTkEntry(main_frame, height=40, fg_color=COLORS["surface"], border_color=COLORS["outline"])
        self.title_entry.pack(fill="x", pady=(0, 16))
        
        # Description
        ctk.CTkLabel(main_frame, text="Description", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.desc_entry = ctk.CTkTextbox(main_frame, height=80, fg_color=COLORS["surface"], border_color=COLORS["outline"], border_width=2)
        self.desc_entry.pack(fill="x", pady=(0, 16))
        
        # Due Date
        ctk.CTkLabel(main_frame, text="Due Date (YYYY-MM-DD)", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.date_entry = ctk.CTkEntry(main_frame, height=40, fg_color=COLORS["surface"], border_color=COLORS["outline"])
        self.date_entry.pack(fill="x", pady=(0, 16))
        
        # Priority & Labels Frame
        row_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=(0, 24))
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)
        
        # Priority
        pri_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        pri_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkLabel(pri_frame, text="Priority", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_menu = ctk.CTkOptionMenu(
            pri_frame, values=["Low", "Medium", "High"], variable=self.priority_var,
            fg_color=COLORS["surface"], button_color=COLORS["primary"], button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"]
        )
        self.priority_menu.pack(fill="x")
        
        # Labels
        lab_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        lab_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        ctk.CTkLabel(lab_frame, text="Labels (comma separated)", font=ctk.CTkFont(family="Inter", size=14, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.labels_entry = ctk.CTkEntry(lab_frame, height=28, fg_color=COLORS["surface"], border_color=COLORS["outline"])
        self.labels_entry.pack(fill="x")
        
        # Save Button
        self.save_btn = ctk.CTkButton(
            main_frame, text="Save Task", height=44,
            font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            command=self._save
        )
        self.save_btn.pack(fill="x", pady=(16, 0))

    def _populate_data(self):
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.desc_entry.insert("1.0", self.task.description)
            self.date_entry.insert(0, self.task.due_date)
            self.priority_var.set(self.task.priority)
            self.labels_entry.insert(0, self.task.labels)
        else:
            # Set default due date to today
            today = datetime.now().strftime("%Y-%m-%d")
            self.date_entry.insert(0, today)

    def _save(self):
        title = self.title_entry.get().strip()
        if not title:
            # Simple validation
            self.title_entry.configure(border_color=COLORS["error"])
            return
            
        description = self.desc_entry.get("1.0", "end").strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority_var.get()
        labels = self.labels_entry.get().strip()
        
        if self.task:
            self.task.title = title
            self.task.description = description
            self.task.due_date = due_date
            self.task.priority = priority
            self.task.labels = labels
            new_task = self.task
        else:
            new_task = Task(title=title, description=description, due_date=due_date, priority=priority, labels=labels)
            
        self.on_save(new_task)
        self.destroy()
