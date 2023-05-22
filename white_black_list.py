# import the necessary packages
import pytesseract
import argparse
import cv2


def white_black_list(img, whitelist, blacklist):
    options = ""

    # check to see if a set of whitelist characters has been provided,
    # and if so, update our options string
    if len(whitelist) > 0:
        options += "-c tessedit_char_whitelist={} ".format(whitelist)

    # check to see if a set of blacklist characters has been provided,
    # and if so, update our options string
    if len(blacklist) > 0:
        options += "-c tessedit_char_blacklist={}".format(blacklist)

    # OCR the input image using Tesseract
    txt = pytesseract.image_to_string(img, config=options)
    return txt


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image to be OCR'd")
    ap.add_argument("-w", "--whitelist", type=str, default="",
                    help="list of characters to whitelist")
    ap.add_argument("-b", "--blacklist", type=str, default="",
                    help="list of characters to blacklist")
    args = vars(ap.parse_args())

    # load the input image, swap channel ordering, and initialize our
    # Tesseract OCR options as an empty string
    image = cv2.imread(args["image"])
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
