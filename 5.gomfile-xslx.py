import os
import pandas as pd

# Thư mục chứa các file .xlsx
folder_path = '/mnt/d/HoaBinh/6. MongHoa/MongHoa/MongHoa-Exel'

# Đường dẫn tới thư mục lưu file ChamMat.xlsx
output_folder = '/mnt/d/HoaBinh/6. MongHoa/MongHoa'

# Tạo một đối tượng ExcelWriter để ghi các sheet vào file ChamMat.xlsx
writer = pd.ExcelWriter(os.path.join(output_folder, 'MongHoa-Cuoi.xlsx'), engine='xlsxwriter')

# Duyệt qua từng file và đọc nội dung của từng sheet
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        # Đọc file Excel
        file_path = os.path.join(folder_path, file_name)
        excel_data = pd.read_excel(file_path, sheet_name=None)
        # Ghi các sheet vào file ChamMat.xlsx
        for sheet_name, sheet_data in excel_data.items():
            # Đặt tên sheet là tên của file Excel
            sheet_name = os.path.splitext(file_name)[0]
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
            print("Dang xu ly file: ",sheet_name)

# Lưu và đóng file ExcelWriter
writer.save()
print("Da luu file exel gom vao thu muc: ",output_folder)
