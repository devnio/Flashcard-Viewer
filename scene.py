import tkinter as tk
import os
from flashcards import Flashcards
from PIL import ImageTk
from PIL import Image as PILImage

class Scene:
    def __init__(self):
        self._root = tk.Tk()

        self.flashcards = None

        self.popupMenu = None
        self.tkvar_deck = tk.StringVar(self._root)
        self.pdfs_found = False
        self.pdfs_list = ["No pdf file found. Load one inside the main directory."]
        self._find_pdfs()
        self.tkvar_deck.set(self.pdfs_list[0])

        self._setup_drop_down_menu()

        self.show_answer = False
        self.imgA = None
        self.imgQ = None
        self.label = None

        self.next_BT = None
        self.turn_BT = None
        self.load_pdf_BT = None
        self.randomize_order_BT = None
        self._setup_buttons()
        
    def load_flashcards(self):
        if not self.pdfs_found:
            print("Need some pdfs first. Place a pdf in the same directory as the main script.")
            return 

        flashcards = Flashcards(resolution=350)
        flashcards.load_pdf(self.tkvar_deck.get())
        flashcards.start()
        self.flashcards = flashcards
        self.load_current_flashcard()

    def randomize_order(self):
        if self.flashcards is None:
            self.load_flashcards()
            return
            
        self.flashcards.randomize_order()

    def _find_pdfs(self):
        for filename in os.listdir("."):
            if filename.endswith(".pdf"):
                if (self.pdfs_found == False):
                    self.pdfs_list = []
                    self.pdfs_found = True

                self.pdfs_list.append(filename)

    def next_cards(self):        
        if self.flashcards is None:
            self.load_flashcards()
            return
        
        self.show_answer = False
        self.flashcards.load_next_card()
        self.load_current_flashcard()

    def load_current_flashcard(self):
        self.imgQ = ImageTk.PhotoImage(self.flashcards.current_question_img)
        self.imgA = ImageTk.PhotoImage(self.flashcards.current_answer_img)

        # Not ideal.. quick hack
        if (self.label is not None):
             self.label.destroy()

        self._show_img(self.imgQ)

    def turn_card(self):
        if self.flashcards is None:
            self.load_flashcards()
            return            

        img = self.imgA
        self.show_answer = not self.show_answer
        
        if not self.show_answer:
            img = self.imgQ
        
        self.label.destroy()
        self._show_img(img)

    def _show_img(self, img):
        self.label = tk.Label(self._root, image=img)
        self.label.image = self.imgA
        self.label.place(x = 0, y = 0)
        self.label.pack()
    
    def _setup_buttons(self):
        self.load_pdf_BT = tk.Button(self._root, text='load pdf', command=self.load_flashcards)
        self.load_pdf_BT.pack()

        self.randomize_order_BT = tk.Button(self._root, text='randomize', command=self.randomize_order)
        self.randomize_order_BT.pack()

        self.next_BT = tk.Button(self._root, text='next card', command=self.next_cards)
        self.next_BT.pack()

        self.turn_BT = tk.Button(self._root, text='turn card', command=self.turn_card)
        self.turn_BT.pack()
    
    def _setup_drop_down_menu(self):
        self.popupMenu = tk.OptionMenu(self._root, self.tkvar_deck, *self.pdfs_list)
        self.popupMenu.pack()

    def runMainLoop(self):
        self._root.mainloop()