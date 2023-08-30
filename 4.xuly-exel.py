
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import quote_sheetname

#Thay đổi đường dẫn thư mục thành thư mục chứa các file Excel của bạn
folder_path = '/mnt/c/Users/Thinkpad/Desktop/CN-lan2/test'


# Duyệt qua tất cả các tệp Excel trong thư mục được chỉ định
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):

        # Đọc dữ liệu từ tệp Excel
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path)

        # Thêm cột mới trước cột đầu tiên
        #if "New Column" in df.columns:
        #    del df["New Column"]
        df.insert(0, "New Column", "")

        # Kiểm tra nếu một trong các ô từ cột 2 đến cột 8 có chứa dữ liệu
        for index, row in df.iterrows():
            if row.iloc[0:8].notna().any():
                # Gán giá trị filename cho cột 1 của hàng đó
                df.at[index, "New Column"] = filename

      
        # Ghi dữ liệu vào tệp Excel
        writer = pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace")
        df.to_excel(writer,sheet_name='themten', index=False)
        writer.save()
        print("Đã xử lý file: ", filename)


# Lấy danh sách tất cả các tệp excel trong thư mục
all_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Đọc các tệp excel và ghép chúng thành một tệp duy nhất.
combined_data = pd.DataFrame()
for f in all_files:
    # Đọc tệp Excel và chỉ lấy các sheet có tên là "themten"
    xls = pd.ExcelFile(os.path.join(folder_path, f))
    sheet_names = [name for name in xls.sheet_names if name == "themten"]
    if len(sheet_names) > 0:
        df = pd.concat([pd.read_excel(os.path.join(folder_path, f), sheet_name=name, header=None).dropna(how='all') for name in sheet_names])
        combined_data = combined_data.append(df)

# Lưu dữ liệu được kết hợp vào một tệp mới
combined_data.to_excel(os.path.join(folder_path, 'SoCongThuong.xlsx'), index=False, header=False)
print("Đã gom vào file: SoCongThuong.xlsx")
