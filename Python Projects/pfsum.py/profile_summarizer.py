import pandas as pd
from fpdf import FPDF
import subprocess
import os
import platform

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Faculty Profiles', 0, 1, 'C')
        self.ln(10)

    def set_table_header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(40, 10, 'Name', 1, 0, 'C')
        self.cell(50, 10, 'Publication Title', 1, 0, 'C')
        self.cell(50, 10, 'Authors', 1, 0, 'C')
        self.cell(40, 10, 'Journal/Conference', 1, 0, 'C')
        self.cell(20, 10, 'Year', 1, 0, 'C')
        self.cell(40, 10, 'DOI/Link', 1, 1, 'C')

    def add_table_row(self, row):
        self.set_font('Arial', '', 10)
        self.cell(40, 10, row['Name'], 1, 0, 'L')
        self.cell(50, 10, row['Publication Title'], 1, 0, 'L')
        self.cell(50, 10, row['Authors'], 1, 0, 'L')
        self.cell(40, 10, row['Journal/Conference'], 1, 0, 'L')
        self.cell(20, 10, str(row['Year']), 1, 0, 'C')
        self.cell(40, 10, row['DOI/Link'], 1, 1, 'L')

def open_file(file_path):
    try:
        if platform.system() == 'Darwin':  
            subprocess.call(('open', file_path))
        elif platform.system() == 'Windows':  
            os.startfile(file_path)
        else:  
            subprocess.call(('xdg-open', file_path))
    except Exception as e:
        print(f"Error opening file: {e}")

def main():
    excel_file_path = 'profiles.xlsx'
    pdf_file_path = 'profiles_summary.pdf'

    if not os.path.isfile(excel_file_path):
        print(f"Excel file not found: {excel_file_path}")
        return

    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    required_columns = ['Name', 'Publication Title', 'Authors', 'Abstract', 'Journal/Conference', 'Year', 'DOI/Link']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following required columns are missing in the Excel file: {', '.join(missing_columns)}")
        return

    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.add_page()

    pdf.set_table_header()

    for index, row in df.iterrows():
        try:
            pdf.add_table_row(row)
        except KeyError as e:
            print(f"Missing data in row {index}: {e}")
            continue

    try:
        pdf.output(pdf_file_path)
        print("PDF generated successfully!")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return

    open_file(pdf_file_path)
if __name__ == "__main__":
    main()