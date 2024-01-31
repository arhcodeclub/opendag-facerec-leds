import cv2

#settings
##Colors for rectangles
colors = [(255, 153, 204), (153, 255, 255), (153, 255, 153), (255, 153, 153), (255, 255, 153), (255, 153, 255), (153, 153, 255), (153, 255, 255), (255, 255, 255)]
##Controls how long to avarage face amounts
avarageMax = 20




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


        #display
        cv2.imshow('Video', frame)
    except Exception as error:        
        print("Foutmelding: " + str(error))

    if (amount > 0.7):
        print("Leds aan")
        ## LED SCRIPT CODE ##
        #
        #
        #
        #
        #
        #
    else:
        print("Leds uit")
        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()

cv2.destroyAllWindows()