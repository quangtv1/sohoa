###############################################################################################
# CÁCH CHẠY: $ python3 1.page-index.py /mnt/c/Users/admin/Desktop/pdf_folder/
# KẾT QUẢ: là file exel cột 1 tên file pdf, cột 2 là vị trí của trang chứa ký tự tìm kiếm, cột 3 tổng số trang của file

import os
import PyPDF2
import pandas as pd
import argparse
import glob

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Search for a phrase in all PDF files in a directory')

# Add an argument for the directory containing the PDF files
parser.add_argument('directory', type=str, help='the directory containing the PDF files')

# Parse the command line arguments
args = parser.parse_args()

# Get the directory from the command line arguments
directory = args.directory


# Define the directory containing the PDF files
#directory = "/mnt/c/Users/admin/Desktop/pdf_folder/"

# Define the search phrase
search_phrase = "MUC"

# Initialize an empty list to store the search results
results = []


pdf_count = 0
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        pdf_count += 1
print("Number of PDF files in directory:", pdf_count)

pdf_thu = 0
# Loop through each file in the directory
for filename in os.listdir(directory):

    # Check if the file is a PDF file
    if filename.endswith(".pdf"):
        pdf_thu += 1

        # Open the PDF file in binary mode
        with open(os.path.join(directory, filename), 'rb') as pdf_file:

            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Get the total number of pages in the PDF file
            total_pages = len(pdf_reader.pages)

            # Initialize an empty list to store the page numbers where the phrase is found
            page_numbers = []

            # Loop through each page in the PDF file
            for page_number in range(total_pages):

                # Get the page object for the current page
                page = pdf_reader.pages[page_number]

                # Extract the text from the page
                text = page.extract_text()

                # Check if the search phrase is in the extracted text
                if search_phrase in text:
                    page_numbers.append(page_number + 1)
                    
                    
                    print(str(pdf_thu)+'/'+str(pdf_count), filename, str(page_number+1)+'/'+str(total_pages))                    
                    results.append({'Pdf thứ': str(pdf_thu) + '/' + str(pdf_count), 'File Pdf': filename, 'First': page_number+1, 'Tổng số trang': total_pages})


            # If the search phrase was found in the PDF file, add the file name and page numbers to the results list
            #if page_numbers:
            #    results.append({'File': filename, 'Page Numbers': page_numbers})

# Create a DataFrame from the search results
df = pd.DataFrame(results)

# Write the DataFrame to an Excel file
with pd.ExcelWriter('search_results.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)


###############################################################################################
#import os
#import PyPDF2
#import pandas as pd
#
## Open the PDF file in binary mode
#with open("/mnt/c/Users/admin/Desktop/2023-03-03.007.pdf", 'rb') as pdf_file: 
#
#    # Create a PDF reader object
#    pdf_reader = PyPDF2.PdfReader(pdf_file) 
#
#    # Get the total number of pages in the PDF file
#    total_pages = len(pdf_reader.pages) 
#
#    # Define the search phrase
#    search_phrase = "MUC" 
#
#    # Define the search phrase pattern using regex
#    #search_phrase = re.compile(r'MUC')
#
#
#
#    # Initialize an empty list to store the page numbers where the phrase is found
#    page_numbers = [] 
#
#    # Loop through each page in the PDF file
#    for page_number in range(total_pages): 
#
#        # Get the page object for the current page
#        page = pdf_reader.pages[page_number] 
#
#        # Extract the text from the page
#        text = page.extract_text() 
#
#        # Check if the search phrase is in the extracted text
#        if search_phrase in text: 
#            print(page_number+1)            
#
#            # Add the current page number to the list of page numbers
#            page_numbers.append(page_number + 1)         
           #
#    # Print the list of page numbers where the search phrase is found
#    print(page_numbers)
#
#

###############################################################################################
## CÁCH 2: SỬ DỤNG pytesseract
#import io
#import numpy as np
#from PIL import Image
#import pytesseract
#import fitz
#
## Load the PDF document
#doc = fitz.open("/mnt/c/Users/admin/Desktop/2023-03-14.020.pdf")
#
## Define the search phrase
#search_phrase = "MUC LUC"
#
## Initialize an empty list to store the page numbers where the phrase is found
#page_numbers = []
#
#   # Loop through each page in the PDF document
#for page_number in range(doc.page_count):
#    # Get the page object for the current page
#    page = doc[page_number]
    #
#    # Get the pixmap of the page
#    pixmap = page.get_pixmap()
#
    #
#    # Convert the pixmap to a numpy array
#    if pixmap.colorspace == 1:
#        n_components = 1
#    else:
#        n_components = 3
#    img = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.height, pixmap.width, n_components)
#
#    # Extract text from the image using Tesseract OCR
#    text = pytesseract.image_to_string(Image.fromarray(img), lang='eng')
    #
#    # Check if the search phrase is in the extracted text
#    if search_phrase in text:
#        # Add the current page number to the list of page numbers
#        page_numbers.append(page_number + 1)
        #
#    print(f"Processed page {page_number + 1}/{doc.page_count}")
#
## Print the list of page numbers where the search phrase is found
#print("Pages containing the search phrase:", page_numbers)
#


#import pdfquery
#
## Load the PDF document
#pdf = pdfquery.PDFQuery("/mnt/c/Users/admin/Desktop/2023-03-14.020.pdf")
#pdf.load()
#
## Define the search phrase
#search_phrase = "MUC LUC"
#
## Search for the search phrase in the PDF document
#page_numbers = []
#for page_number in range(1, len(pdf.pages) ):
#    pdf.load_page(page_number)
#    text_content = pdf.extract_text()
#    if search_phrase in text_content:
#        page_numbers.append(page_number)
#    print(f"Processed page {page_number}")
#
#
## Print the list of page numbers where the search phrase is found
#print("Pages containing the search phrase:", page_numbers)

