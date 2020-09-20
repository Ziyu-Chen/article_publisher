from io import BytesIO
import win32clipboard
from PIL import Image


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def copy_text(text):
    send_to_clipboard(win32clipboard.CF_UNICODETEXT, data)


def copy_image(image_path):
    # file_path = './test.png'
    image = Image.open(image_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)