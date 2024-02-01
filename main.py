import cv2
import math
import time
import communicate



#settings
##Face recognition
 ###Colors for rectangles
colors = [(255, 153, 204), (153, 255, 255), (153, 255, 153), (255, 153, 153), (255, 255, 153), (255, 153, 255), (153, 153, 255), (153, 255, 255), (255, 255, 255)]
 ###Controls how long to avarage face amounts
avarageMax = 20
confidenceMin = 0.5

##Leds
### arduino
USE_ARDUINO = False # Make sure to set this true when connecting arduino otherwise nothing happens

NUM_LEDS     = 60
BAUDRATE = 200000
PORT = 'COM4'
### animation
animationFrequencies = [1,2,3,4,5,6,7,8,9,10]
brightnessAmplitude = 200
brightnessOffset = 55




#leds

if USE_ARDUINO:
    print("Connecting "+str(NUM_LEDS)+" leds to "+PORT+" at "+str(BAUDRATE)+" baudrate")
    leds = [ [ 0, 0, 0 ] for i in range(NUM_LEDS) ]
    state = communicate.connect_waiting(baudrate=BAUDRATE, port=PORT)
    time.sleep(2)
else:
    print("Continuing without leds | set USE_ARDUINO to true to enable leds")
timestamp = time.time()




#Model data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Webcam
video_capture = cv2.VideoCapture(0)



amountArray = []

while True:
    try:
        ret, frame = video_capture.read()
        
        #convert to gray to improve performance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detection
        faces = face_cascade.detectMultiScale3(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels = True
        )

        rects = faces[0]
        neighbours = faces[1]
        weights = faces[2]


        amount = 0;

        #draw rectangles
        i = 0
        for (x, y, w, h) in rects:
            i+=1
            confidence = weights[i-1]
            if confidence > confidenceMin:
                amount += 1
                #draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), colors[amount], 2)

        #avarage amount
        amountArray.append(amount)
        if len(amountArray) > avarageMax:
            amountArray.pop(0)

        amount = sum(amountArray) / len(amountArray)

        #display amount
        cv2.putText(frame, 'Gezichten: ' + str(round(amount)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        print("Gemmideld " + str(amount) + " gezichten in beeld")


        #Led animation
        frequency = animationFrequencies[int(amount)]
        
        #get point on sinus
        t = time.time() - timestamp
        t = t * frequency
        amplitude = brightnessOffset + math.sin(t)*brightnessAmplitude

        #Display a pulsing heart in bottom left
        cv2.putText(frame, '<3', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, amplitude), 2)

        #display
        cv2.imshow('Video', frame)
    except Exception as error:        
        print("Foutmelding: " + str(error))

    else:
        print("Leds uit")
        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()

cv2.destroyAllWindows()