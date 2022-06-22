import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


root = tk.Tk()
root.title("Decision makers info")
root.geometry("400x300")

titleslist = []  # list to store titles
nameslist = []  # list to store names
fonrlist = []  # fo_nummer lista / list to store company numbers


def select_file():
    filetypes = (
        ("text files", "*txt",
         "excel files", "*xlsx")
    )

    filename = fd.askopenfile(
        title="open a file",
        initialdir="/",
    )
    for files in filename:
        label.configure(text="Please wait...\nloading decision maker info...")
        root.update_idletasks()
        newfo_nr = files.strip().zfill(8)
        fonrlist.append(newfo_nr)
        root.after(200, print("..."))  # sleep for a random time
        url = f"https://www.asiakastieto.fi/yritykset/fi/{newfo_nr}/paattajat"
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        names = soup.find_all(attrs={"data-title": "Nimi"})
        titles = soup.find_all(attrs={"data-title": "Asema"})
        for title in titles:
            titleslist.append(title.text)
            for name in names:
                nameslist.append(name.text)
                number_of_names = len(nameslist)
                number_of_fo_nr = len(fonrlist)
                sumfo = number_of_names - number_of_fo_nr
                for i in range(sumfo):
                    if i < sumfo:
                        fonrlist.append(newfo_nr.strip())
                        if title == " ":
                            break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue
        break
    df = pd.DataFrame(list(zip(fonrlist, titleslist, nameslist))) # works
    label.config(text="Process done")

    try:
        # with block automatically closes file
        with fd.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name, header=False, index=False)
    except AttributeError:
        # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
        label.config(text="User cancelled save")


label = Label(root, text="Choose file")
open_button = ttk.Button(
    root,
    text="Open a file",
    command=select_file
)
exit_button = ttk.Button(
    root,
    text="Exit",
    command=root.destroy
)
open_button.pack(expand=True)
label.pack()
exit_button.pack(expand=True)
root.mainloop()