import os
from flask import current_app
try:
    from xxyears.db import get_db
except:
    from db import get_db

import click
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO
import schedule
import time
import threading

@click.command('gen-report')
def generate_report():
    # Get database connection
    with current_app.app_context():
        db = get_db()
        
        # Query to get all user information including the registration date
        query = "SELECT email, code, code_sell, registration_date FROM user"
        
        # Execute query and fetch all results
        results = db.execute(query).fetchall()
        
        # Convert results to pandas DataFrame
        df = pd.DataFrame(results, columns=['Email', 'Code', 'Code type', 'Purchase Date'])
        
        # Convert 'Purchase Date' to datetime
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
        
        # Calculate total sales and total redeemed codes
        total_sales = df['Code type'].sum()
        total_redeemed = len(df) - total_sales
        
        # Calculate sales and redeemed codes for the last month
        last_month = pd.Timestamp.now() - pd.DateOffset(months=1)
        last_month_df = df[df['Purchase Date'] > last_month]
        last_month_sales = last_month_df['Code type'].sum()
        last_month_redeemed = len(last_month_df) - last_month_sales
        
        # Create a BytesIO object to store the PDF
        buffer = BytesIO()
        
        # Create the PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Add title with past month and current year
        styles = getSampleStyleSheet()
        title = f"Video Steam Subscriptions - {pd.Timestamp.now().strftime('%B %Y')}"
        elements.append(Paragraph(title, styles['Title']))
        
        # Convert DataFrame to a list of lists for the table
        df['Code type'] = df['Code type'].map({0: 'redeemed', 1: 'purchased'})
        
        # Format the Purchase Date
        df['Purchase Date'] = df['Purchase Date'].dt.strftime('%Y-%m-%d')
        
        # Convert DataFrame to a list of lists for the table
        data = [df.columns.tolist()] + df.values.tolist()
        # Create the table
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(t)
        # Add vertical spacing
        elements.append(Spacer(1, 20))

        # Add summary statistics
        styles = getSampleStyleSheet()
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            spaceAfter=10,
            alignment=1  # Center alignment
        )

        summary_items = [
            f"Total Sales: {total_sales}",
            f"Total Codes Redeemed: {total_redeemed}",
            f"Total Sales (Last Month): {last_month_sales}",
            f"Total Codes Redeemed (Last Month): {last_month_redeemed}"
        ]

        for item in summary_items:
            elements.append(Paragraph(item, summary_style))
        # Build the PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        # Save the PDF to the tmp folder
        tmp_folder = os.path.join(current_app.instance_path, '../tmp')
        os.makedirs(tmp_folder, exist_ok=True)
        pdf_path = os.path.join(tmp_folder, 'user_report.pdf')
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        
        print(f"Report generated and saved successfully at {pdf_path}")


def init_report_command(app):
    
        app.cli.add_command(generate_report)
        print("Report generated successfully")

# This function should be called in your app's initialization
# For example, in your __init__.py or wherever you create your app:
# from xxyears.report import init_report_scheduler
# init_report_scheduler(app)

if __name__ == '__main__':
    init_report_command(app)
    #generate_report()

