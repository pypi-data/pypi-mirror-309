import requests

def fetch_pdf():
    # URL of the PDF hosted on GitHub
    pdf_url = "https://github.com/himpar21/dlPDF/blob/main/DLCheat.pdf"
    
    try:
        # Fetch the PDF
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Save the PDF locally
        with open("downloaded_file.pdf", "wb") as file:
            file.write(response.content)
        
        print("PDF downloaded successfully as 'downloaded_file.pdf'!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the PDF: {e}")
