
#!/bin/bash

# Đường dẫn của thư mục chứa các file PDF
source_dir="/mnt/f/Nam 2022/02. Phường Tân Hòa_signed/"

# Đường dẫn của thư mục đích
destination_dir="/mnt/d/o kho/Nam 2022/"

# Biến đếm số lượng file đã được copy
count=0

# Kích hoạt chế độ thoát khi gặp lỗi
set -e

# Tạo thư mục đích nếu chưa tồn tại
mkdir -p "$destination_dir"

# Tìm và sao chép các file PDF có ký tự "signed"
find "$source_dir" -type f -iname "*.pdf" -name "*signed*" -exec rsync -R {} "$destination_dir" \; -exec echo "Đã sao chép {} đến $destination_dir/{}" \;

# Đếm số lượng file đã được copy
count=$(find "$destination_dir" -type f -iname "*.pdf" -name "*signed*" | wc -l)

echo "Đã sao chép $count file."

