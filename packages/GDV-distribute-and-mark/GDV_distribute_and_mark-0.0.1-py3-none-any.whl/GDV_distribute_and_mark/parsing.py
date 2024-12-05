# coding: utf-8

import argparse
import os


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GDV_distribute_and_mark helps to distribute GDV scans. ")

    parser.add_argument("gdv_path", type=str, help="Path to folder with pictures of GDV scans. ")

    parser.add_argument("db_path", type=str, help="Path to json databases with classes definition. "
                                                  "It creates new if does not exists. ")

    return parser.parse_args()
