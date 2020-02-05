import os
import io
import copy 
import numpy as np
import PyPDF2
from wand.image import Image
from PIL import ImageTk
from PIL import Image as PILImage

class Flashcards():
    def __init__(self, resolution):

        self.res = resolution

        self.current_loaded_img = None
        self.current_question_img = None
        self.current_answer_img = None

        self.idx = 0
        self.src_pdf = None
        self.src_pdf_path = None
        self.curr_imgs_directory = None
        self.max_pages = None

        self.cards_order = []
        
    def load_pdf(self, src_pdf_path):
        """ Loads the pdf. """
        self.src_pdf_path = src_pdf_path

        dirName = os.path.splitext(self.src_pdf_path)[0]
        self.curr_imgs_directory = dirName

        self.src_pdf = PyPDF2.PdfFileReader(src_pdf_path)
        self.max_pages = self.src_pdf.getNumPages()
        self.cards_order = [i for i in range (0, self.max_pages)]

    def start(self):
        """ Create images from the pdf and store it in a new directory. If the directory already exists only just initialize. """
        if (os.path.isdir(self.curr_imgs_directory)):
            print("Directory exists, means that images are already created.")
        else:
            self._create_flashcard_imgs()

        self._set_current_img()

    def load_next_card(self):
        if self.idx < self.max_pages - 1:
            self.idx = self.idx + 1
            self._set_current_img()
        else: 
            print("No more flashcards")

    def randomize_order(self):
        self.idx = 0
        arr = np.random.permutation(self.cards_order)
        self.cards_order = arr.tolist()

    def _set_current_img(self):
        self.current_answer_img = PILImage.open(self.curr_imgs_directory + "/A" + str(self.cards_order[self.idx]) + ".jpg")
        self.current_question_img = PILImage.open(self.curr_imgs_directory + "/Q" + str(self.cards_order[self.idx]) + ".jpg")

    #===============================
    # Saving images
    #===============================
    def _create_flashcard_imgs(self):
        os.makedirs(self.curr_imgs_directory, exist_ok=True)
        for i in range (0, self.max_pages):
            self._save_page_as_img(i)

    def _save_page_as_img(self, idx):
        self._pdf_page_to_png(idx, resolution=self.res)
        self._cut_images_in_2(idx)
        self._save_curr_imgs(idx)

    def _save_curr_imgs(self, idx):
        self.current_question_img.save(self.curr_imgs_directory + "/Q" + str(idx) + ".jpg", "JPEG") # this works
        self.current_answer_img.save(self.curr_imgs_directory + "/A" + str(idx) + ".jpg", "JPEG") # this works

    #===============================
    # Transform pdfs into images
    #===============================
    def _cut_images_in_2(self, idx):
        img = self.current_loaded_img

        halfImgWidth = int(img.width / 2)
        
        self.current_question_img = img.clone()
        self.current_question_img.crop(right=halfImgWidth)

        img.crop(left=halfImgWidth)
        self.current_answer_img = img

        filter_type = 'lanczos'
        self.current_question_img.resize(850, 632, filter_type)
        self.current_answer_img.resize(850, 632, filter_type)
        
        # self.current_question_img.sharpen(radius=3, sigma=1.5)
        # self.current_answer_img.sharpen(radius=3, sigma=1.5)

        self.current_answer_img = self._convert_wand_to_pil(self.current_answer_img)
        self.current_question_img = self._convert_wand_to_pil(self.current_question_img)
        

    def _pdf_page_to_png(self, pagenum = 0, resolution = 72):
        """
        Returns specified PDF page as wand.image.Image png.
        :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
        :param int pagenum: Page number to take.
        :param int resolution: Resolution for resulting png in DPI.
        """
        dst_pdf = PyPDF2.PdfFileWriter()
        dst_pdf.addPage(self.src_pdf.getPage(pagenum))

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file = pdf_bytes, resolution = resolution)
        img.convert("jpg")

        self.current_loaded_img = img

    def _convert_wand_to_pil(self, wand_img):
        img_buffer = np.asarray(bytearray(wand_img.make_blob(format='jpg')), dtype='uint8')
        bytesio = io.BytesIO(img_buffer)
        pil_img = PILImage.open(bytesio)
        return pil_img