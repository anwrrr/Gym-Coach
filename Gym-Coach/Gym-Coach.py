import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

text_offset_x = 0
text_offset_y = 15
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
font_thickness = 2
bg_color = (0, 0, 255) 
text_color = (0, 0,  0)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Could not open the webcam. Check that it is connected and not in use.")

#####################################################################################################
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle
#####################################################################################################
def Dumbbell_Bicep_Curl(image,pose,bg_color,side,stage,text,key):
                
                image.flags.writeable = False
                results = pose.process(image)
                image.flags.writeable = True


                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


                # Define rectangle coordinates
                rectangle_coords = ((text_offset_x, text_offset_y + 30), (text_offset_x + 100, text_offset_y - 60))

                # Draw filled rectangle
                cv2.rectangle(image, rectangle_coords[0], rectangle_coords[1], bg_color, cv2.FILLED)
                try:
                    landmarks = results.pose_landmarks.landmark
                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    # Calculate angle
                    angle = round(calculate_angle(shoulder, elbow, wrist))
                    angle2 = round(calculate_angle(rshoulder, relbow, rwrist))

                    if side == -1:
                        cv2.putText(image, "press l for left hand or r to right hand or q to exit", (500, 25), font, font_scale,
                                    text_color, font_thickness, cv2.LINE_AA)
                    else:
                        cv2.putText(image, "q to exit", (500, 25), font, font_scale,
                                    text_color, font_thickness, cv2.LINE_AA)
                    # Visualize angle
                    cv2.putText(image, str(angle),
                                tuple(np.multiply(elbow, [1300, 700]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    cv2.putText(image, str(angle2),
                                tuple(np.multiply([relbow[0] - .05, relbow[1]], [1300, 700]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    if side == -1:
                        if key & 0xFF == ord('l'):
                            side = 1
                        if key & 0xFF == ord('r'):
                            side = 2
                    elif side == 1:
                        if angle > 160:
                            stage = "down"
                            text = "Wait"
                            bg_color = (255, 0, 0)
                        if angle < 30 and stage == 'down':
                            stage = "up"
                            bg_color = (0, 255, 0)
                            text = "Correct"
                    elif side == 2:
                        if angle2 > 160:
                            stage = "down"
                            text = "Wait"
                            bg_color = (255, 0, 0)
                        if angle2 < 30 and stage == 'down':
                            stage = "up"
                            bg_color = (0, 255, 0)
                            text = "Correct"

                    cv2.putText(image, text, (text_offset_x + 25, text_offset_y + 10), font, font_scale, text_color,
                                font_thickness, cv2.LINE_AA)
                except:
                    pass
                
                return(image,bg_color,side,stage,text)
#####################################################################################################
def dumbbell_lateral_raise(results, image):
    dlr_status = 'Observing'
    text_color = (0, 0, 0)
    try:
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates
        # left side
        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        # right side
        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        
        # Calculate angle
        # left
        l_angle1 = round(calculate_angle(l_shoulder, l_elbow, l_wrist))
        l_angle2 = round(calculate_angle(l_hip, l_shoulder, l_elbow))
        # right
        r_angle1 = round(calculate_angle(r_shoulder, r_elbow, r_wrist))
        r_angle2 = round(calculate_angle(r_hip, r_shoulder, r_elbow))
        
        # Visualize angle
        cv2.putText(image, str(l_angle1), 
                        tuple(np.multiply(l_elbow, (1300, 700)).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
        )
        cv2.putText(image, str(l_angle2), 
                        tuple(np.multiply(l_shoulder, (1300, 700)).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
        )
        cv2.putText(image, str(r_angle1), 
                        tuple(np.multiply(r_elbow, (1300, 700)).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
        )
        cv2.putText(image, str(r_angle2), 
                        tuple(np.multiply(r_shoulder, (1300, 700)).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
        )
        if (l_angle1 >= 150 and l_angle2 >= 85
            and r_angle1 >= 150 and r_angle2 >= 85):
            dlr_status = "Correct"     
            text_color = (0, 200, 0)
        elif (abs(l_angle1 - r_angle1)  >= 40 
              or abs(l_angle2 - r_angle2) >= 40):
            dlr_status = "InCorrect"     
            text_color = (0, 0, 200)
        
    except:
        pass
    
    # Rep data
    cv2.rectangle(image, (0,0), (125,33), (245,117,16), -1)
    cv2.putText(image, dlr_status, (text_offset_x + 25, text_offset_y + 10), font, font_scale, text_color,
                                font_thickness, cv2.LINE_AA)
    cv2.putText(image, "q to exit", (250, 15), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
    return image
def Dumbbell_push_press(results,image):
    status="waiting"
    text_color = (0, 0, 0)
   #extract landmarks
    try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            #left side
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip =[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            ####### right side
            rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            rhip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            
            # Calculate angle
            anglel1 = round(calculate_angle(shoulder, elbow, wrist))
            anglel2 = round(calculate_angle(hip,shoulder, elbow))
            angler1 = round(calculate_angle(rshoulder, relbow, rwrist))
            angler2 = round(calculate_angle(rhip,rshoulder, relbow))

            
            # Visualize angle
            cv2.putText(image, str(anglel1), 
                           tuple(np.multiply(elbow, [1300, 700]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(anglel2), 
                           tuple(np.multiply(shoulder, [1300, 700]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(angler1), 
                           tuple(np.multiply(relbow, [1300, 700]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(angler2), 
                           tuple(np.multiply(rshoulder, [1300, 700]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            #correct or no
            if (anglel1 >= 160 and anglel2 >= 160
             and angler1 >= 160 and angler2 >= 160):
                status = "Correct"
                text_color = (0, 200, 0)
            else :
              status = "waiting"
              text_color = (200, 0, 0)
            
    
    except:
      pass

    cv2.rectangle(image, (0,0), (125,33), (245,117,16), -1)
    cv2.putText(image, status, (text_offset_x + 25, text_offset_y + 10), font, font_scale, text_color,
                                font_thickness, cv2.LINE_AA)

    cv2.putText(image, "q to exit", (250, 15), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
    return image

###########################################################################################
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        frame = cv2.resize(frame, (1300, 700))
        cv2.putText(frame, "press 1 for Dumbbell Bicep Curl", (450, 25), font, font_scale, text_color, font_thickness,
                        cv2.LINE_AA)
        cv2.putText(frame, "press 2 for Dumbbell lateral raise", (450, 50), font, font_scale, text_color, font_thickness,
                        cv2.LINE_AA)
        cv2.putText(frame, "press 3 for Dumbbell push press", (450, 75), font, font_scale, text_color, font_thickness,
                        cv2.LINE_AA)
        cv2.putText(frame, "or q to exit", (450, 100), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        cv2.imshow('Mediapipe Feed', frame)
        key = cv2.waitKey(10)
        if key & 0xFF == ord('1'):
            cv2.destroyAllWindows()
            side = -1
            text = 'Wait'
            stage = 'down'
            bg_color=(0,0,255)
            key=-1
            while cap.isOpened():
                ret,frame = cap.read()
                if not ret or frame is None:
                    break
                frame = cv2.resize(frame, (1300, 700))
                image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                (image,bg_color,side,stage,text)=Dumbbell_Bicep_Curl(image,pose,bg_color,side,stage,text,key)
                cv2.imshow("Dumbbell Bicep Curl", image)
                key=cv2.waitKey(10)
                if key & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break  

        elif key & 0xFF == ord('2'):
            cv2.destroyAllWindows()
            bg_color=(0,0,255)
            while cap.isOpened():
                ret,frame = cap.read()
                if not ret or frame is None:
                    break
                frame = cv2.resize(frame, (1300, 700))
                image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                image = dumbbell_lateral_raise(results, image)
                cv2.imshow("Dumbbell lateral raise", image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break  
        elif key & 0xFF == ord('3'):
             cv2.destroyAllWindows()
             bg_color=(0,0,255)
             while cap.isOpened():
                ret,frame = cap.read()
                if not ret or frame is None:
                    break
                frame = cv2.resize(frame, (1300, 700))
                image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                image = Dumbbell_push_press(results, image)
                cv2.imshow("Dumbbell push press", image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break 
            
        elif key & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
