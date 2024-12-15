import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from tkinter.ttk import *

class SimpleCodeEditor:
    """
    一个简单的代码编辑器,支持打开、保存和运行Python脚本。
    """
    def back(self):
        res = messagebox.askyesno('提示', '确定要退出吗？')
        if res:
            self.master.destroy()
        else:
            return

    def __init__(self, master):
        self.master = master
        master.title("ZZ Code (V2.0)")
        master.configure(bg="black")
        master.iconbitmap('ZZCODE\\CODE.ico')
        self.text_area = tk.Text(master)
        self.text_area.config(bg="black", fg="#30ff1d", insertbackground='#ef0000', font=("Consolas", 9))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="打开", command=self.open_file)
        self.file_menu.add_command(label="保存", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="运行", command=self.run_code)
        self.file_menu.add_separator()
        self.file_path = None

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
            except IOError as e:
                messagebox.showerror('错误', f"无法打开文件：{e}")
            except UnicodeDecodeError as e:
                messagebox.showerror('错误', f"文件编码错误：{e}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file_content = self.text_area.get(1.0, tk.END)
                    file.write(file_content)
            except IOError as e:
                messagebox.showerror('错误', f"无法保存文件：{e}")
        else:
            default_ext = '.py'
            file_path = filedialog.asksaveasfilename(defaultextension=default_ext)
            if file_path:
                if os.path.splitext(file_path)[1] != '.py':
                    file_path += '.py'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.file_path = file_path

    def run_code(self):
        if self.file_path and self.file_path.endswith('.py'):
            try:
                subprocess.run(['python', self.file_path])
            except FileNotFoundError:
                messagebox.showerror('错误', "Python解释器未找到,请确保已安装Python环境。")
            except Exception as e:
                messagebox.showerror('错误', f"运行代码出错：{e}")
        else:
            messagebox.showinfo('提示', "请先保存Python(.py后缀名)脚本文件。")

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleCodeEditor(root)
    root.mainloop()
