"""This id going to be the central hub of the app. It shows the list of all notes,
the search bar, and the button to create a new note."""

import customtkinter as ctk
from core.note_manager import NoteManager
from ui.note_editor import NoteEditor

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Single shared NoteManager instance
        self.note_manager = NoteManager()
        
        # Windows setup
        self.title("My Notebook")
        self.geometry("700x500")

        # Build ui
        self.build_ui()
    
    def open_new_note(self):
        """Open the noteEditor for editing note."""
        NoteEditor(self, self.note_manager, self.refresh_note_list)

    def open_edit_note(self, note):
        """Open the NoteEditor for editing an existing note."""
        NoteEditor(self, self.note_manager, self.refresh_note_list, note=note)
    
    def delete_note(self, note_id):
        """Delete a note and refresh the UI."""
        self.note_manager.delete_note(note_id)
        self.refresh_note_list()

    def build_ui(self):
        """Build main ui Components."""

        # --- Top Frame (search + button) ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', padx=10, pady=10)

        # Search Entry
        self.search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search Notes...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Search Button
        search_button = ctk.CTkButton(top_frame, text="Search", command=self.search_notes)
        search_button.pack(side="left", padx=5)

        # New Note Button
        new_note_button = ctk.CTkButton(top_frame, text="New Note", command=self.open_new_note)
        new_note_button.pack(side="left", padx=5)

        # --- Notes List Frame ---
        self.notes_frame = ctk.CTkScrollableFrame(self)
        self.notes_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate notes on launch
        self.refresh_note_list()
    
    def _render_notes(self, notes):
        """Render a list of notes in the UI."""

        # Clear existing widgets
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        
        # Render each note
        for note in notes:
            note_frame = ctk.CTkFrame(self.notes_frame)
            note_frame.pack(fill="x", padx=5, pady=5)

            title_label = ctk.CTkLabel(note_frame, text=note.get("title", "Untitled"), 
                                       font=('Arial', 14, 'bold'))
            title_label.pack(anchor="w", padx=5, pady=2)

            created_label = ctk.CTkLabel(note_frame, text=f"Created: {note.get('created_at', '')}")

            created_label.pack(anchor="w", padx=5)

            tags = ", ".join(note.get("tags", []))
            tags_label = ctk.CTkLabel(note_frame, text=f"Tags: {tags}")

            tags_label.pack(anchor='w', padx=5, pady=2)

            button_frame = ctk.CTkFrame(note_frame)
            button_frame.pack(anchor="e", padx=5, pady=5)

            open_button = ctk.CTkButton(button_frame, text="Open", 
                                        command=lambda n=note: self.open_edit_note(n))

            open_button.pack(side="left", padx=5)

            delete_button = ctk.CTkButton(button_frame, text="Delete", 
                                          command=lambda nid=note["id"]: self.delete_note(nid))

            delete_button.pack(side="left", padx=5)


    def refresh_note_list(self):
        """Display all notes."""
        self._render_notes(self.note_manager.notes)
    
    def search_notes(self):
        """Search notes and display results."""
        query = self.search_entry.get()
        results = self.note_manager.search_notes(query)

        self._render_notes(results)

