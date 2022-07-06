import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from bs4 import BeautifulSoup as Bs
import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry

root = tk.Tk()
root.title("Decision Makers Tool")
root.geometry("500x300")

titleslist = []  # list to store titles
nameslist = []  # list to store names
fonrlist = []  # fo_nummer lista / list to store company numbers
x = 0


def select_file():
    filename = fd.askopenfile(
        title="open a file",
        initialdir="/",
    )

    for files in filename:
        global x  # set x as 0 and after that increment by one
        x += 1
        root.update_idletasks()
        newfo_nr = files.strip().zfill(8)
        fonrlist.append(newfo_nr)
        root.after(200, print(""))  # sleep for 2 seconds
        url = f"https://www.asiakastieto.fi/yritykset/fi/{newfo_nr}/paattajat"
        s = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount(url, HTTPAdapter(max_retries=retries))
        page = s.get(url, timeout=30)
        label.configure(text="Please wait...\nloading decision maker info")
        num_label.config(text=x)
        info_label.config(text="companies saved\nto Excel")
        soup = Bs(page.content, "html.parser")
        names = soup.find_all(attrs={"data-title": "Nimi"})
        titles = soup.find_all(attrs={"data-title": "Asema"})
        for name in names:
            nameslist.append(name.text)
            for title in titles:
                titleslist.append(title.text)
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
    df = pd.DataFrame(list(zip(fonrlist, titleslist, nameslist)))  # works
    label.config(text="Process done")

    try:
        # with block automatically closes file
        with fd.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name, header=False, index=False)
    except AttributeError:
        # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
        label.config(text="User cancelled save")


num_label = Label(root, text="")
info_label = Label(root, text="")
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
num_label.pack()
info_label.pack()
exit_button.pack(expand=True)
root.mainloop()
