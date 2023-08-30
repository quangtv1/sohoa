import openpyxl
import fitz
import os

def delete_blank_pages(xlsx_file):
    wb = openpyxl.load_workbook(xlsx_file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        pdf_path = row[0]
        blank_pages = [int(page) for page in row[1].split(',')]

        try:
            doc = fitz.open(pdf_path)

            # Sắp xếp danh sách trang trắng theo thứ tự tăng dần
            blank_pages.sort()

            for page_number in reversed(blank_pages):
                doc.delete_page(page_number - 1)
                print(f"Đã xoá trang: {page_number - 1}")

            temp_path = os.path.splitext(pdf_path)[0] + "_temp.pdf"
            doc.save(temp_path, garbage=4, deflate=True, clean=True)
            doc.close()

            os.replace(temp_path, pdf_path)

            print(f"Đã xoá trang trắng từ {pdf_path}. Kết quả được ghi đè lên tệp {pdf_path}")

        except (fitz.errors.PDFInvalidError, FileNotFoundError) as e:
            print(f"Lỗi khi xử lý tệp {pdf_path}: {str(e)}")

    wb.close()

xlsx_file = "/mnt/c/Users/TTCNTT/Desktop/script/TT.CGCN_2023-03-02.020.xlsx"
delete_blank_pages(xlsx_file)
