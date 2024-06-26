import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import os

# メインウィンドウを作成
root = tk.Tk()
root.title("用語クイズ")
root.geometry("400x300")
root.config(bg='#f8f8f8')

# モードの状態を保持する変数
mode = tk.StringVar(value="word_to_meaning")  # 初期モードを「単語から意味」に設定

# セクション選択のための変数
current_section = tk.StringVar()

# セクションリストの読み込み
def load_sections():
    return [f.split('_')[0] for f in os.listdir() if f.endswith('_words.txt')]

# セクションリストの初期化
sections = load_sections()

# ファイルを読み込む関数
def read_file_lines(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    return []

# ファイルに新しい行を追加する関数
def append_to_file(filename, line):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(line + '\n')

# ファイルから指定された行を削除する関数
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
    if not current_section.get():
        messagebox.showerror("エラー", "セクションを選択してください")
        return

    words = read_file_lines(f'{current_section.get()}_words.txt')
    means = read_file_lines(f'{current_section.get()}_means.txt')

    if words and means:
        n = random.randint(1, len(words))
        if mode.get() == "word_to_meaning":
            question_label.config(text=f"問題: {words[n - 1].strip()}")
        else:
            question_label.config(text=f"問題: {means[n - 1].strip()}")
        answer_label.config(text="")
    else:
        messagebox.showerror("エラー", "ファイルが空です")

# 回答を表示する関数
def show_answer():
    global n, words, means
    try:
        if mode.get() == "word_to_meaning":
            if n <= len(means):
                answer_label.config(text=f"答え: {means[n - 1].strip()}")
            else:
                answer_label.config(text="答えが見つかりません")
        else:
            if n <= len(words):
                answer_label.config(text=f"答え: {words[n - 1].strip()}")
            else:
                answer_label.config(text="答えが見つかりません")
    except NameError:
        messagebox.showerror("エラー", "最初に問題を読み込んでください")

# 用語と意味を追加するためのウィンドウ
def add_word_meaning():
    def on_submit():
        word = word_entry.get().strip()
        meaning = meaning_entry.get().strip()
        section = section_var.get().strip()
        if word and meaning and section:
            append_to_file(f'{section}_words.txt', word)
            append_to_file(f'{section}_means.txt', meaning)
            add_window.destroy()
            messagebox.showinfo("成功", "用語と意味を追加しました")
        else:
            messagebox.showerror("エラー", "すべてのフィールドに値を入力してください")
        update_sections_menu()

    add_window = tk.Toplevel(root)
    add_window.title("用語と意味を追加")
    add_window.geometry("400x300")
    add_window.config(bg='#f0f0f0')

    frame = ttk.Frame(add_window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="セクション:", font=("Arial", 12)).pack(pady=5)
    section_var = tk.StringVar()
    section_combobox = ttk.Combobox(frame, textvariable=section_var, values=sections, state="readonly", width=47, font=("Arial", 12))
    section_combobox.pack(pady=5)

    ttk.Label(frame, text="用語:", font=("Arial", 12)).pack(pady=5)
    word_entry = ttk.Entry(frame, width=50, font=("Arial", 12))
    word_entry.pack(pady=5)

    ttk.Label(frame, text="意味:", font=("Arial", 12)).pack(pady=5)
    meaning_entry = ttk.Entry(frame, width=50, font=("Arial", 12))
    meaning_entry.pack(pady=5)

    ttk.Button(frame, text="決定", command=on_submit).pack(pady=10, padx=10)

# 指定された行を削除するためのウィンドウ
def delete_word_meaning():
    def on_submit():
        selected_entry = entry_combobox.get().strip()
        if selected_entry:
            selected_index = entry_combobox.current()
            section = section_var.get().strip()
            if section:
                remove_line_from_file(f'{section}_words.txt', selected_index + 1)
                remove_line_from_file(f'{section}_means.txt', selected_index + 1)
                delete_window.destroy()
                messagebox.showinfo("成功", "行を削除しました")
                update_sections_menu()
            else:
                messagebox.showerror("エラー", "セクションを選択してください")
        else:
            messagebox.showerror("エラー", "行を選択してください")

    def update_entry_combobox(event):
        selected_section = section_combobox.get()
        words = read_file_lines(f'{selected_section}_words.txt')
        means = read_file_lines(f'{selected_section}_means.txt')
        combined_entries = [f"{w.strip()} - {m.strip()}" for w, m in zip(words, means)]
        entry_combobox['values'] = combined_entries

    delete_window = tk.Toplevel(root)
    delete_window.title("行を削除")
    delete_window.geometry("400x300")
    delete_window.config(bg='#f0f0f0')

    frame = ttk.Frame(delete_window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="セクション:", font=("Arial", 12)).pack(pady=5)
    section_var = tk.StringVar()
    section_combobox = ttk.Combobox(frame, textvariable=section_var, values=sections, state="readonly", width=47, font=("Arial", 12))
    section_combobox.pack(pady=5)
    section_combobox.bind("<<ComboboxSelected>>", update_entry_combobox)

    ttk.Label(frame, text="行を選択:", font=("Arial", 12)).pack(pady=5)
    entry_combobox = ttk.Combobox(frame, state="readonly", width=47, font=("Arial", 12))
    entry_combobox.pack(pady=10)

    ttk.Button(frame, text="決定", command=on_submit).pack(pady=10, padx=10)

# セクションを作成する関数
def create_section():
    def on_submit():
        section_name = section_entry.get().strip()
        if section_name:
            if section_name not in sections:
                sections.append(section_name)
                update_sections_menu()
                create_window.destroy()
                messagebox.showinfo("成功", "セクションを作成しました")
            else:
                messagebox.showerror("エラー", "そのセクションは既に存在します")
        else:
            messagebox.showerror("エラー", "セクション名を入力してください")

    create_window = tk.Toplevel(root)
    create_window.title("セクションを作成")
    create_window.geometry("400x200")
    create_window.config(bg='#f0f0f0')

    frame = ttk.Frame(create_window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="セクション名:", font=("Arial", 12)).pack(pady=5)
    section_entry = ttk.Entry(frame, width=50, font=("Arial", 12))
    section_entry.pack(pady=10)

    ttk.Button(frame, text="決定", command=on_submit).pack(pady=10, padx=10)

# セクションを削除する関数
def delete_section():
    def on_submit():
        section_name = section_var.get().strip()
        if section_name in sections:
            sections.remove(section_name)
            if os.path.exists(f"{section_name}_words.txt"):
                os.remove(f"{section_name}_words.txt")
            if os.path.exists(f"{section_name}_means.txt"):
                os.remove(f"{section_name}_means.txt")
            delete_window.destroy()
            messagebox.showinfo("成功", "セクションを削除しました")
            update_sections_menu()
        else:
            messagebox.showerror("エラー", "そのセクションは存在しません")

    delete_window = tk.Toplevel(root)
    delete_window.title("セクションを削除")
    delete_window.geometry("400x200")
    delete_window.config(bg='#f0f0f0')

    frame = ttk.Frame(delete_window, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="セクション:", font=("Arial", 12)).pack(pady=5)
    section_var = tk.StringVar()
    section_combobox = ttk.Combobox(frame, textvariable=section_var, values=sections, state="readonly", width=47, font=("Arial", 12))
    section_combobox.pack(pady=10)

    ttk.Button(frame, text="決定", command=on_submit).pack(pady=10, padx=10)

# セクションメニューの更新
def update_sections_menu():
    global sections_menu
    sections_menu.delete(0, tk.END)
    for section in sections:
        sections_menu.add_radiobutton(label=section, variable=current_section, value=section)
    section_combobox['values'] = sections

# モードを切り替える関数
def toggle_mode():
    if mode.get() == "word_to_meaning":
        mode.set("meaning_to_word")
    else:
        mode.set("word_to_meaning")
    load_question()  # モード変更後に新しい問題を読み込む

# メニューバーの設定
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="ファイル", menu=file_menu)
file_menu.add_command(label="追加", command=add_word_meaning)
file_menu.add_command(label="削除", command=delete_word_meaning)

sections_menu = tk.Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="セクション選択", menu=sections_menu)

option_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="セクション", menu=option_menu)
option_menu.add_command(label="セクション作成", command=create_section)
option_menu.add_command(label="セクション削除", command=delete_section)

# モード切り替えスイッチの追加
mode_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="モード", menu=mode_menu)
mode_menu.add_radiobutton(label="単語から意味を推測", variable=mode, value="word_to_meaning", command=load_question)
mode_menu.add_radiobutton(label="意味から単語を推測", variable=mode, value="meaning_to_word", command=load_question)

# カスタムスタイルの定義
style = ttk.Style()
style.configure("TLabel", background="#f8f8f8", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TEntry", font=("Arial", 12), padding=5)

# セクション選択
section_label = ttk.Label(root, text="セクション:", font=("Arial", 12))
section_label.pack(pady=5)
section_combobox = ttk.Combobox(root, textvariable=current_section, values=sections, state="readonly", width=47, font=("Arial", 12))
section_combobox.pack(pady=5)

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

# セクションメニューの更新（section_combobox定義後に実行）
update_sections_menu()

# 初めての問題を読み込む
load_question()

# メインループ
root.mainloop()
