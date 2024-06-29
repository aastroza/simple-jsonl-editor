import json
import tkinter as tk
from tkinter import filedialog, messagebox

class JSONLEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("JSONL Editor")
        self.master.geometry("800x600")  # Increased window size

        self.data = []
        self.current_index = 0

        self.create_widgets()

    def create_widgets(self):
        # File selection button
        self.load_button = tk.Button(self.master, text="Load JSONL File", command=self.load_file)
        self.load_button.pack(pady=10)

        # Text widget for displaying and editing JSON
        self.text_widget = tk.Text(self.master, height=30, width=100)  # Increased size
        self.text_widget.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Navigation buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        self.prev_button = tk.Button(button_frame, text="Previous", command=self.show_previous)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(button_frame, text="Next", command=self.show_next)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Changes", command=self.save_changes)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.save_file_button = tk.Button(button_frame, text="Save to File", command=self.save_to_file)
        self.save_file_button.pack(side=tk.LEFT, padx=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSONL files", "*.jsonl")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:  # Added UTF-8 encoding
                self.data = [json.loads(line) for line in file]
            self.current_index = 0
            self.show_current()

    def show_current(self):
        if self.data:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, json.dumps(self.data[self.current_index], indent=2, ensure_ascii=False))  # ensure_ascii=False for proper character display

    def show_previous(self):
        if self.current_index > 0:
            self.save_changes()
            self.current_index -= 1
            self.show_current()

    def show_next(self):
        if self.current_index < len(self.data) - 1:
            self.save_changes()
            self.current_index += 1
            self.show_current()

    def save_changes(self):
        if self.data:
            try:
                edited_json = json.loads(self.text_widget.get(1.0, tk.END))
                self.data[self.current_index] = edited_json
                #messagebox.showinfo("Success", "Changes saved successfully!")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format. Please correct and try again.")

    def save_to_file(self):
        if self.data:
            file_path = filedialog.asksaveasfilename(defaultextension=".jsonl", filetypes=[("JSONL files", "*.jsonl")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:  # Added UTF-8 encoding
                    for item in self.data:
                        json.dump(item, file, ensure_ascii=False)  # ensure_ascii=False for proper character writing
                        file.write('\n')
                messagebox.showinfo("Success", f"File saved successfully to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONLEditor(root)
    root.mainloop()