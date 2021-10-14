from djitellopy import tello
import cv2
import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import time

me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()

# Move using Distance
me.move_up(80)

# Move using Speed
me.send_rc_control(0, 0, 0, 20)
time.sleep(5)
me.send_rc_control(0, 0, 0, 0)

me.streamoff()
me.streamon()

prediction_key = 'YOUR PREDICTION KEY'
ENDPOINT = 'YOUR PROEJECT ENDPOINT'
project_id = 'YOUR PROEJECT ID'
PUBLISH_ITERATION_NAME = 'YOUR ITERATION'

while True:
    img = me.get_frame_read().frame
    
    img = cv2.resize(img, (640, 480))
    shape = img.shape
    filename = 'tmp.jpg'
    cv2.imwrite(filename, img)

    credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(endpoint=ENDPOINT, credentials=credentials)
    
    with open(os.path.join("tmp.jpg"), mode="rb") as test_data:
        results = predictor.detect_image(project_id, PUBLISH_ITERATION_NAME, test_data)
        filtered_preds = [prediction for prediction in results.predictions if prediction.probability > 0.60]
        
        for pred in filtered_preds:
            x = int(pred.bounding_box.left * shape[1])
            y = int(pred.bounding_box.top * shape[0])

            start_point = (x, y)

            x2 = x + int(pred.bounding_box.width * shape[1])
            y2 = y + int(pred.bounding_box.height * shape[0])

            end_point = (x2, y2)


            img = cv2.rectangle(img, start_point, end_point, (0,0,255), 2)
            img = cv2.putText(img, pred.tag_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Image", img)

    print(results)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()




    