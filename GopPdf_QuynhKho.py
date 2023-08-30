import os
from pdfrw import PdfWriter, PdfReader

def merge_pdfs_in_directory(directory):
    writer = PdfWriter()
    bia_files = []
    mltl_files = []
    other_files = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath) and filename.lower().endswith('.pdf'):
            if 'BIA' in filename:
                bia_files.append(filepath)
            elif 'MLTL' in filename:
                mltl_files.append(filepath)
            else:
                other_files.append(filepath)

    bia_files = sorted(bia_files, key=lambda x: os.path.basename(x))
    mltl_files = sorted(mltl_files, key=lambda x: os.path.basename(x))
    other_files = sorted(other_files, key=lambda x: os.path.basename(x))

    pdf_files = bia_files + mltl_files + other_files

    if pdf_files:
        for filepath in pdf_files:
            reader = PdfReader(filepath)
            writer.addpages(reader.pages)

        #first_file_name = os.path.splitext(os.path.basename(pdf_files[0]))[0]
        #new_merged_filename = first_file_name[:-4] + '.pdf'

        parent_directory = os.path.basename(directory)
        new_merged_filename = parent_directory + '._all.pdf'

        merged_filepath = os.path.join(directory, new_merged_filename)
        writer.write(merged_filepath)

        print('Đã tạo thành công tệp PDF gộp tại:', merged_filepath)

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            merge_pdfs_in_directory(subdir_path)

root_directory = '/mnt/c/Users/Thinkpad/Desktop/CN-lan2'
merge_pdfs_in_directory(root_directory)
