import cv2 as cv
import sys

img=cv.imread('opera.jpg')

if img is None :
    sys.exit('파일을 찾을 수 없습니다.')

gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
gray_small = cv.resize(gray, dsize=(0,0), fx = 0.5, fy = 0.5)

date_text = "2026.03.23"

cv.putText(
    gray_small,
    date_text,
    (100, 90),  # 위치
    cv.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)


cv.imshow('Image Display', img)
cv.imshow('Gray image small', gray_small)


cv.waitKey()
cv.destroyAllWindows()