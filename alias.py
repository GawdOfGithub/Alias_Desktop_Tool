import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, font

class AliasManager(tk.Tk):
    """
    A desktop application to manage shell aliases for bash and zsh.
    It allows users to view, add, modify, and delete aliases, which are
    saved to the respective configuration files (~/.bashrc and ~/.zshrc).
    """

    def __init__(self):
        super().__init__()
        self.title("Shell Alias Manager")
        self.geometry("850x550")
        self.configure(bg="#2E3440")
        self.selected_alias_name = None # To track the selected alias for editing

        # --- Style Configuration ---
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Define custom fonts
        self.default_font = font.Font(family="Helvetica", size=10)
        self.title_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.mono_font = font.Font(family="Courier New", size=10)

        # Configure styles for widgets
        self.style.configure("TFrame", background="#2E3440")
        self.style.configure("TLabel", background="#2E3440", foreground="#ECEFF4", font=self.default_font)
        self.style.configure("TLabelFrame", background="#3B4252", bordercolor="#4C566A", relief="groove")
        self.style.configure("TLabelFrame.Label", background="#3B4252", foreground="#ECEFF4", font=self.title_font)
        self.style.configure("TButton", background="#5E81AC", foreground="#ECEFF4", font=self.default_font, borderwidth=0)
        self.style.map("TButton", background=[("active", "#81A1C1")])
        self.style.configure("TEntry", fieldbackground="#4C566A", foreground="#ECEFF4", bordercolor="#4C566A", insertbackground="#ECEFF4")

        # Style for Treeview (alias display)
        self.style.configure("Treeview",
            background="#3B4252",
            foreground="#D8DEE9",
            fieldbackground="#3B4252",
            rowheight=25,
            font=self.default_font
        )
        self.style.configure("Treeview.Heading",
            background="#434C5E",
            foreground="#ECEFF4",
            font=self.title_font,
            relief="flat"
        )
        self.style.map("Treeview.Heading", background=[("active", "#4C566A")])
        self.style.map("Treeview", background=[("selected", "#5E81AC")])

        # --- File Paths ---
        self.home_dir = os.path.expanduser("~")
        self.bash_file = os.path.join(self.home_dir, ".bashrc")
        self.zsh_file = os.path.join(self.home_dir, ".zshrc")
        
        # --- Main Layout ---
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self._create_display_panel()
        self._create_add_alias_panel()

        # Initial load of aliases
        self.load_aliases()

    def _create_display_panel(self):
        """Creates the left panel for displaying current aliases."""
        display_frame = ttk.LabelFrame(self.main_frame, text="Available Aliases", padding="10")
        display_frame.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="nsew")
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        # --- Treeview to display aliases ---
        columns = ("alias", "command")
        self.alias_tree = ttk.Treeview(display_frame, columns=columns, show="headings", selectmode="browse")
        self.alias_tree.heading("alias", text="Alias")
        self.alias_tree.heading("command", text="Command")
        self.alias_tree.column("alias", width=150, anchor="w")
        self.alias_tree.column("command", stretch=True, anchor="w")
        
        self.alias_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Bind selection event
        self.alias_tree.bind("<<TreeviewSelect>>", self._on_alias_select)

        # --- Scrollbar ---
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.alias_tree.yview)
        self.alias_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky="ns")
        
        # --- Action Buttons Frame ---
        action_frame = ttk.Frame(display_frame)
        action_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="ew")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        # --- Refresh Button ---
        refresh_button = ttk.Button(action_frame, text="Refresh List", command=self.load_aliases)
        refresh_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # --- Delete Button ---
        delete_button = ttk.Button(action_frame, text="Delete Selected", command=self.delete_alias)
        delete_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _create_add_alias_panel(self):
        """Creates the right panel for adding or modifying an alias."""
        add_frame = ttk.LabelFrame(self.main_frame, text="Add / Modify Alias", padding="10")
        add_frame.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="nsew")
        add_frame.grid_columnconfigure(1, weight=1)

        # --- Alias Name Input ---
        ttk.Label(add_frame, text="Alias Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.alias_name_entry = ttk.Entry(add_frame, width=40)
        self.alias_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # --- Command Input ---
        ttk.Label(add_frame, text="Command:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.command_entry = ttk.Entry(add_frame, width=40, font=self.mono_font)
        self.command_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # --- Buttons Frame ---
        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # --- Save Alias Button ---
        save_button = ttk.Button(button_frame, text="Save Alias", command=self.save_alias)
        save_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # --- Clear Form Button ---
        clear_button = ttk.Button(button_frame, text="Clear Form", command=self.clear_form)
        clear_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # --- Info/Instructions ---
        info_text = (
            "Instructions:\n"
            "1. To add, fill in the fields and click 'Save Alias'.\n"
            "2. To modify, select an alias, change its details, and click 'Save Alias'.\n\n"
            "The alias will be updated in both your .bashrc and .zshrc files.\n\n"
            "Important: For changes to take effect, restart your terminal or run:\n"
            "source ~/.bashrc\n"
            "source ~/.zshrc"
        )
        info_label = ttk.Label(add_frame, text=info_text, wraplength=350, justify=tk.LEFT)
        info_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

    def _on_alias_select(self, event=None):
        """Populates the form when an alias is selected from the list."""
        selected_items = self.alias_tree.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        alias_name, command = self.alias_tree.item(selected_item, "values")
        
        self.selected_alias_name = alias_name

        self.alias_name_entry.delete(0, tk.END)
        self.alias_name_entry.insert(0, alias_name)
        
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, command)

    def clear_form(self):
        """Clears the input fields and resets the selection state."""
        self.alias_name_entry.delete(0, tk.END)
        self.command_entry.delete(0, tk.END)
        self.selected_alias_name = None
        
        # Deselect any item in the treeview
        if self.alias_tree.selection():
            self.alias_tree.selection_remove(self.alias_tree.selection()[0])

    def _parse_aliases_from_file(self, file_path):
        """Reads a file and extracts all alias definitions."""
        aliases = {}
        if not os.path.exists(file_path):
            return aliases
        
        alias_pattern = re.compile(r"^\s*alias\s+([^=]+)=(['\"])(.*?)\2")
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    match = alias_pattern.match(line)
                    if match:
                        name = match.group(1).strip()
                        command = match.group(3).strip()
                        aliases[name] = command
        except IOError as e:
            messagebox.showerror("File Read Error", f"Could not read {file_path}:\n{e}")
        return aliases

    def load_aliases(self):
        """Loads aliases from both config files and populates the treeview."""
        self.clear_form() # Reset form state on load/refresh
        for item in self.alias_tree.get_children():
            self.alias_tree.delete(item)
            
        bash_aliases = self._parse_aliases_from_file(self.bash_file)
        zsh_aliases = self._parse_aliases_from_file(self.zsh_file)
        
        all_aliases = {**bash_aliases, **zsh_aliases}
        
        for name, command in sorted(all_aliases.items()):
            self.alias_tree.insert("", tk.END, values=(name, command))

    def _remove_alias_from_file(self, file_path, alias_name):
        """Reads a file, removes the specified alias, and rewrites the file."""
        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            alias_pattern = re.compile(r"^\s*alias\s+" + re.escape(alias_name) + r"=")

            with open(file_path, 'w') as f:
                for line in lines:
                    if not alias_pattern.match(line):
                        f.write(line)
        except IOError as e:
            messagebox.showerror("File I/O Error", f"Could not modify {file_path}:\n{e}")

    def save_alias(self):
        """Saves a new alias or updates an existing one."""
        new_alias_name = self.alias_name_entry.get().strip()
        command = self.command_entry.get().strip()

        if not new_alias_name or not command:
            messagebox.showwarning("Input Error", "Both alias name and command are required.")
            return
            
        # The check for spaces in alias names was removed as per user request.
        # Note: Aliases with spaces are not standard and may not work in all shells.
        # if " " in new_alias_name:
        #     messagebox.showwarning("Input Error", "Alias name cannot contain spaces.")
        #     return
        
        if self.selected_alias_name and self.selected_alias_name != new_alias_name:
             self._remove_alias_from_file(self.bash_file, self.selected_alias_name)
             self._remove_alias_from_file(self.zsh_file, self.selected_alias_name)

        self._remove_alias_from_file(self.bash_file, new_alias_name)
        self._remove_alias_from_file(self.zsh_file, new_alias_name)

        alias_string = f"alias {new_alias_name}='{command}'\n"

        try:
            if os.path.exists(self.bash_file):
                with open(self.bash_file, 'a') as f:
                    f.write(alias_string)

            if os.path.exists(self.zsh_file):
                 with open(self.zsh_file, 'a') as f:
                    f.write(alias_string)

            action = "updated" if self.selected_alias_name else "added"
            messagebox.showinfo("Success", f"Alias '{new_alias_name}' has been {action} successfully!")

            self.load_aliases()

        except IOError as e:
            messagebox.showerror("File Write Error", f"Could not write to config files:\n{e}")

    def delete_alias(self):
        """Deletes the selected alias from the config files."""
        if not self.selected_alias_name:
            messagebox.showwarning("Selection Error", "Please select an alias to delete.")
            return
            
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the alias '{self.selected_alias_name}'?"
        )

        if confirm:
            self._remove_alias_from_file(self.bash_file, self.selected_alias_name)
            self._remove_alias_from_file(self.zsh_file, self.selected_alias_name)
            
            messagebox.showinfo("Success", f"Alias '{self.selected_alias_name}' has been deleted.")
            self.load_aliases()


if __name__ == "__main__":
    app = AliasManager()
    app.mainloop()

