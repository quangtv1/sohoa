import os
from pdfrw import PdfWriter, PdfReader

def merge_pdfs_in_directory(directory):
    writer = PdfWriter()
    pdf_files = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath) and filename.lower().endswith('.pdf'):
            pdf_files.append(filepath)

    if pdf_files:
        pdf_files = sorted(pdf_files, key=lambda x: x.count('.'))

        for filepath in pdf_files:
            try:
                reader = PdfReader(filepath)
                writer.addpages(reader.pages)
            except Exception as e:
                print(f"Lỗi khi đọc file {filepath}: {str(e)}")
                continue

        first_file_name = os.path.splitext(os.path.basename(pdf_files[0]))[0]
        new_filename = first_file_name + '._all.pdf'

        merged_filepath = os.path.join(directory, new_filename)
        writer.write(merged_filepath)

        print('Đã tạo thành công tệp PDF gộp tại:', merged_filepath)

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            merge_pdfs_in_directory(subdir_path)

root_directory = '/mnt/e/DongTien-Gop/DongTien-2022-link'
merge_pdfs_in_directory(root_directory)
