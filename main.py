import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd

root = tk.Tk()
root.geometry("600x630")

path = 'photos'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

def Clicked():
    df=pd.read_csv('Attendance.csv')
    print(df)
def clicked():
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(name):
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            print(myDataList)
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)


image_path = "C:\\Users\\MYSQ\\Desktop\\attendance.jpg"  # Replace with the actual path to your image
image = Image.open(image_path)
image = image.resize((500, 400))

# Convert the image to Tkinter-compatible format
photo = ImageTk.PhotoImage(image)


image_label = tk.Label(root, image=photo).grid(row=1)

tk.Label(root, text="FACE RECOGNITION ATTENDANCE SYSTEM", font="arial 20 bold").grid(row=0)
tk.Button(root, text="Check Attendance",font="arial ", command=Clicked,padx=30,pady=30).grid(row=3, column=0)
tk.Button(root, text="Take Attendance",font="arial ", command=clicked,padx=30,pady=30).grid(row=2, column=0)



root.mainloop()