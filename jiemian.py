import tkinter
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os
import tkinter.messagebox

def drop(event):
       
        file_path = event.data.strip()
        file_path = file_path.strip("{}")  # 处理 Windows 路径
        
        entry_sv.set(file_path)
        print(f"拖入的文件路径: {file_path}")

def start_processing():
        file_path = entry_sv.get().strip()  # 获取文件路径
        if os.path.isfile(file_path):
            # 使用 Anaconda 环境中的 Python 解释器
            anaconda_python = r"D:\anaconda\envs\data\python.exe"  # 替换为您的 Anaconda 环境路径
            try:
                subprocess.run([anaconda_python, "d:/ZJDATA/5g/main.py"], check=True)
            except subprocess.CalledProcessError as e:
                tkinter.messagebox.showerror("错误", f"脚本运行失败: {str(e)}")
            except FileNotFoundError:
                tkinter.messagebox.showerror("错误", "Python 解释器未找到，请确认路径。")
        else:
            tkinter.messagebox.showerror("错误", "文件路径无效，请确认路径。")

if __name__ == '__main__':
    root = TkinterDnD.Tk()
    root.title("5g容量处理")
    root.geometry("700x360")


    label = tkinter.Label(root, text="请将文件拖入此处")
    label.pack()

    entry_sv = tkinter.StringVar()
    entry = tkinter.Entry(root, textvariable=entry_sv, width=80)
    entry.pack()

    entry.drop_target_register(DND_FILES)
    entry.dnd_bind('<<Drop>>', drop)

    button = tkinter.Button(root, text="开始处理", command=start_processing)
    button.pack(pady=20, anchor="center")

    root.mainloop()

