import PyPDF2

def extract_text_from_pdf(pdf_path, txt_output_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create PDF reader object
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Initialize a variable to hold the extracted text
        full_text = ""
        
        # Loop through each page and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            full_text += text
        
    # Write the extracted text to a .txt file
    with open(txt_output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(full_text)
    
    print(f"Text successfully extracted to {txt_output_path}")

# Usage
pdf_file_path = "iesc111.pdf"  # Path to your PDF file
txt_file_path = "output.txt"   # Path to save the output text

extract_text_from_pdf(pdf_file_path, txt_file_path)
