import cv2
import numpy


def thresholding(img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerWhite = numpy.array([85, 0, 0])
    upperWhite = numpy.array([179, 160, 255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    return maskWhite


def warpImg(img, points, width, height, inv=False):
    pts1 = numpy.float32(points)
    pts2 = numpy.float32([[0, 0], [width, 0], [0, height], [width, height]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (width, height))
    return imgWarp


def nothing(x):
    pass


def initializeTrackbars(initialTrackbarVal, widthTarget=480, heightTarget=240):
    cv2.namedWindow('Trackbars')
    cv2.resizeWindow('Trackbars', 360, 240)
    cv2.createTrackbar('Width Top', 'Trackbars', initialTrackbarVal[0], widthTarget // 2, nothing)
    cv2.createTrackbar('Height Top', 'Trackbars', initialTrackbarVal[1], heightTarget, nothing)
    cv2.createTrackbar('Width Bottom', 'Trackbars', initialTrackbarVal[2], widthTarget // 2, nothing)
    cv2.createTrackbar('Height Bottom', 'Trackbars', initialTrackbarVal[3], heightTarget, nothing)


def valTrackbars(widthTarget=480, heightTarget=240):
    widthTop = cv2.getTrackbarPos('Width Top', 'Trackbars')
    heightTop = cv2.getTrackbarPos('Height Top', 'Trackbars')
    widthBottom = cv2.getTrackbarPos('Width Bottom', 'Trackbars')
    heightBottom = cv2.getTrackbarPos('Height Bottom', 'Trackbars')
    points = numpy.float32([(widthTop, heightTop),
                            (widthTarget - widthTop, heightTop),
                            (widthBottom, heightBottom),
                            (widthTarget - widthBottom, heightBottom)
                            ])
    return points


def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img


def getHistogram(img, minPer=0.1, display=False, region=4):
    if region == 1:
        histValues = numpy.sum(img, axis=0)
    else:
        histValues = numpy.sum(img[img.shape[0] // region:, :], axis=0)
    #print(histValues)
    maxValues = numpy.max(histValues)
    minValues = minPer * maxValues

    indexArray = numpy.where(histValues >= minValues)
    basePoint = int(numpy.average(indexArray))
    #print(basePoint)

    if display:
        imgHist = numpy.zeros((img.shape[0], img.shape[1], 3), numpy.uint8)
        for x, intensity in enumerate(histValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0] - intensity // 255 // region), (255, 0, 2551), 1)
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return basePoint, imgHist

    return basePoint


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = numpy.zeros((height, width, 3), numpy.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = numpy.hstack(imgArray[x])
        ver = numpy.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
                if len(imgArray[x].shape) == 2:
                    imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = numpy.hstack(imgArray)
        ver = hor
    return ver
