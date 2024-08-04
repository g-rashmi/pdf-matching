import re
from PyPDF2 import PdfReader

# Text Extraction from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path);
    text = ""
    for page in reader.pages:
        text += page.extract_text();
    return text

# Feature Extraction from Text
def extract_features(text):
    # Example: Extract numbers, dates, and keywords
    numbers = re.findall(r'\d+', text) 
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
    keywords = re.findall(r'\b(?:invoice|total|amount|date|number|due|pay)\b', text, re.IGNORECASE)
    return numbers + dates + keywords

# Jaccard Similarity Calculation
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return (intersection / union)*100;

def calculate_similarity(text1, text2):
    features1 = set(extract_features(text1))
    features2 = set(extract_features(text2))
    return jaccard_similarity(features1, features2)

# Invoice Database(consist of some invoices )
class InvoiceDatabase:
    def __init__(self):
        self.invoices = []

    def add_invoice(self, invoice_text):
        self.invoices.append(invoice_text)

    def find_most_similar(self, input_text):
        max_similarity = 0
        most_similar_invoice = None
        for invoice_text in self.invoices:
            similarity = calculate_similarity(input_text, extract_text_from_pdf(invoice_text))
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_invoice = invoice_text
        return most_similar_invoice, max_similarity

# Main Function
def main():
    db = InvoiceDatabase();

    # Add existing invoices to the database
    db.add_invoice("./train/2024.03.15_0954.pdf")
    db.add_invoice("./train/2024.03.15_1145.pdf")
    db.add_invoice("./train/faller_8.pdf")
    db.add_invoice("./train/invoice_77073.pdf")
    db.add_invoice("./train/invoice_102856.pdf")
  
    # Add more invoices as needed......

    # Input invoice(here if input invoice path is provided)
    input_invoice_text = extract_text_from_pdf("./test/invoice_77098.pdf")

    # Find the most similar invoice
    most_similar_invoice, similarity_score = db.find_most_similar(input_invoice_text);
#here we will get as most similar invoice path 
    print("Most Similar Invoice path:", most_similar_invoice)
    print("Similarity Score:", similarity_score);

if __name__ == "__main__":
    main()
