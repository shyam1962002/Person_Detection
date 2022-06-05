import numpy as np
import face_recognition as fr
import cv2
import smtplib
from email.message import EmailMessage
import pywhatkit as pwk
import os
from datetime import datetime
myobj=datetime.now()


video_capture= cv2.VideoCapture(0)
prithivi_image = fr.load_image_file('10.jpg')
prithivi_face_encoding = fr.face_encodings(prithivi_image)[0]
known_face_encondings = [prithivi_face_encoding]
known_face_names = ["PRITHIVIRAJ"]

i=0

while True: 
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_face_encondings, face_encoding)
        name = "Unknown"
        face_distances = fr.face_distance(known_face_encondings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        ret,frame=video_capture.read()
        
            
        if(name=="Unknown"):
            cv2.imwrite('Frame'+str(i)+'.jpg', frame)
            msg=EmailMessage()
            msg['Subject']='HOME'
            msg['From']='saraprit2002@gmail.com'
            msg['To']='saraprit2002@gmail.com','shyam1962002@gmail.com'
            msg.set_content(name)
            with open('Frame0.jpg','rb')as f:
                file_data=f.read()
                file_name=f.name
                            
                msg.add_attachment(file_data,maintype="application",subtype="JPG",filename=file_name)
            
            h=myobj.hour
            mi=myobj.minute
            m=mi+1
            
            server=smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.login('saraprit2002@gmail.com','hlvnwpembrsrhwtr')
            server.send_message(msg)
            server.quit() 
            
            print('mail sent')
            pwk.sendwhatmsg("+917904893754", "UNKNOWN PERSON",h,m)
            file_path = '/Frame0.jpg'
            os.remove(file_path)
            
            
        elif(name=="PRITHIVIRAJ"):
            msg=EmailMessage()
            msg['Subject']='HOME'
            msg['From']='saraprit2002@gmail.com'
            msg['To']='saraprit2002@gmail.com','shyam1962002@gmail.com'
            msg.set_content(name)
            server=smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.login('saraprit2002@gmail.com','hlvnwpembrsrhwtr')
            server.send_message(msg)
            server.quit()  
            print('mail sent')
               
    cv2.imshow('Webcam_facerecognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()