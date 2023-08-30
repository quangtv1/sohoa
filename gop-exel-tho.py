import os
import os
import pandas as pd
import os
import pandas as pd

def merge_excel_sheets(input_dir, output_file):
    all_data = []
    file_names_temp = []

    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                file_path = os.path.join(root, file_name)
                print("Đang gộp file:", file_path)
                xls = pd.ExcelFile(file_path)
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    all_data.append(df)
                    file_names_temp.append(file_name)

    # Đảm bảo số lượng cột của các DataFrame giống nhau
    max_cols = max(df.shape[1] for df in all_data)
    for df in all_data:
        while df.shape[1] < max_cols:
            new_col_name = 'Column' + str(df.shape[1] + 1)  # Tạo tên cột không trùng lặp
            df.insert(df.shape[1], new_col_name, '')  # Thêm cột trống

    # Xác định số lượng dòng dữ liệu từ từng file Excel và thêm tên file tương ứng vào danh sách `file_names`
    num_rows_per_file = [len(df) for df in all_data]
    total_rows = sum(num_rows_per_file)
    file_names = [file_name for i, num_rows in enumerate(num_rows_per_file) for file_name in [file_names_temp[i]] * num_rows]

    merged_data = pd.concat(all_data, ignore_index=True, axis=0)

    # Kiểm tra xem cột 'File Name' đã tồn tại trong `merged_data` chưa trước khi thêm nó vào
    if 'File Name' not in merged_data.columns:
        merged_data.insert(0, 'File Name', file_names)

    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        merged_data.to_excel(writer, index=False, sheet_name='MergedSheet')

if __name__ == "__main__":
    input_directory = "/mnt/c/Users/Thinkpad/Desktop/script_54/exel"  # Thay đổi đường dẫn tới thư mục của bạn
    output_file_path = "/mnt/c/Users/Thinkpad/Desktop/merged_file.xlsx"  # Thay đổi đường dẫn tới file đầu ra của bạn

    merge_excel_sheets(input_directory, output_file_path)
    print("Sheets have been merged successfully into a single Excel file!")

