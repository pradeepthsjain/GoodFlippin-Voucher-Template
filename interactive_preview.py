import fitz  # PyMuPDF
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

class PDFVoucherPositioner:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Voucher Code Positioner")
        self.root.geometry("1400x900")
        
        self.pdf_path = "Good Flippin Burgers.pdf"
        self.doc = fitz.open(self.pdf_path)
        self.page = self.doc[0]
        
        # Default values
        self.x = 110
        self.y = 180
        self.sample_code = "1001"
        
        self.setup_ui()
        self.update_preview()
    
    def setup_ui(self):
        # Create main frames
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        preview_frame = ttk.Frame(self.root, padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Controls
        row = 0
        
        ttk.Label(control_frame, text="Position Controls", font=('Arial', 14, 'bold')).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        
        # X position
        ttk.Label(control_frame, text="X Position:", font=('Arial', 11)).grid(row=row, column=0, sticky=tk.W, pady=8)
        self.x_entry = ttk.Entry(control_frame, width=10, font=('Arial', 11))
        self.x_entry.insert(0, str(self.x))
        self.x_entry.grid(row=row, column=1, pady=8, padx=5)
        self.x_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        row += 1
        
        # Y position
        ttk.Label(control_frame, text="Y Position:", font=('Arial', 11)).grid(row=row, column=0, sticky=tk.W, pady=8)
        self.y_entry = ttk.Entry(control_frame, width=10, font=('Arial', 11))
        self.y_entry.insert(0, str(self.y))
        self.y_entry.grid(row=row, column=1, pady=8, padx=5)
        self.y_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        row += 1
        
        # Sample code input
        ttk.Label(control_frame, text="Sample Code:", font=('Arial', 11)).grid(row=row, column=0, sticky=tk.W, pady=8)
        self.code_entry = ttk.Entry(control_frame, width=10, font=('Arial', 11))
        self.code_entry.insert(0, self.sample_code)
        self.code_entry.grid(row=row, column=1, pady=8, padx=5)
        self.code_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        row += 1
        
        # Update button
        ttk.Button(control_frame, text="Update Preview", command=self.update_preview).grid(row=row, column=0, columnspan=2, pady=15)
        row += 1
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        # Current coordinates display
        ttk.Label(control_frame, text="Current Position:", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        self.coord_label = ttk.Label(control_frame, text=f"X: {self.x}, Y: {self.y}", font=('Arial', 10))
        self.coord_label.grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # Preview canvas with scrollbars
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='gray85')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scroll bars
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=v_scroll.set)
    
    def update_preview(self):
        try:
            # Get values from entries
            self.x = float(self.x_entry.get())
            self.y = float(self.y_entry.get())
            self.sample_code = self.code_entry.get()
            
            # Update coordinate label
            self.coord_label.config(text=f"X: {self.x}, Y: {self.y}")
            
        except ValueError:
            return  # Invalid number, skip update
        
        # Create temporary PDF with the code
        temp_doc = fitz.open(self.pdf_path)
        temp_page = temp_doc[0]
        
        # Draw red crosshair at the position
        temp_page.draw_line((self.x-15, self.y), (self.x+15, self.y), color=(1, 0, 0), width=2)
        temp_page.draw_line((self.x, self.y-15), (self.x, self.y+15), color=(1, 0, 0), width=2)
        
        # Draw a small circle at the exact position
        temp_page.draw_circle((self.x, self.y), 3, color=(1, 0, 0), fill=(1, 0, 0))
        
        # Insert the text
        temp_page.insert_text(
            (self.x, self.y),
            self.sample_code,
            fontsize=18,
            color=(0, 0, 0),
            fontname="helv",
        )
        
        # Render to image - fit to window
        pix = temp_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        img_data = pix.tobytes("ppm")
        
        image = Image.open(io.BytesIO(img_data))
        photo = ImageTk.PhotoImage(image)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        temp_doc.close()
    
    def __del__(self):
        if hasattr(self, 'doc'):
            self.doc.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFVoucherPositioner(root)
    root.mainloop()
