# coding: utf-8

from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from io import BytesIO
import os
from ksupk import get_files_list


def hits_to_percents(hit_list: list) -> list:
    return [round(x / sum(hit_list), 2) for x in hit_list] if sum(hit_list) != 0 else [0.0 for _ in hit_list]


def create_histogram_man(percentages, width=400, height=300):
    bar_width = width // len(percentages)
    max_height = height - 20

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    for i, perc in enumerate(percentages):
        bar_height = int(perc * max_height)
        x0 = i * bar_width
        y0 = height - bar_height
        x1 = x0 + bar_width - 10  # Пробел между столбиками
        y1 = height
        draw.rectangle([x0, y0, x1, y1], fill="blue")

        text = f"{perc:.2f}"
        text_x = x0 + (bar_width - 10) // 2
        text_y = y0 - 15
        draw.text((text_x, text_y), text, fill="black")

    return img


def create_histogram(percentages):
    fig, ax = plt.subplots(figsize=(4, 2))
    x = list(range(len(percentages)))
    ax.bar(x, percentages, color='skyblue', tick_label=[f"Class {i}" for i in x])
    ax.set_title("Class percentages")
    ax.set_ylabel("Percentages")
    ax.set_ylim(0, 1)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)


def get_gdv_dict(folder_path: str):
    """
    :param folder_path: path to folder with GDV scans
    :return: dict like this {"GDV_scan_id": "/path/to/picture", ...}
    """
    pic_ext = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tiff", ".bmp"}
    files = get_files_list(folder_path)
    d = {}
    for file_i in files:
        file_i_name = os.path.basename(file_i)
        n, e = os.path.splitext(file_i_name)
        n, e = str(n), str(e).lower()
        if e in pic_ext:
            d[n] = os.path.abspath(file_i)

    return d
