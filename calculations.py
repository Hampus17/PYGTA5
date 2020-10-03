
# Draw the lanes on the original image (for debug purposes)
def draw_lanes(image, lines):
    try:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(image, 'Lines: Detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)

    except:  
        cv2.putText(image, 'Lines: Not Detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
        pass