import cv2 # type: ignore
import face_recognition # type: ignore

img=cv2.imread("messi.jpg")
rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img_encoding=face_recognition.face_encodings(rgb_img)[0]

img2=cv2.imread("images/messi 2.jpg")
rgb_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
img_encoding2=face_recognition.face_encodings(rgb_img2)[0]

result=face_recognition.compare_faces([img_encoding],img_encoding2)
print("result:",result)

cv2.imshow("img",img)
cv2.imshow("img 2",img2)
cv2.waitKey(0)