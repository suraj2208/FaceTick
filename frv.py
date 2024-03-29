import cv2
import pickle

face_cascade = cv2.CascadeClassifier(r"C:\Users\Suraj\Desktop\frv\data\haarcascade_frontalface_alt2.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")


labels={"person_name":1}
with open("label.pickle","rb") as f:
    og_labels=pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture('test2.mp4')



while(cap.isOpened()):
    ret, frame = cap.read()

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        id_, conf=recognizer.predict(roi_gray)
        if conf>=10 and  conf<=99:
            print(id_)
            print(labels[id_])
            font=cv2.FONT_HERSHEY_SIMPLEX
            name=labels[id_]
            color=(255,255,255)
            stroke=2
            cv2.putText(frame, name,(x,y),font,1,color,stroke,cv2.LINE_AA)
            
        img_item="7.png"
        cv2.imwrite(img_item, roi_color)
        
        
        color=(255, 0, 0)
        stroke=2
        endcord_x = x + w
        endcord_y = y + h
        cv2.rectangle(frame, (x, y), (endcord_x, endcord_y),color,stroke)
        
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
