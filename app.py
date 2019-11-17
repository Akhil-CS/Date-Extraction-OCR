import base64
from io import BytesIO

from flask import Flask, jsonify, request
import re

from PIL import (Image, ImageFile)
from pytesseract import pytesseract
from dateutil import parser

ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)


def match_regex(list_text):
    """
    This function takes extracted text as input and returns the extracted date
    """
    regex = r"[\d]{1,2}[ ]*[-][ ]*[\d]{1,2}[ ]*[-][ ]*[1|2][\d]{1,3}|[\d]{1,2}[ ]*[/][ ]" \
            r"*[\d]{1,2}[ ]*[/][ ]*[1|2][\d]{1,3}|[\d]{1,2}[ ]*[.][ ]*[\d]{1,2}[ ]*[.][ ]" \
            r"*[1|2][\d]{1,3}|[\d]{1,2}[ ]*[-][ ]*(January|February|March|April|May|June|" \
            r"July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|" \
            r"Aug|Sep|Oct|Nov|Dec)\w*[ ]*[-][ ]*[1|2][\d]{1,3}|[\d]{1,2}[ ]*[/][ ]*(January|" \
            r"February|March|April|May|June|July|August|September|October|November|December|" \
            r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*[ ]*[/][ ]*[1|2][\d]{1,3}|" \
            r"[\d]{1,2}[ ]*[.][ ]*(January|February|March|April|May|June|July|August|September|" \
            r"October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*[ ]" \
            r"*[.][ ]*[1|2][\d]{1,3}|(January|February|March|April|May|June|July|August|September|" \
            r"October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ ]*[-|,]?[ ]" \
            r"*[\d]{1,2}[ ]*[-|,|']?[ ]*[1|2][\d]{3}"

    match_string = None
    for line in list_text:

        matches = re.finditer(regex, line, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            try:
                match_string = str(parser.parse(match.group(0)).date())
            except:
                match_string = str(match.group(0))
    return match_string


@app.route('/extract_date', methods=["POST"])
def image_process_and_get_date():
    """
    This function will handle the core OCR processing of images.
    """
    data = request.get_json()['base_64_image']
    im = Image.open(BytesIO(base64.b64decode(data)))
    rgb_im = im.convert('RGB')
    rgb_im.save('image1.jpeg', 'JPEG')
    text = pytesseract.image_to_string('image1.jpeg')
    list_text = text.split('\n')
    return jsonify({'date': match_regex(list_text)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
