import os, shutil
import zipfile
import tkinter as tk
from tkinter import filedialog
from opencc import OpenCC

root = tk.Tk()
root.withdraw()

# 获取桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

# 获取当前文件夹路径
now_path = os.getcwd()

# 选择文件
file = filedialog.askopenfilename(
    title = '选择Epub文件',
    filetype = [('Epub电子书', '*.epub')],
    initialdir = desktop_path
    )

# Epub解压文件夹
foldername = os.path.basename(file)

# 解压Epub到同名文件夹
unzipf = zipfile.ZipFile(file, 'r')
unzipf.extractall(foldername)
unzipf.close()

# 遍历解压的Epub文件夹里的所有文件
def get_zip_file(input_path, result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)

filelist = []
get_zip_file(foldername, filelist)

# OpenCC处理文件
convert_list = []
for path in filelist:
    suffix = os.path.splitext(path)[1]
    text_suffix_list = ['.opf', '.ncx', '.xhtml']
    for i in text_suffix_list:
        if(i == suffix):
            convert_list.append(path)

# opencc t2s
cc = OpenCC('t2s')

for path in convert_list:
    cmd = 'python -m opencc -c t2s -i ' + path + ' -o ' + path
    os.system(cmd)

s_foldername = cc.convert(foldername)

# 压缩文件夹为Epub
zipf = zipfile.ZipFile(now_path + '/' + s_foldername, 'w', zipfile.ZIP_DEFLATED)

for file in filelist:
    zipf.write(file)

zipf.close()

shutil.rmtree(foldername)