##  python3 1.find-muc-luc-v1.py "MUC" "/mnt/g/Shared drives/TTCNTT/Job CNTT/2023-02_Hoa Binh/1. SCAN ALL/HoaBinh/QuynhLam/6.BD/Scan03_QL_BD_20230330_002.pdf"

import sys
import PyPDF2
import re

# Get the file path from the command line arguments
file_path = sys.argv[2]

# Get the search phrase from the command line arguments
search_phrase = sys.argv[1]

# Open the PDF file in binary mode
with open(file_path, 'rb') as pdf_file: 

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file) 

    # Get the total number of pages in the PDF file
    total_pages = len(pdf_reader.pages) 

    # Define the search phrase pattern using regex
    search_phrase_pattern = re.compile(search_phrase)

    # Initialize an empty list to store the page numbers where the phrase is found
    page_numbers = [] 

    # Loop through each page in the PDF file
    for page_number in range(total_pages): 

        # Get the page object for the current page
        page = pdf_reader.pages[page_number] 

        # Extract the text from the page
        text = page.extract_text() 

        # Check if the search phrase is in the extracted text
        if search_phrase_pattern.search(text): 
            print(page_number+1)            

            # Add the current page number to the list of page numbers
            page_numbers.append(page_number + 1)         
           
    # Print the list of page numbers where the search phrase is found
    print(page_numbers)
