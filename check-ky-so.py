import os
from openpyxl import Workbook

def list_pdf_files(folder_path):
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file_name)
                pdf_files.append(pdf_path)
                print("Đang kiểm tra:", pdf_path)
    return pdf_files

def save_to_excel(file_list, excel_path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Địa chỉ file không ký", "Địa chỉ file đã ký"])

    for pdf_path in file_list:
        if "_signed.pdf" in pdf_path:
            ws.append(["", pdf_path])
        else:
            ws.append([pdf_path, ""])

    wb.save(excel_path)
    print("Kết quả đã được lưu vào:", excel_path)

if __name__ == "__main__":
    folder_to_check = "/mnt/e/TNMT_Signed/Tong/"
    excel_file_path = "check-ky-so-2.xlsx"

    pdf_files = list_pdf_files(folder_to_check)
    save_to_excel(pdf_files, excel_file_path)
