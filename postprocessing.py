import cv2
import pytesseract
import argparse


def postprocess(img):
    # use Tesseract to OCR the image
    txt = pytesseract.image_to_string(img, lang='hrv', config='--tessdata-dir .')
    return txt


if __name__ == "__main__":
    # construct the argument parser and parse the arguments}
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image to be OCR'd")
    args = vars(ap.parse_args())

    # load the input image and convert it from BGR to RGB channel
    # ordering}
    image = cv2.imread(args["image"])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    text = postprocess(image)
    print(text)
