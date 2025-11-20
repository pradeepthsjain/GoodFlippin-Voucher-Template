import fitz  # PyMuPDF

pdf_path = "Good Flippin Burgers.pdf"
output_path = "Good Flippin Burgers - With Codes.pdf"

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
# Replace ↑ these positions with your exact 30 box coordinates

# ----------------------------------------
# ENTER YOUR 30 VOUCHER CODES
# ----------------------------------------
voucher_codes = [
    "1234", "5678", "9012", "3456", "7890", "2345",
    "1111", "2222", "3333", "4444", "5555", "6666",
    "7777", "8888", "9999", "1212", "3434", "5656",
    "7878", "9090", "1020", "3040", "5060", "7080",
    "9091", "1122", "3344", "5566", "7788", "9900"
]
# Replace ↑ with your 30 actual voucher codes

doc = fitz.open(pdf_path)
page = doc[0]

# ----------------------------------------
# PLACE EACH CODE AT ITS COORDINATE
# ----------------------------------------
for i, (x, y) in enumerate(coordinates):
    if i >= len(voucher_codes):
        break

    page.insert_text(
        (x, y),
        voucher_codes[i],
        fontsize=18,
        color=(0, 0, 0),      # black
        fontname="helv"
    )

doc.save(output_path)
doc.close()

print("Done! Saved as:", output_path)
