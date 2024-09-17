import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from rules import Rule
from constants import rules_data_file
from dataFormatter import load_file,save_file

class HIDSGUI:
    def __init__(self, master):
        self.master = master
        self.rules = load_file(rules_data_file)
        self.master.title("Host Intrusion Detection System")
        self.master.geometry("1000x600")

        self.create_widgets()

    def create_widgets(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        # Rules tab
        self.rules_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_frame, text="Rules")

        # Create Treeview
        self.tree = ttk.Treeview(self.rules_frame, columns=("ID", "Level", "Category", "Description", "Patterns"), show="headings")
        self.tree.heading("ID", text="Rule ID")
        self.tree.heading("Level", text="Level")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Patterns", text="Patterns")

        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Level", width=50)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=300)
        self.tree.column("Patterns", width=400)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.rules_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid layout for treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons frame
        btn_frame = ttk.Frame(self.rules_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Add rule button
        add_btn = ttk.Button(btn_frame, text="Add Rule", command=self.add_rule)
        add_btn.pack(side=tk.LEFT, padx=5)

        # Edit rule button
        edit_btn = ttk.Button(btn_frame, text="Edit Rule", command=self.edit_rule)
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Delete rule button
        delete_btn = ttk.Button(btn_frame, text="Delete Rule", command=self.delete_rule)
        delete_btn.pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        self.rules_frame.grid_rowconfigure(0, weight=1)
        self.rules_frame.grid_columnconfigure(0, weight=1)

        self.update_rules_treeview()

    def update_rules_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rule in self.rules:
            self.tree.insert("", "end", values=(rule.id, rule.level, rule.category, rule.description, ", ".join(rule.patterns)))

    def add_rule(self):
        id = simpledialog.askstring("Add Rule", "Enter rule ID:")
        level = simpledialog.askinteger("Add Rule", "Enter rule level:")
        description = simpledialog.askstring("Add Rule", "Enter rule description:")
        category = simpledialog.askstring("Add Rule", "Enter rule category:")
        patterns = simpledialog.askstring("Add Rule", "Enter patterns")
        
        new_rule = Rule(id, level, description, category, patterns)
        self.rules.append(new_rule)
        save_file(self.rules,rules_data_file)
        self.update_rules_treeview()

    def edit_rule(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Rule", "Please select a rule to edit.")
            return

        item = self.tree.item(selected_item)
        index = self.tree.index(selected_item)
        rule = self.rules[index]

        rule.id = simpledialog.askstring("Edit Rule", "Enter new ID:", initialvalue=rule.id)
        rule.level = simpledialog.askinteger("Edit Rule", "Enter new level:", initialvalue=rule.level)
        rule.description = simpledialog.askstring("Edit Rule", "Enter new description:", initialvalue=rule.description)
        rule.category = simpledialog.askstring("Edit Rule", "Enter new category:", initialvalue=rule.category)
        rule.patterns = simpledialog.askstring("Edit Rule", "Enter new patterns:", initialvalue=", ".join(rule.patterns))

        self.update_rules_treeview()
        save_file(self.rules,rules_data_file)


    def delete_rule(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Rule", "Please select a rule to delete.")
            return

        index = self.tree.index(selected_item)
        del self.rules[index]
        self.update_rules_treeview()
        save_file(self.rules,rules_data_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = HIDSGUI(root)
    root.mainloop()