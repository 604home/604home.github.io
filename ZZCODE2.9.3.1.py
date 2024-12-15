import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import json
import re

class ViewSettingsWindow:
    def __init__(self, master, text_area, settings_file):
        self.master = master
        self.text_area = text_area
        self.settings_file = settings_file
        self.window = tk.Toplevel(master)
        self.window.title("视图设置")
        self.window.geometry("300x400")
        self.window.configure(bg="black")

        # 检查当前工作目录
        print(f"Current working directory: {os.getcwd()}")

        # 显式指定文件路径
        self.settings_file = os.path.join(os.path.dirname(__file__), "settings.txt")

        # 背景颜色选项
        self.bg_frame = tk.Frame(self.window, bg="black")
        self.bg_frame.pack(pady=10)
        self.bg_label = tk.Label(self.bg_frame, text="背景颜色", bg="black", fg="white")
        self.bg_label.pack(side=tk.LEFT, padx=10)
        self.bg_var = tk.StringVar(value="black")
        self.bg_options = ["black", "white", "gray", "#dcdc8b"]
        self.bg_dropdown = tk.OptionMenu(self.bg_frame, self.bg_var, *self.bg_options, command=self.change_background_color)
        self.bg_dropdown.config(bg="black", fg="white", activebackground="black", activeforeground="white")
        self.bg_dropdown["menu"].config(bg="black", fg="white")
        self.bg_dropdown.pack(side=tk.LEFT, padx=5)

        # 前景色选项
        self.fg_frame = tk.Frame(self.window, bg="black")
        self.fg_frame.pack(pady=10)
        self.fg_label = tk.Label(self.fg_frame, text="前景颜色", bg="black", fg="white")
        self.fg_label.pack(side=tk.LEFT, padx=10)
        self.fg_var = tk.StringVar(value="black")
        self.fg_options = ["#30ff1d", "red", "blue", "black"]
        self.fg_dropdown = tk.OptionMenu(self.fg_frame, self.fg_var, *self.fg_options, command=self.change_foreground_color)
        self.fg_dropdown.config(bg="black", fg="white", activebackground="black", activeforeground="white")
        self.fg_dropdown["menu"].config(bg="black", fg="white")
        self.fg_dropdown.pack(side=tk.LEFT, padx=5)

        # 字号选项
        self.font_size_frame = tk.Frame(self.window, bg="black")
        self.font_size_frame.pack(pady=10)
        self.font_size_label = tk.Label(self.font_size_frame, text="字号", bg="black", fg="white")
        self.font_size_label.pack(side=tk.LEFT, padx=10)
        self.font_size_var = tk.IntVar(value=9)
        self.font_size_options = [8, 9, 10, 11, 12, 14, 16]
        self.font_size_dropdown = tk.OptionMenu(self.font_size_frame, self.font_size_var, *self.font_size_options, command=self.change_font_size)
        self.font_size_dropdown.config(bg="black", fg="white", activebackground="black", activeforeground="white")
        self.font_size_dropdown["menu"].config(bg="black", fg="white")
        self.font_size_dropdown.pack(side=tk.LEFT, padx=5)

        # 透明度滑块
        self.transparency_slider = tk.Scale(self.window, from_=0.1, to=1.0, resolution=0.1, orient=tk.VERTICAL, command=self.change_transparency)
        self.transparency_slider.set(1.0)
        self.transparency_slider.pack(side=tk.RIGHT, fill=tk.Y)

        # 保存按钮
        self.save_button = tk.Button(self.window, text="保存设置", command=self.save_settings)
        self.save_button.pack(pady=10)

        # 加载上次保存的设置
        self.load_settings()

    def change_background_color(self, color):
        self.text_area.config(bg=color)

    def change_foreground_color(self, color):
        self.text_area.config(fg=color)

    def change_font_size(self, size):
        current_font = self.text_area.cget("font")
        font_name, _ = current_font.split()
        self.text_area.config(font=(font_name, int(size)))

    def change_transparency(self, value):
        self.master.attributes('-alpha', float(value))

    def save_settings(self):
        settings = {
            "bg_color": self.bg_var.get(),
            "fg_color": self.fg_var.get(),
            "font_size": self.font_size_var.get(),
            "transparency": self.transparency_slider.get()
        }
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)
        messagebox.showinfo("提示", "设置已保存")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)
                self.bg_var.set(settings.get("bg_color", "black"))
                self.fg_var.set(settings.get("fg_color", "black"))
                self.font_size_var.set(settings.get("font_size", 9))
                self.transparency_slider.set(settings.get("transparency", 1.0))
                self.change_background_color(settings.get("bg_color", "black"))
                self.change_foreground_color(settings.get("fg_color", "black"))
                self.change_font_size(settings.get("font_size", 9))
                self.change_transparency(settings.get("transparency", 1.0))

