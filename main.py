import fitz  # PyMuPDF
import csv
import os

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------
pdf_path = r"C:\PRADEEPTH\Photobooth\Voucher code Template\Good Flippin Burgers-2.pdf"
csv_path = r"C:\PRADEEPTH\Photobooth\Voucher code Template\50.csv"
output_folder = r"C:\PRADEEPTH\Photobooth\Voucher code Template\output"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# ----------------------------------------
# ENTER YOUR 30 (x, y) COORDINATES HERE
# Coordinates must match the PDF's coordinate system (points)
# ----------------------------------------
coordinates = [
    (30, 125), (30, 880), (300, 729), (570, 578), (840, 427), (1110, 276),
    (30, 276), (300, 125), (300, 880), (570, 729), (840, 578), (1110, 427),
    (30, 427), (300, 276), (570, 125), (570, 880), (840, 729), (1110, 578),
    (30, 578), (300, 427), (570, 276), (840, 125), (840, 880), (1110, 729),
    (30, 729), (300, 578), (570, 427), (840, 276), (1110, 125), (1110, 880)
]

# ----------------------------------------
# READ VOUCHER CODES FROM CSV
# ----------------------------------------
voucher_codes = []
with open(csv_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        voucher_codes.append(row['Voucher Code'])

print(f"Total voucher codes loaded: {len(voucher_codes)}")

# ----------------------------------------
# GENERATE PDFs (30 codes per PDF)
# ----------------------------------------
codes_per_pdf = 30
total_pdfs = (len(voucher_codes) + codes_per_pdf - 1) // codes_per_pdf  # Ceiling division

for pdf_num in range(total_pdfs):
    start_idx = pdf_num * codes_per_pdf
    end_idx = min(start_idx + codes_per_pdf, len(voucher_codes))
    
    # Get the batch of codes for this PDF
    current_batch = voucher_codes[start_idx:end_idx]
    
    # Open a fresh copy of the template PDF
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Place each code at its coordinate
    for i, code in enumerate(current_batch):
        if i >= len(coordinates):
            break
        
        x, y = coordinates[i]
        page.insert_text(
            (x, y),
            str(code),
            fontsize=18,
            color=(0, 0, 0),  # black
            fontname="helv"
        )
    
    # Save the PDF
    output_path = os.path.join(output_folder, f"Voucher_Batch_{pdf_num + 1:03d}.pdf")
    doc.save(output_path)
    doc.close()
    
    print(f"Generated: {output_path} (Codes {start_idx + 1} to {end_idx})")

print(f"\nDone! Generated {total_pdfs} PDF(s) in folder: {output_folder}")
