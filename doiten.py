import os
import shutil

def rename_pdf_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                old_name = os.path.join(root, file)
                dirname = os.path.dirname(old_name)
                filename = os.path.basename(old_name)
                arr = filename.split('_', 1)
                print(arr)
                if len(arr) == 2:
                    suffix = arr[0]
                    ten = arr[1]

                new_suffix = suffix.replace('_', '')
                new_arr = ten.split('.')
                new_arr.insert(len(new_arr) - 2, new_suffix)

                reslut = '.'.join(new_arr).replace('_', '.').replace('07.05.H28', '06.05.H28')
                new_name = os.path.join(dirname,reslut)
                os.rename(old_name, new_name)
                print(f"Đã đổi tên từ '{old_name}' sang '{new_name}'")

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if "_" in dir_name and "." in dir_name:
                old_path = os.path.join(root, dir_name)
                foldername = os.path.basename(old_path)
                arr_f = foldername.split('_', 1)
                print(arr_f)
                if len(arr_f) == 2:
                    suffix_f = arr_f[0]
                    ten_f = arr_f[1]

                new_suffix_f = suffix_f.replace('_', '')
                new_arr_f = ten_f.split('.')
                new_arr_f.append(new_suffix_f)

                reslutf = '.'.join(new_arr_f).replace('_', '.').replace('07.05.H28', '06.05.H28')
                new_path = os.path.join(root, reslutf)
                shutil.move(old_path, new_path)
                print(f"Đã đổi tên từ '{old_path}' thành '{new_path}'")

# Thay đổi đường dẫn thư mục tại đây
directory = '/mnt/g/Shared drives/3. HoaBinh_TNMT_Link/1. SCAN ALL/HO SO DA TACH/12. Bo sung Tân Thịnh/'

rename_pdf_files(directory)
