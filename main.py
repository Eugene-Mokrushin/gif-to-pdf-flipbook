from PIL import Image
from fpdf import FPDF
import os

def gif_to_frames(gif_path):
    """Extract frames from GIF and return them as a list of PIL Images."""
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy().convert('RGB')
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

def frames_to_pdf(frames, pdf_path, frames_per_page=6, row_gap=10):
    """Convert list of frames into a PDF, with multiple frames per page, keeping aspect ratio and adding row margin."""
    pdf = FPDF('P', 'mm', 'A4')
    page_width, page_height = 210, 297  # A4 size in mm
    margin = 10  # Margin around the page in mm

    # Calculate space available for images
    image_slot_width = (page_width - 2 * margin) / 2  # 2 images per row
    image_slot_height = ((page_height - 2 * margin) - 2 * row_gap) / 3  # 3 images per column with gaps

    for i in range(0, len(frames), frames_per_page):
        pdf.add_page()
        for j in range(frames_per_page):
            if i + j < len(frames):
                frame = frames[i + j]
                aspect_ratio = frame.width / frame.height
                if aspect_ratio > 1:
                    img_width = min(image_slot_width, frame.width * image_slot_height / frame.height)
                    img_height = img_width / aspect_ratio
                else:
                    img_height = min(image_slot_height, frame.height * image_slot_width / frame.width)
                    img_width = img_height * aspect_ratio
                x = margin + (j % 2) * image_slot_width + (image_slot_width - img_width) / 2
                y = margin + (j // 2) * (image_slot_height + row_gap) + (image_slot_height - img_height) / 2
                frame_path = f"frame_{i+j}.png"
                frame.save(frame_path)
                pdf.image(frame_path, x, y, img_width, img_height)
                os.remove(frame_path)

    pdf.output(pdf_path)

def gif_to_pdf(gif_path, pdf_path):
    frames = gif_to_frames(gif_path)
    frames_to_pdf(frames, pdf_path)

# Example usage
gif_path = 'tenor.gif'
pdf_path = 'flipbook.pdf'
gif_to_pdf(gif_path, pdf_path)

print(f"Flipbook PDF saved as {pdf_path}")
