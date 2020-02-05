# Flashcard-Viewer
A flashcard viewer that takes as input a pdf file.


I wrote this without knowing any of the libraries (so its probably not optimal at all). 
Improvised in an afternoon in order to visualize my iPad notes as flashcards. 
I made this work using this [pdf template](readme_material/flashcard_h_temp.pdf).

Idea
====
-  Finds all the pdfs in the main directory (a bit messy, need change)
-  Can load one pdf in the dropdown menu 
-  Create images for each page of the pdf and divides the image in 2 (done only once)
   -  The left half of the page is the question
   -  The right half is the answer
-  (conversion is pretty slow, so it might take some minutes if there are a lot of flashcards)
-  Can randomize the order of the cards and visualize the back and the front of each card.

Dependencies
====
- tkinter
- PyPDF2
- PIL
- wand.image
- numpy


TODO
====
- find better way to convert pdf pages to images
- have a parameter for setting the cut of the pdf (e.g instead of exact middle one can have [0,300] is question and [300,1000])
- allow horizontal cuts
  - in case there are multiple flashcards on a page (e.g. 4 flashcards on an A4 page)


![Screen](readme_material/screen_example.jpg)
