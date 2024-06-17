import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

# ファイルを読み込む関数
def read_file_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()

# ファイルに新しい行を追加する関数
def append_to_file(filename, line):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(line + '\n')

# ファイルから指定行を削除する関数
def remove_line_from_file(filename, line_number):
    lines = read_file_lines(filename)
    if 1 <= line_number <= len(lines):
        del lines[line_number - 1]
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(lines)
    else:
        messagebox.showerror("エラー", "行番号が範囲外です")

# 問題を出題する関数
def load_question():
    global n, words, means
    words = read_file_lines('words.txt')
    means = read_file_lines('mean.txt')
    if words and means:
        n = random.randint(1, len(words))
        question_label.config(text=f"問題: {words[n - 1].strip()}")
        answer_label.config(text="")
    else:
        messagebox.showerror("エラー", "ファイルが空です")

# 回答を表示する関数
def show_answer():
    global n, means
    if n <= len(means):
        answer_label.config(text=f"答え: {means[n - 1].strip()}")
    else:
        answer_label.config(text="答えが見つかりません")

# 用語と意味を追加するためのウィンドウ
def add_word_meaning():
    def on_submit():
        word = word_entry.get().strip()
        meaning = meaning_entry.get().strip()
        if word and meaning:
            append_to_file('words.txt', word)
            append_to_file('mean.txt', meaning)
            add_window.destroy()
            messagebox.showinfo("成功", "用語と意味を追加しました")
        else:
            messagebox.showerror("エラー", "両方のフィールドに値を入力してください")

    add_window = tk.Toplevel(root)
    add_window.title("用語と意味を追加")
    add_window.geometry("400x200")
    add_window.config(bg='#f0f0f0')

    frame = ttk.Frame(add_window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="用語:", font=("Arial", 12)).pack(pady=5)
    word_entry = ttk.Entry(frame, width=50, font=("Arial", 12))
    word_entry.pack(pady=5)

    ttk.Label(frame, text="意味:", font=("Arial", 12)).pack(pady=5)
    meaning_entry = ttk.Entry(frame, width=50, font=("Arial", 12))
    meaning_entry.pack(pady=5)

    ttk.Button(frame, text="決定", command=on_submit).pack(pady=10)

# 指定された行を削除するためのウィンドウ
def delete_word_meaning():
    def on_submit():
        try:
            line_number = int(line_entry.get().strip())
            remove_line_from_file('words.txt', line_number)
            remove_line_from_file('mean.txt', line_number)
            delete_window.destroy()
            messagebox.showinfo("成功", "行を削除しました")
        except ValueError:
            messagebox.showerror("エラー", "有効な数字を入力してください")

    delete_window = tk.Toplevel(root)
    delete_window.title("行を削除")
    delete_window.geometry("400x200")
    delete_window.config(bg='#f0f0f0')

    frame = ttk.Frame(delete_window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="行番号:", font=("Arial", 12)).pack(pady=5)
    line_entry = ttk.Entry(frame, width=50, font=("Arial", 12))
    line_entry.pack(pady=10)

    ttk.Button(frame, text="決定", command=on_submit).pack(pady=10)

# words.txtとmean.txtからデータを読み込む
words = read_file_lines('words.txt')
means = read_file_lines('mean.txt')

# GUIの設定
root = tk.Tk()
root.title("用語クイズ")
root.geometry("400x250")
root.config(bg='#f8f8f8')

# メニューバーの設定
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="ファイル", menu=file_menu)
file_menu.add_command(label="追加", command=add_word_meaning)
file_menu.add_command(label="削除", command=delete_word_meaning)

# カスタムスタイルの定義
style = ttk.Style()
style.configure("TLabel", background="#f8f8f8", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TEntry", font=("Arial", 12), padding=5)

# 問題ラベル
question_label = ttk.Label(root, text="問題: ", font=("Arial", 16, "bold"))
question_label.pack(pady=10)

# 回答ボタン
answer_button = ttk.Button(root, text="答えを表示", command=show_answer)
answer_button.pack(pady=5)

# 次の問題ボタン
next_button = ttk.Button(root, text="次の問題", command=load_question)
next_button.pack(pady=5)

# 答えラベル
answer_label = ttk.Label(root, text="", font=("Arial", 16))
answer_label.pack(pady=10)

# 初めての問題を読み込む
load_question()

# メインループ
root.mainloop()
