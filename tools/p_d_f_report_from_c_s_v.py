import pandas as pd
from fpdf import FPDF


# Define the PDF class for report creation
class PDF(FPDF):
    def header(self):
        # Set font and add a title at the top of the page
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'CSV Report: codes_used.csv', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Add a page number in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def create_pdf_from_csv(csv_file, output_pdf):
    # Load the CSV content into a pandas DataFrame
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} does not exist.")
        return

    # Instantiate the PDF object
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)

    # Build the table header
    col_widths = [40] * len(df.columns)  # Example: Adjust individual column widths as needed
    for col in df.columns:
        pdf.cell(col_widths[0], 10, col, border=1, align='C')
    pdf.ln()

    # Fill the table with data row by row
    for index, row in df.iterrows():
        for item in row:
            pdf.cell(col_widths[0], 10, str(item), border=1, align='C')
        pdf.ln()

    # Output the resulting PDF
    pdf.output(output_pdf)
    print(f"PDF report successfully created: {output_pdf}")


if __name__ == "__main__":
    # Specify the input CSV and output PDF paths
    input_csv = "xxyears/static/codes_used.csv"
    output_pdf = "codes_used_report.pdf"

    # Generate the PDF report from the CSV file
    create_pdf_from_csv(input_csv, output_pdf)