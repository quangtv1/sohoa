###############################################################################################
# CÁCH CHẠY: $ python3 1.find-muc-luc-2.py /mnt/g/Shared drives/TTCNTT/Job CNTT/2023-02_Hoa Binh/1. SCAN ALL/HoaBinh/QuynhLam/1.GCN
# KẾT QUẢ: là file exel cột 1 tên file pdf, cột 2 là vị trí của trang chứa ký tự tìm kiếm, cột 3 tổng số trang của file

import os
import PyPDF4
import pandas as pd
import argparse
import glob

# parser = argparse.ArgumentParser(description='Search for a phrase in all PDF files in a directory')
# parser.add_argument('directory', type=str, help='the directory containing the PDF files')
# args = parser.parse_args()
# directory = args.directory

directory = '/mnt/c/Users/admin/Desktop/script/MucLuc/ChamMat'

search_phrase = "MUC"
results = []
pdf_count = 0

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        pdf_count += 1
print("Number of PDF files in directory:", pdf_count)

pdf_thu = 0

for filename in os.listdir(directory):

    if filename.endswith(".pdf"):

        pdf_thu += 1

        with open(os.path.join(directory, filename), 'rb') as pdf_file:

            pdf_reader = PyPDF4.PdfFileReader(pdf_file)
            total_pages = pdf_reader.getNumPages()

            page_numbers = []

            for page_number in range(total_pages):

                page = pdf_reader.getPage(page_number)
                text = page.extractText()

                if search_phrase in text:
                    page_numbers.append(page_number + 1)

                    print(str(pdf_thu)+'/'+str(pdf_count), filename, str(page_number+1)+'/'+str(total_pages))  

                    results.append({'Pdf thứ': str(pdf_thu) + '/' + str(pdf_count), 'File Pdf': filename, 'First': page_number+1, 'Tổng số trang': total_pages})
            
            df = pd.DataFrame(results)

            with pd.ExcelWriter('MucLuc/ChamMat/CM.CDCL.8.xlsx') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)


