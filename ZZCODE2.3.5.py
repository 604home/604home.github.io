import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from tkinter.ttk import *

class ViewSettingsWindow:
    def __init__(self, master, text_area):
        self.master = master
        self.text_area = text_area
        self.window = tk.Toplevel(master)
        self.window.title("视图设置")
        self.window.geometry("300x400")
        self.window.configure(bg="black")

        # 背景颜色选项
        self.bg_frame = tk.Frame(self.window, bg="black")
        self.bg_frame.pack(pady=10)
        self.bg_label = tk.Label(self.bg_frame, text="背景颜色", bg="black", fg="white")
        self.bg_label.pack(side=tk.LEFT, padx=10)
        self.bg_black_button = tk.Button(self.bg_frame, text="黑色", command=lambda: self.change_background_color("black"))
        self.bg_black_button.pack(side=tk.LEFT, padx=5)
        self.bg_white_button = tk.Button(self.bg_frame, text="白色", command=lambda: self.change_background_color("white"))
        self.bg_white_button.pack(side=tk.LEFT, padx=5)
        self.bg_gray_button = tk.Button(self.bg_frame, text="灰色", command=lambda: self.change_background_color("gray"))
        self.bg_gray_button.pack(side=tk.LEFT, padx=5)
        self.bg_yellow_button = tk.Button(self.bg_frame, text="暖黄色", command=lambda: self.change_background_color("#dcdc8b"))
        self.bg_yellow_button.pack(side=tk.LEFT, padx=5)

        # 前景色选项
        self.fg_frame = tk.Frame(self.window, bg="black")
        self.fg_frame.pack(pady=10)
        self.fg_label = tk.Label(self.fg_frame, text="前景颜色", bg="black", fg="white")
        self.fg_label.pack(side=tk.LEFT, padx=10)
        self.fg_green_button = tk.Button(self.fg_frame, text="绿色", command=lambda: self.change_foreground_color("#30ff1d"))
        self.fg_green_button.pack(side=tk.LEFT, padx=5)
        self.fg_red_button = tk.Button(self.fg_frame, text="红色", command=lambda: self.change_foreground_color("red"))
        self.fg_red_button.pack(side=tk.LEFT, padx=5)
        self.fg_blue_button = tk.Button(self.fg_frame, text="蓝色", command=lambda: self.change_foreground_color("blue"))
        self.fg_blue_button.pack(side=tk.LEFT, padx=5)
        self.fg_black_button = tk.Button(self.fg_frame, text="黑色", command=lambda: self.change_foreground_color("black"))
        self.fg_black_button.pack(side=tk.LEFT, padx=5)

        # 字号选项
        self.font_size_frame = tk.Frame(self.window, bg="black")
        self.font_size_frame.pack(pady=10)
        self.font_size_label = tk.Label(self.font_size_frame, text="字号", bg="black", fg="white")
        self.font_size_label.pack(side=tk.LEFT, padx=10)
        self.font_size_8_button = tk.Button(self.font_size_frame, text="8", command=lambda: self.change_font_size(8))
        self.font_size_8_button.pack(side=tk.LEFT, padx=5)
        self.font_size_9_button = tk.Button(self.font_size_frame, text="9", command=lambda: self.change_font_size(9))
        self.font_size_9_button.pack(side=tk.LEFT, padx=5)
        self.font_size_10_button = tk.Button(self.font_size_frame, text="10", command=lambda: self.change_font_size(10))
        self.font_size_10_button.pack(side=tk.LEFT, padx=5)
        self.font_size_11_button = tk.Button(self.font_size_frame, text="11", command=lambda: self.change_font_size(11))
        self.font_size_11_button.pack(side=tk.LEFT, padx=5)
        self.font_size_12_button = tk.Button(self.font_size_frame, text="12", command=lambda: self.change_font_size(12))
        self.font_size_12_button.pack(side=tk.LEFT, padx=5)
        self.font_size_14_button = tk.Button(self.font_size_frame, text="14", command=lambda: self.change_font_size(14))
        self.font_size_14_button.pack(side=tk.LEFT, padx=5)
        self.font_size_16_button = tk.Button(self.font_size_frame, text="16", command=lambda: self.change_font_size(16))
        self.font_size_16_button.pack(side=tk.LEFT, padx=5)

        # 透明度滑块
        self.transparency_slider = tk.Scale(self.window, from_=0.1, to=1.0, resolution=0.1, orient=tk.VERTICAL, command=self.change_transparency)
        self.transparency_slider.set(1.0)
        self.transparency_slider.pack(side=tk.RIGHT, fill=tk.Y)

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
        self.view_settings_window = ViewSettingsWindow(self.master, self.text_area)

    def __init__(self, master):
        self.master = master
        master.title("ZZ Code (V2.3.5)")
        master.configure(bg="black")
        master.iconbitmap(os.path.join('ZZCODE', 'CODE.ico'))
        
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        self.h_scrollbar = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
        self.text_area = tk.Text(master, wrap=tk.NONE, xscrollcommand=self.h_scrollbar.set)
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

        # 视图菜单
        self.view_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="视图", menu=self.view_menu)
        self.view_menu.add_command(label="打开视图设置", command=self.open_view_settings_window)

        # 右键菜单
        self.right_click_menu = tk.Menu(self.text_area, tearoff=False)
        self.right_click_menu.add_command(label="保存", command=self.save_file)
        self.right_click_menu.add_command(label="保存并运行", command=self.save_and_run)
        self.text_area.bind("<Button-3>", self.show_right_click_menu)

        self.file_path = None

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

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleCodeEditor(root)
    root.mainloop()