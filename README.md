# FYLE - Data Extraction

The below API is used to extract date from a receipt image 

# Libraries Used :

1. PyTesseract to extract text from images
2. Regex patterns to find match across date formats.

Rest API :-
Input : Base 64 Image Data

Output : Extracted Date

Postman Collection :
https://www.getpostman.com/collections/3df3d7772774bab256fb

API :
http://18.217.27.177:8000/extract_date

Install Requirements using pip install -r requirements.txt

# Future Enhancements :

To increase the accuracy of OCR we can use Image Processing techniques using OpenCV.
