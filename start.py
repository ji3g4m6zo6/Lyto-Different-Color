import numpy as np
import cv2
from PIL import Image
import io
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


def find_different(arr):
    for num, i in enumerate(arr):
        if (arr.count(i) == 1):
            return num
    else:
        return 0


browser = webdriver.Chrome('./chromedriver')
url = 'https://www.facebook.com/instantgames/play/1099543880229447/'
browser.get(url)

input("Press Enter after the game is started...")
browser.set_window_size(393, 738)

while 1:
    # sct.get_pixels(mon)
    # img = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
    canvas = browser.find_element_by_xpath('//*[@id="quicksilver_player"]/div/div/iframe')
    img_bytes = canvas.screenshot_as_png
    img = np.asarray(Image.open(io.BytesIO(img_bytes)))

    # capture part of the image
    screen_x = 30
    screen_y = 200
    screen_w = 325 - screen_x
    screen_h = 540 - screen_y
    img = img[screen_y:screen_y + screen_h, screen_x:screen_x + screen_w]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               1,
                               20,
                               param1=50,
                               param2=30,
                               minRadius=3,
                               maxRadius=85)

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        this = []
        for (x, y, r) in circles:
            this.append(list(img[y, x, :]))
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
        # print(circles)
        nn = find_different(this)
        for num, (x, y, r) in enumerate(circles):
            if num == nn:
                cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                ActionChains(browser).move_to_element_with_offset(canvas, x + screen_x, y + screen_y).click().perform()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('test', np.array(img))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
