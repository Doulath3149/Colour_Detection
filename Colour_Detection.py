# Import required libraries
import cv2
import pandas as pd

# File paths
img_path = 'pic1.jpg'  # Ensure this image exists in the same directory
csv_path = 'colors.csv'  # Ensure this file exists in the same directory

# Load CSV file into a DataFrame
df = pd.read_csv(csv_path, names=['color', 'color_name', 'hex', 'R', 'G', 'B'], header=None)

# Read and resize the image
img = cv2.imread(img_path)
if img is None:
    print("Error: Image not found! Check img_path.")
    exit()
img = cv2.resize(img, (800, 600))

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to find the closest color name
def get_color_name(R, G, B):
    minimum = 10000  # Set a high initial value
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# Function to handle mouse clicks
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = img[y, x]  # Get color from clicked pixel
        b, g, r = int(b), int(g), int(r)  # Convert to int
        print(f"Clicked at ({xpos}, {ypos}) - RGB({r}, {g}, {b})")  # Debugging

# Create a window and set a mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    temp_img = img.copy()  # Prevent overwriting
    if clicked:
        # Draw a rectangle to display the color name and RGB values
        cv2.rectangle(temp_img, (20, 20), (600, 60), (b, g, r), -1)

        # Get the color name
        color_name = get_color_name(r, g, b)
        text = f"{color_name} R={r} G={g} B={b}"
        
        # Choose text color based on brightness
        text_color = (255, 255, 255) if (r + g + b) < 600 else (0, 0, 0)

        # Display color name and RGB values
        cv2.putText(temp_img, text, (50, 50), 2, 0.8, text_color, 2, cv2.LINE_AA)

    cv2.imshow('image', temp_img)

    # Exit when 'ESC' is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
