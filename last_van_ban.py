import os
import pandas as pd
import re

def count_and_extract_numbers(directory):
    result = []
    for root, _, files in os.walk(directory):
        pdf_files = [file for file in files if file.lower().endswith('.pdf')]
        folder_name = os.path.basename(root)
        pdf_count = len(pdf_files)
        
        max_number = 0
        for file in pdf_files:
            match = re.search(r'(\d+)\.pdf$', file)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)
        
        result.append((folder_name, pdf_count, max_number + 1))
    
    return result

def write_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=['Folder', 'PDF Count', 'Max Number + 1'])
    df.to_excel(output_file, index=False)

# Đường dẫn thư mục bạn muốn đếm file PDF và trích xuất số
directory_path = '/mnt/d/03. Phường Đồng Tiến/DongTien_VanBan'

# Tên file Excel đầu ra
output_file = 'last_van_ban_.xlsx'

# Đếm số lượng file PDF và trích xuất số, sau đó ghi vào file Excel
result = count_and_extract_numbers(directory_path)
write_to_excel(result, output_file)

print('Đã ghi kết quả vào file Excel:', output_file)
