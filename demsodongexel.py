import os
import pandas as pd

def count_non_empty_rows(file_path):
    try:
        # Đọc file Excel với header=None để không coi dòng tiêu đề là dữ liệu
        df = pd.read_excel(file_path, header=None)

        # Thay 'A' bằng tên cột A trong file Excel của bạn
        column_name = df.columns[0]

        # Lấy tất cả các giá trị trong cột đầu tiên
        column_a_values = df[column_name].tolist()

        # In dữ liệu thô để kiểm tra
        print(column_a_values)

        # Đếm số dòng không trống trong cột đầu tiên (bao gồm cả dòng tiêu đề)
        count = sum(pd.notna(value) and str(value).strip() != "" for value in column_a_values)

        return count
    except pd.errors.EmptyDataError:
        return 0

def count_non_empty_rows_in_directory(directory_path):
    data = []
    total_rows = 0

    for idx, (root, _, files) in enumerate(os.walk(directory_path)):
        for file in files:
            #if file.endswith('.xlsx'):
            if file.endswith('.xls') or file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                rows = count_non_empty_rows(file_path)
                data.append([idx + 1, file, file_path, rows])
                total_rows += rows
                print(f"File: {file}, Số dòng: {rows}")

    # Tạo DataFrame từ danh sách data
    columns = ['STT', 'Tên file Excel', 'Đường dẫn', 'Số lượng dòng']
    df = pd.DataFrame(data, columns=columns)

    # Ghi DataFrame vào file Excel
    output_file = 'thong_ke_file_excel.xlsx'  # Thay đổi tên file Excel đích nếu cần
    df.to_excel(output_file, index=False)

    # Trả về tổng số dòng có dữ liệu
    return total_rows

# Thay đổi đường dẫn đến thư mục cha của các file Excel của bạn
directory_path = '/mnt/d/Dung So Hoa'
total_rows_with_data = count_non_empty_rows_in_directory(directory_path)
print("Tổng số dòng có dữ liệu trên các file Excel: ", total_rows_with_data)
