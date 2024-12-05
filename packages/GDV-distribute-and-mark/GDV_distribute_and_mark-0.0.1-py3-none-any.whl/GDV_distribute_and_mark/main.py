# coding: utf-8

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from GDV_distribute_and_mark.db import DB
from GDV_distribute_and_mark.parsing import get_args
from GDV_distribute_and_mark.resource_manager import ResourceManager
from GDV_distribute_and_mark.class_definition_logic import get_gdv_dict, create_histogram, hits_to_percents
from ksupk import singleton_decorator, get_files_list

@singleton_decorator
class ImageViewerApp:
    def __init__(self, root, gdv_path: str):
        self.root = root
        self.root.title("GDV scans defenition. ")
        self.root.iconphoto(False, tk.PhotoImage(file=ResourceManager().ico_path()))
        # self.root.geometry("400x400")

        self.images = get_files_list(gdv_path)
        self.d = get_gdv_dict(gdv_path)
        self.ids = sorted(map(int, list(self.d.keys())))

        self.current_index = DB().current()
        self.image_hits = DB().hits(self.current_index)
        self.photo = self.load_image(self.current_index)
        self.hist = self.load_hist(self.current_index)

        self.title_label = Label(self.root, text=str(self.current_index), font=("Arial", 24))
        self.title_label.grid(row=0, column=0, columnspan=3)

        self.image_label = Label(self.root, image=self.photo)
        self.image_label.grid(row=1, column=0, columnspan=3)

        self.hist_label = Label(self.root, image=self.hist)
        self.hist_label.grid(row=2, column=0, columnspan=3)

        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("1", lambda e: self.up_score(0))
        self.root.bind("q", lambda e: self.down_score(0))
        self.root.bind("2", lambda e: self.up_score(1))
        self.root.bind("w", lambda e: self.down_score(1))
        self.root.bind("3", lambda e: self.up_score(2))
        self.root.bind("e", lambda e: self.down_score(2))

    def load_image(self, index: int):
        img = Image.open(
            self.d[str(index)]
        )
        # img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)

    def load_hist(self, index: int):
        hits = DB().hits(index)
        percents = hits_to_percents(hits)
        img = create_histogram(percents)
        return ImageTk.PhotoImage(img)

    def update_image(self):
        self.photo = self.load_image(self.current_index)
        self.hist = self.load_hist(self.current_index)
        self.title_label.config(text=str(self.current_index))
        self.image_label.config(image=self.photo)
        self.hist_label.config(image=self.hist)

    def next_image(self, event=None):
        self.current_index += 1
        if self.current_index > self.ids[ len(self.ids) - 1 ]:
            self.current_index = self.ids[0]
        self.update_image()

    def prev_image(self, event=None):
        self.current_index -= 1
        if self.current_index < self.ids[0]:
            self.current_index = self.ids[ len(self.ids) - 1 ]
        self.update_image()

    def up_score(self, class_num: int):
        hits = DB().hits(self.current_index)
        hits[class_num] += 1
        DB().update(self.current_index, hits)
        self.update_image()

    def down_score(self, class_num: int):
        hits = DB().hits(self.current_index)
        hits[class_num] = hits[class_num]-1 if hits[class_num]-1 >= 0 else 0
        DB().update(self.current_index, hits)
        self.update_image()


def main():
    args = get_args()
    DB(args.db_path)
    root = tk.Tk()
    app = ImageViewerApp(root, args.gdv_path)
    root.mainloop()


if __name__ == "__main__":
    main()
