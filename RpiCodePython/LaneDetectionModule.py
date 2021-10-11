import cv2
import numpy
import utlis

curveList = []
avgVal = 10


def getLaneCurve(img, display=2):
    imgCopy = img.copy()
    imgResult = imgCopy

    # STEP 1 : get binare image(black and white) from the orginal image using the tesholding function
    imgThresh = utlis.thresholding(img)

    # STEP 2 get the warped view from the property of the orignal image
    heightTarget, widthTarget, chanel = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThresh, points, widthTarget, heightTarget)
    imgWarpPoints = utlis.drawPoints(imgCopy, points)

    # STEP 3
    # basePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    # STEP 4 : averaging
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    # STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, widthTarget, heightTarget, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:heightTarget // 3, 0:widthTarget] = 0, 0, 0
        imgLaneColor = numpy.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (widthTarget // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (widthTarget // 2, midY), (widthTarget // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((widthTarget // 2 + (curve * 3)), midY - 25), (widthTarget // 2 + (curve * 3), midY + 25),
                 (0, 255, 0), 5)
        for x in range(-30, 30):
            w = widthTarget // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)

    #cv2.imshow('Threshold Image', imgThresh)
    #cv2.imshow('Warped Image', imgWarp)
    #cv2.imshow('Warp Points', imgWarpPoints)
    #cv2.imshow('Histogram', imgHist)

    #### NORMALIZATION
    curve = curve / 100
    if curve > 1:
        curve == 1
    if curve < -1:
        curve == -1

    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture('vid1.mp4')
    initialTrackBarVal = [102, 80, 20, 214]
    utlis.initializeTrackbars(initialTrackBarVal)

    frameCounter = 0

    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read(0)
        img = cv2.resize(img, (480, 240))
        getLaneCurve(img, display=2)

        cv2.imshow('vid', img)
        cv2.waitKey(1)
