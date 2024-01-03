import subprocess
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, BufferedIOBase
import sfontmgr

def has_transparency(img : Image.Image):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False


def create_text_image(text : str, max_width : int, font_family : str, font_size : int, align_text : str = "left"):
    # Create a blank image with a white background
    temp_img = Image.new("L", (1, 1), color="white")
    temp_draw = ImageDraw.Draw(temp_img)

    # Load the specified font
    font = ImageFont.truetype(sfontmgr.findfont(font_family), font_size)

    # Calculate the size needed for the text
    # print(draw.textsize(text, font=font))
    print(temp_draw.textbbox((0,0), text=text, font=font))
    _, _, text_width, text_height = temp_draw.textbbox((0,0), text=text, font=font)
    
    text_img_buffer = Image.new("L", (text_width, text_height), color="white")
    tib_draw = ImageDraw.Draw(text_img_buffer)
    tib_draw.text((0, 0), text, fill="black", font=font, align=align_text)
    
    if text_width > max_width:
        text_img_buffer = text_img_buffer.resize((max_width, int(max_width / (text_width/text_height))), Image.Resampling.BICUBIC)
    
    del temp_img
    del temp_draw
    
    # Resize the image according to the text size
    # text_img_buffer = Image.new("RGB", (, 1), color="white")
    

    # Create a new image with enough height for the text
    image = Image.new("L", (max_width, text_img_buffer.height+10), color="white")
    image.paste(text_img_buffer)
    # draw = ImageDraw.Draw(image)

    # Draw the text on the image

    # Save the image as a BytesIO object
    img_byte_array = BytesIO()
    image.convert('1').save(img_byte_array, format="PPM") # .rotate(90, expand=True)
    img_byte_array.seek(0)

    return img_byte_array

def create_image(image_buf : BufferedIOBase, max_width : int):
    img_byte_array = BytesIO()
    temp_image = Image.open(image_buf)
    if has_transparency(temp_image):
        bgimg = Image.new("RGB", temp_image.size, (255,255,255))
        bgimg.paste(temp_image, (0,0), temp_image)
        temp_image = bgimg
    temp_image.resize((max_width, int(max_width / (temp_image.width/temp_image.height))), Image.Resampling.LANCZOS).convert('1', dither=Image.Dither.FLOYDSTEINBERG).save(img_byte_array, format="PPM")    
    img_byte_array.seek(0)

    return img_byte_array

if __name__ == "__main__":
    # Example usage:
    exit()
    text = subprocess.run(["neofetch", "--stdout"], stdout=subprocess.PIPE).stdout.decode()
    max_width = 384
    font_family = "Comic Sans MS"  # Replace with your font file
    font_size = 18
    
    image_file = create_text_image(text, max_width, font_family, font_size)
    
    # image_file now contains the image as a BytesIO object that you can work with
    # For instance, you can save it to a file or use it in other parts of your code
    # Example to save the image to a file:
    with open("text_image.pbm", "wb") as file:
        file.write(image_file.read())
