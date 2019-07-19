from tkinter import PhotoImage

class Format:
    def __init__(self, file_type, format_type)
        #file_type is like txt, pdf, py
        #format_type is like document, video, image
        self.file_type = file_type
        self.format_type = format_type
        self.short_format = self.format_type[:3]
        self.icon = self.define_icon()
    
    def define_icon(self):
        return PhotoImage(
            file="/icons/{}".format(self.format_type)
        )