from imutils.video import VideoStream

import numpy as np
import cv2, time, imutils, argparse

class MakePhoto:
    def __init__(self, args, path):
        self.args = args
        self.path = path

    def Photo(self):
        print("loading model...")

        net = cv2.dnn.readNetFromCaffe(self.args["prototxt"], self.args["model"])

        # image = cv2.imread(args["image"])
        stream = VideoStream(src = 0).start()

        time.sleep(2)

        while True:
            frame = stream.read()

            frame = imutils.resize(frame, width=400)

            (h, w) = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

            print("detection...")

            net.setInput(blob)
            detections = net.forward()

            personFound = False

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if (confidence > self.args['confidence']):
                    print(detections)
                    # input()
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    
                    (startX, startY, endX, endY) = box.astype('int')
                    
                    text = "{:.2f} %".format(confidence * 100)
                    textY = startY - 10 if startY - 10 > 10 else startY + 10

                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

                    cv2.putText(frame, text, (startX, textY), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.45, (0, 0, 255), 1)
                    personFound = True
                else:
                    continue

            # cv2.imshow('Result', frame)
            if (not personFound): 
                stream.stop()
                cv2.imwrite(self.path, frame)
                print("Saved!")
                return False
            cv2.imwrite(self.path, frame)
            print("Saved!")
            break
            
            # key = cv2.waitKey(1)
            
            # if (key == ord("x")):
            #     break
            
        # cv2.destroyAllWindows()
        stream.stop()
        return True