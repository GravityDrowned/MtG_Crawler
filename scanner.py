# Paying money for scanning more then 99 cards? no thank you.
import cv2
import numpy as np
import os


def diff(first, second):
    try:
        # they have to be the same size.

        # get the diff
        diff = cv2.absdiff(first, second)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # binarize it
        # thresh = cv2.threshold(diff, 1, 255, cv2.THRESH_BINARY_INV)
        ret, thresh = cv2.threshold(diff, 42, 255, cv2.THRESH_BINARY)

        # find contours in threshold
        # contours, hierachy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # output drawing
        out = second

        #cv2.drawContours(out, contours, -1, (0,255,0), 3)

        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(out, [box], 0, (0, 0, 255), 2)

        x, y, w, h = cv2.boundingRect(contours[0])

        # [[321 427], [240 427], [240 333], [321 333]]

        roi = out[y:y+h, x:x+w]

        #cv2.imshow("FIRST", first);
        #cv2.imshow("SECOND", second);
        cv2.imshow("ABS-DIFF", diff);
        cv2.imshow("THRESH", thresh);
        cv2.imshow("OUTPUT", out);
        cv2.imshow("ROI", roi);

        # cv2.waitKey();
    except:
        a= 1


def scan():
    '''
    scans continously
    collects scans in a list, writes that to a file or seomething
    :return:
    '''
    # Idea Nr 1. image recognition on the cards
    # Idea Nr 2. the name,... the name is literally printed on top?

    # Read from Webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    ret, frame = cap.read()
    first = frame

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            second = frame
            diff(first, second)
            # first = second

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    scan()
