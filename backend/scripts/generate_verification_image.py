"""Generate verification test image"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create a 1080x1080 image with brand colors
width, height = 1080, 1080
background_color = (10, 13, 18)  # #0A0D12
text_color = (164, 180, 255)  # #A4B4FF

# Create image
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Try to use a nice font, fallback to default
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw text
y_position = 300

# Checkmark
draw.text((width//2, y_position), "✓", fill=text_color, font=font_large, anchor="mm")
y_position += 120

# Main text
draw.text((width//2, y_position), "Instagram", fill=text_color, font=font_medium, anchor="mm")
y_position += 80
draw.text((width//2, y_position), "Connection Test", fill=text_color, font=font_medium, anchor="mm")
y_position += 120

# Bottom text
draw.text((width//2, y_position), "Reels Studio", fill=(255, 255, 255), font=font_small, anchor="mm")

# Save image
output_path = "/home/ubuntu/reelai/backend/assets/verification_test.jpg"
image.save(output_path, "JPEG", quality=95)
print(f"✓ Verification test image created: {output_path}")
