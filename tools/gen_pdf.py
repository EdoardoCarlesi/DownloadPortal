import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Read the CSV file
csv_file = 'data/codes.csv'  # Change this to your CSV file path
df = pd.read_csv(csv_file)
print(df.head())

# Function to create a PDF with a table
def create_pdf(output_file, data):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4

    # Table settings
    num_cols = 5
    num_rows = len(data) // num_cols + (len(data) % num_cols > 0)
    cell_width = width / num_cols
    cell_height = height / num_rows

    row_csv1 = []
    row_csv2 = []
    df = pd.DataFrame()

    for i, code in enumerate(data):
        row = i // num_cols
        col = i % num_cols
        x = col * cell_width
        y = height - (row + 1) * cell_height

        text = f"Redeem on www.xxyearsofsteel.com\n{code}\n"
        c.drawString(x + 0.5 * cm, y + cell_height - 1 * cm, text)
        
        if i<250:
            row_csv1.append(text)
        elif i>=250:
            row_csv2.append(text)

    #c.save()
    df['Codes1'] = row_csv1
    df['Codes2'] = row_csv2
    df.to_csv('redeem_codes.csv')

# Get the codes from the dataframe
#codes = df.iloc[:, 0].tolist()
codes = df['Code'].values#[0:10]

# Create the PDF
output_pdf = 'codes_table.pdf'  # Output PDF file
create_pdf(output_pdf, codes)

print(f"PDF created: {output_pdf}")

