#30.08.23
#Reconocimiento 2.py 
import serial, time,cv2 as cv ,face_recognition as fr

# Conexión a Arduino 
arduino = serial.Serial('COM3', 9600)
time.sleep(5) 

# Reconocimiento de rostro
image = cv.imread("entrenamiento\CamilaCabello\img1.jpg")
face_loc = fr.face_locations(image)[0]
face_image_encodings = fr.face_encodings(image, known_face_locations=[face_loc])[0]

# Captura de cámara 
cap = cv.VideoCapture(1)
# Para el temporizador
last_face_detected_time = None
while(True):
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    face_locations = fr.face_locations(frame, model="hog")
    
    if len(face_locations) == 1:  # Solo una cara detectada
        last_face_detected_time = time.time() #actualizacion de tiempo 
        face_location = face_locations[0]
        face_frame_encodings = fr.face_encodings(frame, known_face_locations=[face_location])[0]
        result = fr.compare_faces([face_image_encodings], face_frame_encodings)
        
        if result[0] == True:
            text = "Camila Cabello"
            color = (125, 220, 0)
            arduino.write(b'1')
        else:
            text = "Desconocido"
            color = (50, 50, 255)
            arduino.write(b'0')
            
        cv.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
        cv.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
        cv.putText(frame, text, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)

    elif len(face_locations) > 1:  # Más de una cara detectada
        cv.putText(frame, "Por favor, solo un rostro para el reconocimiento", (30, 30), 2, 0.7, (0, 0, 255), 1)

       # Verificar tiempo transcurrido desde la última detección
    if last_face_detected_time and (time.time() - last_face_detected_time) > 3:
        arduino.write(b'2')  # Nuevo comando para apagar ambos LEDs
        last_face_detected_time = None  # Resetea el temporizador
    
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == 27:  # tecla ESC
        break;

cap.release()
cv.destroyAllWindows()
arduino.close()