import cv2

def get_row_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
    # Allow the user to select the Region of Interest (ROI)
    roi = cv2.selectROI("Select ROI", img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")

    # Extract the ROI coordinates
    x, y, w, h = roi
    # print(x, y, w, h)
    # Crop the image to the selected ROI
    roi_img = img[y:y+h, x:x+w]

    # Ask the user to enter the number of columns and rows
    num_columns = int(input("Enter the number of columns: "))
    num_rows = int(input("Enter the number of rows: "))

    # Calculate the width and height of each bubble 53 207 113 407
    bubble_width = w // num_columns
    bubble_height = h // num_rows

    # Ask the user to enter the row number they want to access (0-indexed)
    row_number = int(input("Enter the row number (0-indexed): ")) - 1

    # Calculate the y-coordinate range for the specific row
    row_start = row_number * bubble_height
    row_end = row_start + bubble_height

    # Extract the specific row image from the ROI
    row_image = roi_img[row_start:row_end, :]

    return row_image

if __name__ == "__main__":
    image_path = "form.jpg"
    row_image = get_row_image(image_path)

    # Show the selected row image
    cv2.imshow("Selected Row", row_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
