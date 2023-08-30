import os

def process_line(line):
    if line.endswith(".pdf"):
        modified_line = line.replace(".pdf", "_signed.pdf")
        return modified_line
    return None

# Thay đổi tên tệp với biến
pdf_list_file = "tong.txt"
output_file_path = "tong-checked.txt"

lines_a_set = set()
lines_b_set = set()

# Thực hiện lệnh bash để tạo danh sách đường dẫn tệp PDF
os.system('find . -iname "*.pdf" > ' + pdf_list_file)

# Đọc tệp và lọc dòng vào tập hợp A hoặc B
with open(pdf_list_file, "r", encoding="utf-8") as file:
    for line in file:
        stripped_line = line.strip()
        if "_signed.pdf" in stripped_line:
            lines_b_set.add(stripped_line)
        else:
            lines_a_set.add(stripped_line)

lines_to_write = []

for line_a in lines_a_set:
    processed_line = process_line(line_a)
    if processed_line and processed_line not in lines_b_set:
        lines_to_write.append(line_a)

# Sắp xếp danh sách trước khi ghi ra tệp
lines_to_write.sort()

with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.writelines('\n'.join(lines_to_write))

# In ra số dòng được ghi vào tệp
print(f"Đã ghi {len(lines_to_write)} dòng vào tệp {output_file_path}")

print("Đã hoàn thành việc kiểm tra và ghi kết quả vào tệp checked.txt")
