# import cv2
# import numpy as np

# def get_row_image(img, num_columns, num_rows, row_number, roi):
#     # Convert the image to a NumPy array
#     img_np = np.array(img)

#     # Extract the ROI coordinates
#     left, top, width, height = roi
#     # Crop the image to the selected ROI
#     roi_img = img_np[top:top + height, left:left + width]

#     # Calculate the width and height of each bubble
#     bubble_width = width // num_columns
#     bubble_height = height // num_rows

#     # Calculate the y-coordinate range for the specific row
#     row_number = row_number - 1
#     row_start = row_number * bubble_height
#     row_end = row_start + bubble_height

#     # Extract the specific row image from the ROI
#     row_image = roi_img[row_start:row_end, :]
#     return row_image

# def grade_bubble_sheet(image_with_roi, answer_key, num_columns, num_rows, roi):
#     score = 0

#     # Load the image with ROI applied
#     img = cv2.imread(image_with_roi)

#     for row_num, correct_answer in enumerate(answer_key, start=1):
#         # Get the row image for the current row number
#         row_image = get_row_image(img, num_columns, num_rows, row_num, roi)

#         # Calculate the score for the current row
#         # (You may use any method to compare the row_image with correct_answer)
#         # For example, you could use OCR or template matching to recognize the marked bubble.

#         # Here, I'm assuming that correct_answer is an integer representing
#         # the correct answer for the current row, and we are comparing it with the selected option in the row_image.
#         # You'll need to adapt this part depending on how you want to compare the answer.

#         # Sample comparison assuming correct_answer is an integer.
#         selected_option = None  # TODO: Extract the selected option from row_image
#         if selected_option == correct_answer:
#             row_score = 1
#         else:
#             row_score = 0

#         score += row_score

#     return score

# # Example usage:
# if __name__ == "__main__":
#     # Assuming you have an image with ROI applied and an answer key
#     image_with_roi_path = "scan/1685500.tif"
#     answer_key = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1]  # Correct answers for each row in the bubble sheet
#     num_columns = 4  # Number of columns in the bubble sheet
#     num_rows = 19   # Number of rows in the bubble sheet
#     roi = [604, 380, 208, 575]  # ROI coordinates
#     score = grade_bubble_sheet(image_with_roi_path, answer_key, num_columns, num_rows, roi)
#     print("Score:", score)



import cv2

def draw_bubble_boxes(image_path,roi,num_columns,num_rows):
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.resize(img,(1000,1000),interpolation=cv2.INTER_AREA)
    # Allow the user to select the Region of Interest (ROI)
    # roi = cv2.selectROI("Select ROI", img, fromCenter=False, showCrosshair=True)
    # cv2.destroyWindow("Select ROI")

    # Extract the ROI coordinates
    x, y, w, h = roi

    # Crop the image to the selected ROI
    roi_img = img[y:y+h, x:x+w]

    # Ask the user to enter the number of columns and rows
    # num_columns = int(input("Enter the number of columns: "))
    # num_rows = int(input("Enter the number of rows: "))

    # Calculate the width and height of each bubble
    bubble_width = w // num_columns
    bubble_height = h // num_rows

    # Draw boxes (rectangles) around the bubbles
    for row in range(num_rows):
        for col in range(num_columns):
            x1 = col * bubble_width
            y1 = row * bubble_height
            x2 = x1 + bubble_width
            y2 = y1 + bubble_height
            cv2.rectangle(roi_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Show the final image with boxes
    cv2.imshow("Bubble Sheet with Boxes", roi_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = "scan/1685500.tif"
    roi = [604, 380, 208, 575]  # ROI coordinates
    num_columns = 4  # Number of columns in the bubble sheet
    num_rows = 19   # Number of rows in the bubble sheet
    draw_bubble_boxes(image_path,roi,num_columns,num_rows)
