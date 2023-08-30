import os
import PyPDF4
import openpyxl
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import fitz

# Download trên Console
credentials_path = '/mnt/c/Users/TTCNTT/Desktop/script/tnmt-hoabinh-be030cc0dce7.json'

# Thư mục lưu file pdf cần check và share cho user "tnmt-hoabinh@tnmt-hoabinh.iam.gserviceaccount.com"
#folder_path = '/mnt/g/Shared drives/TNMT_HoaBinh3/3.BAN_GIAO/11.YEN_MONG/6.TK/HOP1/YM.TK_001.07.05.H28_2010.1/'
folder_path = '/mnt/g/Shared drives/SCAN/CongThuong-HoaBinh/LOC SCAN- da tach/Lan 3/'

# Link file google sheet cần ghi dữ liệu, 
#url_gsheet = "https://docs.google.com/spreadsheets/d/18mQW7um-CEZFq_s6G7vuTt8odI5lkx6w5mbUU0e7lso/"
url_gsheet = "https://docs.google.com/spreadsheets/d/1tGh-0NocWMB0Elhv7B0Urte3zSh6FLgqTeXGt9rIQSw"
sheet_name = "lan3"

def check_blank_pages(pdf_file):
    blank_pages = 0
    total_pages = 0
    blank_page_positions = []

    with fitz.open(pdf_file) as doc:
        total_pages = doc.page_count

        for page_num in range(total_pages):
            page = doc.load_page(page_num)

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
                print(f"{pdf_file}, đọc trang: {page_num+1}/{total_pages} ==> page {page_num+1} (là trang trắng)")
                blank_page_positions.append(str(page_num + 1))

            else:
                print(f"{pdf_file}, đọc trang: {page_num+1}/{total_pages}")

    blank_page_positions_str = ', '.join(blank_page_positions)
    return blank_pages, total_pages, blank_page_positions_str

def insert_data_to_google_sheet(data):
    global url_gsheet, sheet_name, credentials_path

    # Khởi tạo kết nối đến Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(credentials)


    # Mở sheet, nếu không tồn tại thì thêm sheet mới
    try:
        gsheet = gc.open_by_url(url_gsheet)
        wsheet = gsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        # Tạo sheet mới nếu không tồn tại
        wsheet = gsheet.add_worksheet(title=sheet_name, rows=1, cols=1)


    # Kiểm tra nếu sheet không có dữ liệu
    if wsheet.row_count == 0:
        wsheet.append_row(data)
    else:
        # Chèn dữ liệu vào dòng cuối cùng của sheet
        wsheet.append_row(data, value_input_option='USER_ENTERED')



try:
    # Duyệt thư mục và lấy danh sách file pdf vào mảng
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, f))

    # Sắp xếp mảng pdf_files theo thứ tự tăng dần của tên file
    pdf_files.sort()
    
    # Kiểm tra nếu có file PDF để xử lý    
    if len(pdf_files) > 0:
        # Tạo danh sách để chứa dữ liệu để ghi vào Google Sheet
        data = []
        file_count = 0
        total_blank_pages = 0
        total_pages = 0

        # Ghi Header vào Google Sheet
        # insert_data_to_google_sheet(['Tên file','Danh sách Blank','Tổng số trang','Số trang trắng','Tỉ lệ'])

        header = ['Tên file','Danh sách Blank','Tổng số trang','Số trang trắng','Tỉ lệ']
        insert_data_to_google_sheet(header)

        # Duyệt qua từng file PDF
        for pdf_file in pdf_files:
            try:
                pdf_folder = os.path.dirname(pdf_file)
                pdf_folder_name = os.path.basename(pdf_folder)
                print(f"Bắt đầu kiểm tra file: {pdf_folder_name}/{os.path.basename(pdf_file)}")

                # Kiểm tra trang trắng và lấy thông tin
                blank_pages, num_pages, blank_page_positions_str = check_blank_pages(pdf_file)

                file_count += 1
                total_blank_pages += blank_pages
                total_pages += num_pages

                # Tạo dữ liệu cho mỗi file PDF
                row_data = [pdf_folder + "/" + os.path.basename(pdf_file), blank_page_positions_str, num_pages, blank_pages, f"{(blank_pages/num_pages) * 100:.2f}%"]
                #data.append(row_data)

                # Ghi dữ liệu vào Google Sheet
                if len(row_data) > 0:
                    insert_data_to_google_sheet(row_data)
                    # print(row_data)
                    # print("")
                else:
                    print("Không có dữ liệu để ghi vào Google Sheet.")

                row_data = ''

                # Ghi dữ ra log thông tin
                if total_pages != 0:
                    if blank_page_positions_str != '':
                        print(f"File: {pdf_folder_name}/{os.path.basename(pdf_file)} => có danh sách trang trắng: {blank_page_positions_str}")
                    else:
                        print(f"File: {pdf_folder_name}/{os.path.basename(pdf_file)} => không có trang trắng.")
                print("------------------------------------------------------------------")

            except PyPDF4.utils.PdfReadError:
                print(f"Không thể đọc file {os.path.basename(pdf_file)}")
                continue


        print()
        print("##################################################################")

        if total_pages != 0:
            percentage = total_blank_pages / total_pages
            print(f"Tổng số trang trắng của thư mục: {total_blank_pages}/{total_pages} ({percentage:.2%})")
        else:
            print("Không có trang trắng trong tệp PDF.")

        print(f"Kết quả đã được ghi vào Google Sheet: {url_gsheet}")
        print("##################################################################")

    else:
        print("Không tìm thấy tệp PDF trong thư mục.")

except Exception as e:
    print(f"Có lỗi xảy ra trong quá trình xử lý: {e}")
