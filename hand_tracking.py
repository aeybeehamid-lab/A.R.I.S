import cv2
import mediapipe as mp
import pyautogui

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
lastGesture = None

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmList) != 0:
        fingers = []

        if lmList[4][1] > lmList[2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        tipIds = [8, 12, 16, 20]
        pipIds = [6, 10, 14, 18]

        for i in range(4):
            if lmList[tipIds[i]][2] < lmList[pipIds[i]][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers == [0, 0, 0, 0, 0]:
            gesture = "Fist"
        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "Open Palm"
        elif fingers == [0, 1, 0, 0, 0]:
            gesture = "Pointing"
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "Peace Sign"
        elif fingers == [1, 0, 0, 0, 0]:
            gesture = "Thumbs Up"
        else:
            gesture = "Unknown"

        if gesture != lastGesture:
            print(gesture)

            if gesture == "Open Palm":
                pyautogui.press("win")
                pyautogui.write("notepad")
                pyautogui.press("enter")

            elif gesture == "Fist":
                screenshot = pyautogui.screenshot()
                screenshot.save("screenshot.png")
                print("Screenshot saved")

            elif gesture == "Peace Sign":
                pyautogui.press("win")
                pyautogui.write("vscode")
                pyautogui.press("enter")

            lastGesture = gesture

    else:
        lastGesture = None

    cv2.imshow("A.R.I.S - Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()