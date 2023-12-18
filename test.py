import PyPDF2

# Qasim : 0315 2968299

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_file_path = 'your_pdf_file.pdf'

# Specify the page range you want to extract (10 to 15)
start_page = 10
end_page = 15

# Initialize an empty string to store the text
text = ""

# Open the PDF file in read-binary mode
with open(pdf_file_path, 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Check if the specified page range is within the total page count
    total_pages = pdf_reader.getNumPages()
    if start_page > total_pages or end_page > total_pages:
        print("Page range is out of bounds.")
    else:
        # Iterate through the specified page range (10 to 15)
        for page_number in range(start_page - 1, end_page):
            # Get the page object
            page = pdf_reader.getPage(page_number)

            # Extract the text from the page
            page_text = page.extractText()

            # Append the text from this page to the overall text
            text += page_text

# Print or use the extracted text
print(text)
