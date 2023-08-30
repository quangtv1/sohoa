import os
import datetime
from PyPDF4 import PdfFileWriter, PdfFileReader

# Đường dẫn đến thư mục cha chứa tất cả các thư mục con cần xử lý

#root_dir = '/mnt/d/6. MongHoa/MongHoa/1.CGCN/'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/10.TTTH/'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/2.CGCNLN/'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/7.CMD/'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/8.TC/'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/3.CDCL'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/9.TK'
#root_dir = '/mnt/d/6. MongHoa/MongHoa/6.BD'
#root_dir = '/mnt/d/HoaBinh/6. MongHoa/MongHoa/5.CN'
#root_dir = '/mnt/d/HoaBinh/7. DanHoa/TACH'
#root_dir = '/mnt/d/HoaBinh/8. YenQuang/TACH'
#root_dir = '/mnt/d/HoaBinh/9. Hoa Binh/TACH'
#root_dir = '/mnt/d/HoaBinh/6. MongHoa/TACH'
#root_dir = '/mnt/g/Shared drives/TTCNTT/Job CNTT/2023-02_Hoa Binh/1. SCAN ALL/TACH/5. ChamMat_Huce'
#root_dir = '/mnt/d/HoaBinh/5.ChamMat/TACH'
#root_dir = '/mnt/d/HoaBinh/10. HopThanh/TACH'
#root_dir = '/mnt/d/HoaBinh/11. YenMong/TACH'
#root_dir = '/mnt/d/HoaBinh/1.TanThinh/TACH/4.BD-k67'
root_dir = '/mnt/c/Users/Thinkpad/Desktop/CN-lan2/test'


# Tạo thư mục FIRST_PDF để lưu trữ các file pdf đầu tiên đã được tách
first_pdf_dir = os.path.join(root_dir, 'FIRST_PDF')
if not os.path.exists(first_pdf_dir):
    os.makedirs(first_pdf_dir)

# Duyệt qua tất cả các thư mục con và tách trang đầu tiên của các file pdf trong thư mục cha
for root, dirs, files in os.walk(root_dir):
    if root == first_pdf_dir:
        continue
    for file in files:
        if file.endswith('.pdf'):
            file_path = os.path.join(root, file)
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'xử lý file: ', file_path )

            # Đọc file pdf vào đối tượng PdfFileReader
            with open(file_path, 'rb') as f:
                pdf_reader = PdfFileReader(f)
                page = pdf_reader.getPage(0)

                # Tạo đối tượng PdfFileWriter để ghi trang đã tách ra
                output_pdf = PdfFileWriter()
                output_pdf.addPage(page)

                # Lưu trang đã tách ra thành một file pdf mới
                output_file_path = os.path.join(first_pdf_dir, os.path.splitext(file)[0] + '_first.pdf')
                with open(output_file_path, 'wb') as out_f:
                    output_pdf.write(out_f)