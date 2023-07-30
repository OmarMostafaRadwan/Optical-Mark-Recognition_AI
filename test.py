import os
import cv2
import json

def apply_roi_and_show_images(folder_name, roi_list):
    # Get a list of image file names in the specified folder
    image_files = sorted([f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))])


    # Iterate through each image file and apply the ROI
    for image_file in image_files:
        image_path = os.path.join(folder_name, image_file)
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        try:
            image = cv2.resize(image,(1000,1000),interpolation=cv2.INTER_AREA)
        except:
            pass
        # Apply the ROI on the image
        for roi in roi_list:
            # Extract ROI coordinates
            x, y, width, height = roi
            # Draw a rectangle on the image to represent the ROI
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
        
        # Show the image with the ROI applied
        cv2.imshow("Image with ROI", image)
        
        # Wait for a key press (0 means wait indefinitely)
        cv2.waitKey(0)
        
        # Close the image window after a key press
        cv2.destroyAllWindows()

# Example usage:
folder_name = "scan"

with open('roi.json', 'r') as f:
            ROI_list = json.load(f)
            roi_list = []
            for roi in ROI_list:
                roi_list.append(roi[0])
            print(roi_list)


apply_roi_and_show_images(folder_name, roi_list) 
