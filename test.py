import numpy as np
import cv2, os

directory_path = "./input/face_unblur/"
target_directory_path = "./input/face/"
count = 0

def crop_image(img):
    face_detect = cv2.CascadeClassifier('haarcascade.xml')
    face_data = face_detect.detectMultiScale(img, 1.3, 5)

    cropped_img = None
    for (x, y, w, h) in face_data:
        x = x + 100
        y = y + 100

        cropped_img = img[y-290:y+h+100, x-200:x+w+100]

    # cv2.imwrite(f"./junk/test.png", cropped_img)
    return cropped_img


def blur_face(img):
    global count
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_roi = None
    img = crop_image(img)
    face_detect = cv2.CascadeClassifier('haarcascade.xml')
    face_data = face_detect.detectMultiScale(img, 1.3, 5)
    roi_count = 0
    for (x, y, w, h) in face_data: 
        roi_count = roi_count + 1
        x = x + 100
        y = y + 100
        roi = img[y:y+h-200, x:x+w-200]
        # cropped_roi = img[y-270:y+h+100, x-200:x+w+100]
        # cv2.imwrite(f"./junk/test-{roi_count}.png", cropped_roi)
        # if count == 0:
        face_roi = img[y:y+roi.shape[0], x:x+roi.shape[1]]
        
        # applying a gaussian blur over this new rectangle area 
        roi = cv2.GaussianBlur(roi, (101, 101), 100)
        # impose this blurred image on original image to get final image 
        
        img[y:y+roi.shape[0], x:x+roi.shape[1]] = roi
        

        # # print(img[y-100:y+h-100, x:x+w-140].shape)
        # print(roi.shape)
        # print(img[y:y+roi.shape[0], x:x+roi.shape[1]].shape)
    # if count == 0:
    # face_roi = cropped_roi
    # cv2.imwrite("./junk/test.png", face_roi)
    cv2.imwrite(target_directory_path + filename, img)

    count = count + 1


for filename in os.listdir("./input/face/"):
    img = cv2.imread(directory_path + filename)
    print(img.shape)

# img1 = cv2.imread("./input/face/test25.png")
# img2 = cv2.imread("./input/face/image00013.png")
# img3 = cv2.imread("./unprocessed/test25.png")

# print(img1.shape)
# print(img2.shape)
# print(img3.shape)
    blurred_img = blur_face(img)

    # if count >3:
    #     break



