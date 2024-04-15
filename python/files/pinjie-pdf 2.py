# -*- coding: utf-8 
import os
import sys
from PyPDF2 import PdfFileMerger

sys.setrecursionlimit(6000)
# 循环path中的文件，可import os 然后用 for img in os.listdir(img_path)实现
# 这里为了让文件以1，2，3的形式进行拼接，就偷懒循环文件名中的数字。

# 将文件放到需要拼接的目录下面
D_dir = "./"
BitStart = 0
BitEnd = -4

dirs = os.listdir(D_dir)
for d in dirs:

    # 检测到脚本则跳过
    if d.startswith('pinjie'):
        continue

    if d.startswith('.'):
        continue

    if d.endswith('.pdf'):
        continue

    d = D_dir + d
    
    if d != "":
        print(d)
        pdf_path = d
        files = os.listdir(pdf_path)
        for l in files:
            if l == ".DS_Store":
                files.remove(".DS_Store")

        files.sort(key=lambda x:int(x[BitStart:BitEnd]))
        pdfdoc = PdfFileMerger()
        print(files)
        for pdf in files:
            if pdf.startswith('.'):
                continue

            print(pdf)
            pdf_file = pdf_path + '/' + pdf  
            pdfbytes = pdfdoc.append(pdf_file)
        pdfdoc.write(pdf_path+'.pdf')
