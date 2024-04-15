# -*- coding: utf-8 
import os
import sys
from PyPDF2 import PdfFileMerger

sys.setrecursionlimit(6000)
# 循环path中的文件，可import os 然后用 for img in os.listdir(img_path)实现
# 这里为了让文件以1，2，3的形式进行拼接，就偷懒循环文件名中的数字。

# 将文件放到需要拼接的目录下面
D_dir = "./"
BitStart = -7
BitEnd = -4
#BitStart = -10
#BitEnd = -7
NewList= []
Tital = ""

files = os.listdir(D_dir)

for l in files:
    print(l)
    if l.startswith('.'):
        continue
    if l.startswith('pinjie'):
        continue
    if l.startswith(Tital):
        NewList.append(l)  

NewList.sort(key=lambda x:int(x[BitStart:BitEnd]))
pdfdoc = PdfFileMerger()
print(NewList)
for pdf in NewList:
    print(pdf)
    pdf_file = D_dir + pdf  
    pdfbytes = pdfdoc.append(pdf_file)
pdfdoc.write('../../' + Tital + '.pdf')
