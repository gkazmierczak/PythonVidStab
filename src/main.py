import greyscale
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

if __name__ == "__main__":
    Tk().withdraw()
    inputFilePath = askopenfilename(title="Select file to convert")
    if inputFilePath == "":
        messagebox.showerror("File error", "No file selected")
        exit(-1)
    outputFilePath = asksaveasfile(title="Save file as")
    if outputFilePath == None:
        messagebox.showerror("File error", "No path specified")
        exit(-1)
    greyscale.convertToGreyscale(inputFilePath, outputFilePath.name, compress=True)
