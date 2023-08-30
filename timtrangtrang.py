import os
import PyPDF4
import openpyxl
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import fitz

#def check_blank_pages(pdf_file):
#    with open(pdf_file, 'rb') as f:
#        pdf_reader = PyPDF4.PdfFileReader(f)
#        total_pages = pdf_reader.getNumPages()
#        blank_pages = sum([1 for page in pdf_reader.pages if page.extractText().strip() == ''])
#        return blank_pages, total_pages

#def check_blank_pages(pdf_file):
#    blank_pages = 0
#    total_pages = 0

#    with open(pdf_file, 'rb') as f:
#        pdf_reader = PyPDF4.PdfFileReader(f)
#        total_pages = pdf_reader.getNumPages()

#        for page_num in range(total_pages):
#            page = pdf_reader.getPage(page_num)

#            # Convert PDF page to image
#            images = convert_from_path(pdf_file, first_page=page_num+1, last_page=page_num+1)
#            image = images[0]

#            # Convert image to grayscale for OCR
#            image = image.convert('L')

#            # Use Pytesseract to extract text from the image
#            text = pytesseract.image_to_string(image)

#            # Check if the extracted text is blank
#            if not text.strip():
#                blank_pages += 1

#    return blank_pages, total_pages

## Rest of the code remains the same




def check_blank_pages(pdf_file):
    blank_pages = 0
    total_pages = 0
    blank_page_positions = []

    with fitz.open(pdf_file) as doc:
        total_pages = doc.page_count

        for page_num in range(total_pages):

            page = doc.load_page(page_num)

            print(f"Đọc trang: {page_num}")

            # Convert PDF page to image
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Convert image to grayscale for OCR
            img_gray = img.convert('L')

            # Use Pytesseract to extract text from the image
            text = pytesseract.image_to_string(img_gray)

            # Check if the extracted text is blank
            if not text.strip():
                blank_pages += 1
                print(f"Trang {page_num}  ==> Là trang trắng")
                blank_page_positions.append(str(page_num + 1))

    blank_page_positions_str = ', '.join(blank_page_positions)

    return blank_pages, total_pages, blank_page_positions_str


# Rest of the code remains the same



folder_path = '/mnt/g/Shared drives/TNMT_HoaBinh1,2/check_blank'

pdf_files = []
for root, dirs, files in os.walk(folder_path):
    for f in files:
        if f.endswith('.pdf'):
            pdf_files.append(os.path.join(root, f))

data = {
    'Thư mục': [],
    'Tên file': [],
    'Danh sách Blank': [],
    'Tổng số trang': [],
    'Số trang trắng': [],
    'Tỉ lệ': [],

}

file_count = 0
total_blank_pages = 0
total_pages = 0

for pdf_file in pdf_files:
    try:
        blank_pages, num_pages, blank_page_positions_str = check_blank_pages(pdf_file)

        file_count += 1
        total_blank_pages += blank_pages
        total_pages += num_pages

        pdf_folder = os.path.dirname(pdf_file)
        pdf_folder_name = os.path.basename(pdf_folder)

        data['Thư mục'].append(pdf_folder)
        data['Tên file'].append(os.path.basename(pdf_file))
        data['Danh sách Blank'].append(blank_page_positions_str)
        data['Tổng số trang'].append(num_pages)
        data['Số trang trắng'].append(blank_pages)
        data['Tỉ lệ'].append(f"{(blank_pages/num_pages) * 100:.2f}%")  # Chuyển tỉ lệ thành phần trăm

        print(f"Tên file: {pdf_folder_name}/{os.path.basename(pdf_file)} => Blank: {blank_page_positions_str}")

    except PyPDF4.utils.PdfReadError:
        print(f"Không thể đọc file {os.path.basename(pdf_file)}")
        continue

print(f"Tổng số trang trắng: {total_blank_pages}/{total_pages} ({total_blank_pages/total_pages:.2%})")

wb = openpyxl.Workbook()
ws = wb.active

headers = ['Thư mục', 'Tên file', 'Danh sách Blank','Tổng số trang', 'Số trang trắng', 'Tỉ lệ']

ws.append(headers)

for i in range(len(data['Thư mục'])):
    row_data = [data['Thư mục'][i], data['Tên file'][i],data['Danh sách Blank'][i], data['Tổng số trang'][i], data['Số trang trắng'][i], data['Tỉ lệ'][i]]
    ws.append(row_data)

wb.save('DemBlank.xlsx')
print("Kết quả đã được lưu vào file DemBlank.xlsx")
