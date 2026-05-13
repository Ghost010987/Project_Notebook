""" This module is going to take a string of text and return it with misspelled
    words corrected."""

from spellchecker import SpellChecker as PySpellChecker

class NoteSpellChecker:
    def __init__(self):
        """ Intialize the spell checker instance"""
        self.spell = PySpellChecker()
        
    def correct_text(self, text):
        """
        Correct misspelled words in the given text.
        Args:
            text(str): The input string.
        Returns: 
            str: The corrected string. 
        
        """
        words = text.split()
        corrected_words = []

        for word in words:
            corrected = self.spell.correction(word)

            if corrected is None:
                corrected_words.append(word)
            
            else:
                corrected_words.append(corrected)
        
        return " ".join(corrected_words)
    
    
    
         
