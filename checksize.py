import PyPDF4


with open('/mnt/g/Shared drives/TTCNTT/Job CNTT/2023-02_Hoa Binh/1. SCAN ALL/TACH/DanChu/6.CMD/HOP1/DC.CMD_001.07.05.H28_2015.28.pdf', 'rb') as f:
    pdf_reader = PyPDF4.PdfFileReader(f)
    for i in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(i)
        width = page.cropBox.getWidth()
        height = page.cropBox.getHeight()
        print(f'Kích thước trang {i+1}: {width} x {height}')
