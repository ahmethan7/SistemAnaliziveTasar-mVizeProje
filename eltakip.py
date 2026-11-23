import cv2
import numpy as np
import pyautogui


cap = cv2.VideoCapture(0)

# RENK AYARLARI
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])
# 
last_action = ""

while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1) 
    h, w, _ = img.shape
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Ekrana klavuz çizgileri çiz
    cv2.line(img, (0, h//2), (w, h//2), (200, 200, 200), 1)
    cv2.line(img, (w//2, 0), (w//2, h), (200, 200, 200), 1)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        if radius > 15:
            cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            
            # 1. SES AYARI
            if y < (h * 0.3): # Nesne ekranın üst kısmındaysa
                pyautogui.press('volumeup')
                cv2.putText(img, "SES ARTIYOR", (w//2-50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            elif y > (h * 0.7): # Nesne ekranın alt kısmındaysa
                pyautogui.press('volumedown')
                cv2.putText(img, "SES AZALIYOR", (w//2-50, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 2. KLAVYE AYARI
            if x > (w * 0.8) and last_action != "right":
                pyautogui.press('right')
                last_action = "right"
            elif x < (w * 0.2) and last_action != "left":
                pyautogui.press('left')
                last_action = "left"
            elif (w * 0.4) < x < (w * 0.6):
                last_action = ""

    cv2.imshow("Final Projesi - Akdeniz Uni", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()