class RunDialog:
    def __init__(self, master, editor):
        self.editor = editor
        self.master = master
        self.dialog = tk.Toplevel(master)
        self.dialog.title("运行状态")
        self.dialog.geometry("300x100")
        self.dialog.protocol("WM_DELETE_WINDOW", self.stop_run)

        self.label = tk.Label(self.dialog, text="代码正在运行...")
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self.dialog)
        self.button_frame.pack(pady=10)

        self.re_run_button = tk.Button(self.button_frame, text="重新运行", command=self.re_run)
        self.re_run_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="停止运行", command=self.stop_run)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.process = None

    def re_run(self):
        self.stop_run()
        self.editor.run_code()

    def stop_run(self):
        if self.process:
            self.process.terminate()
            self.process = None
        self.dialog.destroy()

class SimpleCodeEditor:
    def back(self):
        if self.is_modified():
            res = messagebox.askyesnocancel('提示', '文件已修改，是否保存？')
            if res is True:
                self.save_file()
                self.master.destroy()
            elif res is False:
                self.master.destroy()
        else:
            self.master.destroy()

    def is_modified(self):
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content != self.text_area.get(1.0, tk.END).strip()
        return True

    def open_view_settings_window(self):
        self.view_settings_window = ViewSettingsWindow(self.master, self.text_area, self.settings_file)

    def __init__(self, master):
        self.master = master
        master.title("ZZ Code (V2.9.3.1)")
        master.configure(bg="black")
        master.iconbitmap(os.path.join('ZZCODE', 'CODE.ico'))
        
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        self.h_scrollbar = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
        self.text_area = tk.Text(master, wrap=tk.NONE, xscrollcommand=self.h_scrollbar.set, undo=True, maxundo=-1, autoseparators=True)
        self.text_area.config(bg="#dcdc8b", fg="black", insertbackground='#ef0000', font=("Consolas", 9))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.h_scrollbar.config(command=self.text_area.xview)
        
        # 文件菜单
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="打开", command=self.open_file)
        self.file_menu.add_command(label="保存", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="运行", command=self.run_code)
        self.file_menu.add_separator()

        # 编辑菜单
        self.edit_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="编辑", menu=self.edit_menu)
        self.edit_menu.add_command(label="撤销", command=self.undo)
        self.edit_menu.add_command(label="重做", command=self.redo)

        # 视图菜单
        self.view_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="视图", menu=self.view_menu)
        self.view_menu.add_command(label="打开视图设置", command=self.open_view_settings_window)

        # 右键菜单
        self.right_click_menu = tk.Menu(self.text_area, tearoff=False)
        self.right_click_menu.add_command(label="保存", command=self.save_file)
        self.right_click_menu.add_command(label="保存并运行", command=self.save_and_run)
        self.right_click_menu.add_command(label="撤销", command=self.undo)
        self.right_click_menu.add_command(label="重做", command=self.redo)
        self.text_area.bind("<Button-3>", self.show_right_click_menu)

        # 快捷键
        master.bind("<F5>", lambda event: self.run_code())
        master.bind("<F6>", lambda event: self.stop_run())
        master.bind("<Control-z>", lambda event: self.undo())
        master.bind("<Control-y>", lambda event: self.redo())

        # 语法高亮
        self.text_area.bind("<KeyRelease>", self.highlight_syntax)

        self.file_path = None
        self.settings_file = "settings.txt"
        self.run_dialog = None

    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass

    def highlight_syntax(self, event=None):
        keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield']
        self.text_area.tag_remove('keyword', '1.0', tk.END)
        for keyword in keywords:
            start = '1.0'
            while True:
                start = self.text_area.search(keyword, start, tk.END, nocase=True)
                if not start:
                    break
                end = f"{start}+{len(keyword)}c"
                self.text_area.tag_add('keyword', start, end)
                start = end
        self.text_area.tag_config('keyword', foreground='blue')

    def show_right_click_menu(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

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

    def save_and_run(self):
        self.save_file()
        self.run_code()

    def run_code(self):
        if self.file_path and self.file_path.endswith('.py'):
            try:
                self.run_dialog = RunDialog(self.master, self)
                self.run_dialog.process = subprocess.Popen(['python', self.file_path])
            except FileNotFoundError:
                messagebox.showerror('错误', "Python解释器未找到,请确保已安装Python环境。")
            except Exception as e:
                messagebox.showerror('错误', f"运行代码出错：{e}")
        else:
            messagebox.showinfo('提示', "请先保存Python(.py后缀名)脚本文件.")

    def stop_run(self):
        if self.run_dialog and self.run_dialog.process:
            self.run_dialog.process.terminate()
            self.run_dialog.process = None
            self.run_dialog.dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleCodeEditor(root)
    root.mainloop()