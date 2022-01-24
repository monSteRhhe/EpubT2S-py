import os, shutil , _thread, zipfile
from tkinter import *
from tkinter import filedialog
from opencc import OpenCC

def epubt2s():
    root = Tk()
    root.withdraw()

    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

    # 获取当前文件夹路径
    current_path = os.getcwd()

    # 选择文件
    file = filedialog.askopenfilename(
        title = '选择Epub文件',
        filetype = [('Epub电子书', '*.epub')],
        initialdir = desktop_path
        )

    # opencc t2s
    cc = OpenCC('t2s')

    # Epub解压文件夹
    # foldername是epub名，folder是文件夹名
    foldername = os.path.basename(file)
    folder = os.path.splitext(foldername)[0]

    s_foldername = cc.convert(foldername)
    s_folder = cc.convert(folder)

    # 解压Epub到同名文件夹
    unzipf = zipfile.ZipFile(file, 'r')
    unzipf.extractall(s_folder)
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
    get_zip_file(s_folder, filelist)

    # OpenCC处理文件
    convert_list = []
    for path in filelist:
        suffix = os.path.splitext(path)[1]
        text_suffix_list = ['.opf', '.ncx', '.xhtml']
        for i in text_suffix_list:
            if(i == suffix):
                convert_list.append(path)

    for path in convert_list:
        CCcmd = 'python -m opencc -c t2s -i ' + path + ' -o ' + path
        os.system(CCcmd)

    # 打包文件夹为Epub
    def zipDir(dirpath,outFullName):
        zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
        for path,dirnames,filenames in os.walk(dirpath):
            # 去掉目标根路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath,'')

            for filename in filenames:
                zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
        zip.close()

    zipDir(s_folder, current_path + '/' + s_foldername)


    shutil.rmtree(s_folder)

_thread.start_new_thread(epubt2s, ())

input()