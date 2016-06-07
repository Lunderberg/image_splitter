#!/usr/bin/env python2

from ensure_venv import ensure_venv
ensure_venv('requirements.txt', python='python2')

import os
import sys
import Tkinter as tk
import tkFileDialog
import tkMessageBox

from PIL import Image
sys.path.append(os.path.join(os.path.dirname(__file__),
                             'autocrop'))
from autocrop import MultiPartImage, Background

def image_splitter(background_filename, scanned_image_filename, output_dir):
    background_image = Image.open(background_filename)
    background = Background().load_from_image(background_image, dpi=200)
    images = Image.open(scanned_image_filename)
    split_images = MultiPartImage(images, background, dpi=200)

    base_name, ext = os.path.splitext(os.path.basename(scanned_image_filename))


    for i, pic in enumerate(split_images):
        output_filename = os.path.join(output_dir,
                                       '{}_{}.{}'.format(base_name,i,ext))
        pic.save(output_filename)

class MainWindow(object):

    def __init__(self):
        self.input_filenames = []

        self.window = tk.Tk()
        self._setup_GUI()

    def _setup_GUI(self):
        self.window.wm_title('Image Splitter')

        frame = tk.Frame(self.window)
        button = tk.Button(frame,
                           text='Select Input Files',
                           command=self.SelectInputFiles)
        button.pack(side=tk.LEFT)
        frame.pack()

        frame = tk.Frame(self.window)
        self.background_image_entry = tk.Entry(frame)
        self.background_image_entry.pack(side=tk.LEFT)
        button = tk.Button(frame,
                           text='Select Background Image',
                           command=self.SelectBackgroundImage)
        button.pack(side=tk.LEFT)
        frame.pack()

        frame = tk.Frame(self.window)
        self.output_dir_entry = tk.Entry(frame)
        self.output_dir_entry.pack(side=tk.LEFT)
        button = tk.Button(frame,
                           text='Select Output Dir',
                           command=self.SelectOutputDir)
        button.pack(side=tk.LEFT)
        frame.pack()

        frame = tk.Frame(self.window)
        button = tk.Button(frame,
                           text="Split 'Em",
                           command=self.SplitFiles)
        button.pack()
        frame.pack()

    def Run(self):
        self.window.mainloop()

    def SelectInputFiles(self,*args):
        filenames = tkFileDialog.askopenfilenames()
        if filenames:
            self.input_filenames = filenames

    def SelectBackgroundImage(self,*args):
        filename = tkFileDialog.askopenfilename()
        if filename:
            self.background_image_entry.delete(0,tk.END)
            self.background_image_entry.insert(0,filename)

    def SelectOutputDir(self,*args):
        filename = tkFileDialog.askdirectory()
        if filename:
            self.output_dir_entry.delete(0,tk.END)
            self.output_dir_entry.insert(0,filename)

    def SplitFiles(self,*args):
        background_image = self.background_image_entry.get()
        output_dir = self.output_dir_entry.get()
        input_filenames = self.input_filenames

        try:
            for input_filename in input_filenames:
                image_splitter(background_image, input_filename, output_dir)
        except Exception as e:
            tkMessageBox.showerror(title="Error!!?!",
                                   message=str(e))

if __name__=='__main__':
    window = MainWindow()
    window.Run()
