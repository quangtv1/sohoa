import os
import pandas as pd

# Đường dẫn đến thư mục gốc chứa các file CSV
thu_muc_goc = '/duong/dan/thu/muc/goc'

# Duyệt qua tất cả các thư mục và file trong thư mục gốc
for thu_muc_goc, thu_muc_con, danh_sach_file in os.walk(thu_muc_goc):
    for ten_file in danh_sach_file:
        if ten_file.endswith('.csv'):
            duong_dan_csv = os.path.join(thu_muc_goc, ten_file)
            # Đọc file CSV
            df = pd.read_csv(duong_dan_csv)
            
            # Lưu thành file Excel có cùng tên
            ten_file_excel = os.path.splitext(ten_file)[0] + '.xlsx'
            duong_dan_excel = os.path.join(thu_muc_goc, ten_file_excel)
            df.to_excel(duong_dan_excel, index=False) # index=False để không lưu cột index vào file Excel
            print(f'{ten_file} đã được chuyển thành {ten_file_excel}')
