import json
import os
import uuid

from utils.time_helper import get_current_timestamp

class NoteManager:
    def __init__(self):
        self.file_path = "data/notes.json"
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.notes = self.load_notes()
    
    def load_notes(self):
        """Load notes from the json file
        returns a list of note dictionaries. Else return an 
        empty list if does not exist or is empty/corrupted."""
        
        if not os.path.exists(self.file_path):
            return []    

        try:
            with open(self.file_path, "r", encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    return []
                else:
                    return json.loads(content)
                
        except (json.JSONDecodeError, IOError):
            return []

        
    def save_notes(self):
        """ Saves notes to json file."""
        with open(self.file_path, "w", encoding='utf-8') as file:
            json.dump(self.notes, file, indent=4)

    def create_note(self, title, content, tags):
        """Create a new note and save it"""
        new_note = {
            "id": str(uuid.uuid4()), 
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": get_current_timestamp(),
            "updated_at": None
        }
        self.notes.append(new_note)
        self.save_notes()

        return new_note

    def delete_note(self, note_id):
        """Delete notes by its id """
        original_count = len(self.notes)

        self.notes = [note for note in self.notes if note["id"] != note_id]
        if len(self.notes) < original_count:
            self.save_notes()
            return True       # If id is deleted
        return False          # If id was not found 

    def search_notes(self, query):
        """Search notes by query string across title, content, and tags."""
        query = query.lower() # This makes the search case-insensative.

        return [
            note for note in self.notes   # Filter with list comprehension
            if (
                query in note["title"].lower()      # Check inside title
                or query in note["content"].lower() # Check inside content 
                or any(query in tag.lower() for tag in note.get("tags", []))
            )   
                # Check if the query exist in any of the tags.
        ]
