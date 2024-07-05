# -*- coding: utf-8
import fitz  
import os

# 循环path中的文件，可import os 然后用 for img in os.listdir(img_path)实现
# 这里为了让文件以1，2，3的形式进行拼接，就偷懒循环文件名中的数字。

# 将文件放到需要拼接的目录下面
D_dir = "./"
BitStart = 5
BitEnd = -4

dirs = os.listdir(D_dir)
for d in dirs:

    # 检测到脚本则跳过
    if d.startswith('pinjie'):
        continue

    if d.startswith('.'):
        continue

    d = D_dir + d
    
    if d != "":
        print(d)
        doc = fitz.open()
        img_path = d
        files = os.listdir(img_path)
        files.sort(key=lambda x:int(x[BitStart:BitEnd]))
        print(files)
        for img in files:
            print(img)
            img_file = img_path + '/' + img
            imgdoc = fitz.open(img_file)
            pdfbytes = imgdoc.convertToPDF()
            pdf_name = str(img) + '.pdf'
            imgpdf = fitz.open(pdf_name, pdfbytes)
            doc.insertPDF(imgpdf)
        doc.save(img_path+'.pdf')
        doc.close()
