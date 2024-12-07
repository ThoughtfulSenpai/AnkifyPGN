import tkinter as tk
from tkinter import filedialog, messagebox

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convert PGN file to ANKI Deck")
        self.root.geometry("400x300")

        self.loaded_data = ""

        # Load Button
        self.load_button = tk.Button(root, text="Load File", command=self.load_file, width=20, height=2)
        self.load_button.pack(pady=20)

        # Convert Button
        self.convert_button = tk.Button(root, text="Convert to Flashcards", command=self.convert_to_flashcards, state=tk.DISABLED, width=20, height=2)
        self.convert_button.pack(pady=20)

        # Save Button
        self.save_button = tk.Button(root, text="Save Flashcards", command=self.save_flashcards, state=tk.DISABLED, width=20, height=2)
        self.save_button.pack(pady=20)

    def load_file(self):
        # Open file dialog to select a .txt or .pgn file
        file_path = filedialog.askopenfilename(filetypes=[("PGN Files", "*.pgn"), ("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.loaded_data = file.read()
                messagebox.showinfo("File Loaded", "File loaded successfully!")
                self.convert_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def convert_to_flashcards(self):
        if self.loaded_data:
            try:
                games = []
                current_game = []

                # Process the PGN content line by line
                for line in self.loaded_data.splitlines():
                    stripped_line = line.strip()

                    # Start of a new game is indicated by "[Event "
                    if stripped_line.startswith("[Event "):
                        if current_game:  # If a game is already being accumulated, save it
                            games.append(" ".join(current_game).strip())
                            current_game = []
                    current_game.append(stripped_line)  # Add line to the current game

                if current_game:  # Add the last game if it exists
                    games.append(" ".join(current_game).strip())

                self.flashcards = games
                messagebox.showinfo("Conversion Successful", f"{len(games)} games processed into flashcards!")
                self.save_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process PGN file: {e}")
        else:
            messagebox.showwarning("No Data", "No file loaded to convert.")

    def save_flashcards(self):
        if hasattr(self, 'flashcards') and self.flashcards:
            # Save flashcards to a new file
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write("\n".join(self.flashcards))  # Save each game as a line
                    messagebox.showinfo("File Saved", "Flashcards saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            messagebox.showwarning("No Flashcards", "No flashcards available to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
