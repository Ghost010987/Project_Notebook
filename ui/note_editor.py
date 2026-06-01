
import customtkinter as ctk
from core.spell_checker import NoteSpellChecker

class NoteEditor(ctk.CTkToplevel):
    def __init__(self, parent, note_manager, on_save_callback, note=None):
        super().__init__(parent)
        
        self.note_manager = note_manager
        self.spell_checker = NoteSpellChecker()
        self.on_save_callback = on_save_callback
        self.note = note

        # Windows title
        self.title("Edit Note" if note else "New Note")

        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """ Build all ui components. """

        # Title Entry
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(padx=10, pady=5, fill='x')

        # Content Textbox
        self.content_textbox = ctk.CTkTextbox(self, height=200)
        self.content_textbox.pack(padx=10, pady=5, fill='both', expand=True)

        # Tag Entry
        self.tag_entry = ctk.CTkEntry(self, placeholder_text="Tags (comma separated)")
        self.tag_entry.pack(padx=10, pady=5, fill='x')

        # Font family OptionMenu
        self.font_family_var = ctk.StringVar(value="Arial")
        self.font_family_menu = ctk.CTkOptionMenu(
            self,
            values=["Arial", "Courier", "Helvetica"],
            variable=self.font_family_var,
            command=lambda _: self.apply_font()
        )

        self.font_family_menu.pack(padx=10, pady=5)

        # Font size OptionMenu

        self.font_size_var = ctk.StringVar(value='14')
        self.font_size_menu = ctk.CTkOptionMenu(
            self,
            values=["12", "14", "16", "18", "20"],
            variable=self.font_size_var,
            command=lambda _: self.apply_font()
        )
        self.font_size_menu.pack(padx=10, pady=5)

        # Buttons
        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_note)
        self.save_button.pack(padx=10, pady=5)

        self.spell_button = ctk.CTkButton(self, text="Correct Spelling", command=self.apply_spell_check)
        self.spell_button.pack(padx=10, pady=5)

        # Pre-fill if editing
        if self.note:
            self.title_entry.insert(0, self.note.get("title", ""))
            self.content_textbox.insert("1.0", self.note.get("content", ""))
            self.tag_entry.insert(0, ", ".join(self.note.get("tags", [])))
        
        # Apply initial font
        self.apply_font()

    def apply_spell_check(self):
        """Apply spell correction to the content textbox."""
        content = self.content_textbox.get("1.0", "end-1c")
        corrected = self.spell_checker.correct_text(content)

        self.content_textbox.delete("1.0", "end")
        self.content_textbox.insert("1.0", corrected)

    def save_note(self):
        """Save the note (create for now)"""
        title = self.title_entry.get()
        content = self.content_textbox.get("1.0", "end-1c")
        tags_input = self.tag_entry.get()

        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

        if self.note is None:
            self.note_manager.create_note(title, content, tags)
        else:
            # TODO: update existing note
            pass

        self.on_save_callback()
        self.destroy()
    
    def apply_font(self):
        """Apply selected font to the textbox"""
        family = self.font_family_var.get()
        size = int(self.font_size_var.get())

        self.content_textbox.configure(font=(family, size))

