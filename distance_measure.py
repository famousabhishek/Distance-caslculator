import cv2
import numpy as np

selected_points = []
lines = []
undo_stack = []
current_shape = None  


PIXEL_TO_FEET = 0.000866  

buttons = {
    "Reset": (10, 10, 110, 50),
    "Undo": (120, 10, 220, 50),
    "Circle": (230, 10, 330, 50),
    "Rectangle": (340, 10, 470, 50),
    "Square": (480, 10, 580, 50),
    "Quit": (590, 10, 690, 50)
}

def draw_buttons(frame):
    """Draw buttons on screen."""
    for name, (x1, y1, x2, y2) in buttons.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), -1)
        cv2.putText(frame, name, (x1 + 10, y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (255, 255, 255), 2)

def inside_button(x, y):
    """Check if click is inside a button."""
    for name, (x1, y1, x2, y2) in buttons.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return name
    return None

def mouse_callback(event, x, y, flags, param):
    global selected_points, lines, undo_stack, current_shape

    if event == cv2.EVENT_LBUTTONDOWN:
        btn = inside_button(x, y)
        if btn:
            if btn == "Reset":
                selected_points.clear()
                lines.clear()
                undo_stack.clear()
            elif btn == "Undo":
                undo_action()
            elif btn == "Circle":
                current_shape = "circle"
            elif btn == "Rectangle":
                current_shape = "rectangle"
            elif btn == "Square":
                current_shape = "square"
            elif btn == "Quit":
                cv2.destroyAllWindows()
                exit()
        else:
            selected_points.append((x, y))
            undo_stack.append(('add_point', (x, y)))
            if len(selected_points) >= 2:
                cv2.line(param, selected_points[-2], selected_points[-1], (0, 255, 0), 2)
                lines.append((selected_points[-2], selected_points[-1]))
                undo_stack.append(('add_line', lines[-1]))

def calculate_distance(p1, p2):
    """Calculate distance in cm, inch, feet, meter."""
    pixel_distance = np.sqrt((p2[0] - p1[0])*2 + (p2[1] - p1[1])*2)
    feet = pixel_distance * PIXEL_TO_FEET
    return {
        "feet": f"{feet:.2f} ft",
        "inch": f"{feet * 12:.2f} in",
        "cm": f"{feet * 30.48:.2f} cm",
        "meter": f"{feet * 0.3048:.2f} m"
    }

def calculate_area(points, shape):
    """Calculate area of shape in square feet."""
    if shape == "rectangle" and len(points) >= 4:
        w = np.linalg.norm(np.array(points[0]) - np.array(points[1])) * PIXEL_TO_FEET
        h = np.linalg.norm(np.array(points[1]) - np.array(points[2])) * PIXEL_TO_FEET
        return f"Rectangle Area: {w*h:.2f} ft²"

    elif shape == "circle" and len(points) >= 2:
        r = np.linalg.norm(np.array(points[0]) - np.array(points[1])) * PIXEL_TO_FEET
        return f"Circle Area: {np.pi * r * r:.2f} ft²"

    elif shape == "square" and len(points) >= 4:
        sides = [np.linalg.norm(np.array(points[i]) - np.array(points[i+1])) * PIXEL_TO_FEET for i in range(3)]
        side = np.mean(sides)
        return f"Square Area: {side*side:.2f} ft²"

    return ""

def undo_action():
    """Undo last action."""
    global selected_points, lines, undo_stack
    if not undo_stack:
        return
    action, data = undo_stack.pop()
    if action == 'add_point' and data in selected_points:
        selected_points.remove(data)
    elif action == 'add_line' and data in lines:
        lines.remove(data)

# main program starting from here 
print("⚠ Paste your IP URL (e.x. http://192.168.0.8:8080)")
url = input("📷 Camera URL (leave blank for default webcam): ")

if url.strip() == "":
    print("👉 Using default webcam...")
    url = 0
else:
    if not url.endswith("/video"):
        url = url.rstrip("/") + "/video"

cap = cv2.VideoCapture(url)

# if camera or ip could not be work properly it will print this  
if not cap.isOpened():
    print("❌ Could not open video stream. Make sure:")
    print("1️⃣ Phone & PC are on same Wi-Fi")
    print("2️⃣ Correct IP/Port entered")
    print("3️⃣ /video is added at the end")
    exit()

cv2.namedWindow("Object Measurement")
cv2.setMouseCallback("Object Measurement", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠ Failed to grab frame.")
        break

    draw_buttons(frame)


    for p in selected_points:
        cv2.circle(frame, p, 5, (0, 0, 255), -1)

   
    for l in lines:
        cv2.line(frame, l[0], l[1], (0, 255, 0), 2)

    # show distance
    if len(selected_points) == 2:
        distances = calculate_distance(selected_points[0], selected_points[1])
        y_pos = 80
        for unit, val in distances.items():
            cv2.putText(frame, val, (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            y_pos += 30

    # show area
    if current_shape:
        area_text = calculate_area(selected_points, current_shape)
        if area_text:
            cv2.putText(frame, area_text, (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Object Measurement", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()