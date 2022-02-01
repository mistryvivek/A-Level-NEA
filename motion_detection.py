"""# Import needed libraries.
import cv2
import argparse
import imutils

# Create a new function which looks for changes in frame.
def frame_calculation(difference):


        return True



    # Calculate the difference in frames.
    difference = cv2.subtract(old_frame_prep, new_frame_prep)
    # Looks at the differences for each part of the BGR channels.
    blue, green, red = cv2.split(difference)
    # Counts the pixels that aren`t zero.
    blue_non_match = cv2.countNonZero(blue)
    green_non_match = cv2.countNonZero(green)
    red_non_match = cv2.countNonZero(red)
    # Find out the total number of pixels on the frame and
    # compare it to that.
    dimensions = new_frame_prep.shape
    total_pixels = dimensions[0] * dimensions[1]
    percentage_difference = (green_non_match + blue_non_match + red_non_match) / (total_pixels * 3)
    # Returns the value depending on the logical operator.
    if percentage_difference > 0.3:
        return True
    else:
        return False
    #Save to see difference.
    cv2.imwrite("lft_blur.jpg",old_frame_prep)
    cv2.imwrite("castle_blur.jpg",new_frame_prep)


# frame_calculation("Background One.jpg","Background Two.jpg")

counter = 0


def main():
    # Identifies video source.
    source = cv2.VideoCapture(0)

    # Set needed variables.
    changed_frame = False

    # Loop until motion is detected.
    while changed_frame == False:
        # Get each frame.
        info, frame = source.read()

        # Puts text on frame.
        frame = cv2.putText(frame, "PIN ENTRY SUCCESSFUL", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1,
                            cv2.LINE_AA)
        frame = cv2.putText(frame, "Press 'q' to exit.", (550, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1,
                            cv2.LINE_AA)

        # Display frame.
        cv2.imshow("Motion Tracking Has been activated", frame)

        # If the q key is pressed exit loop.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            changed_frame = True

        # Convert to grey scale and blur it.
        new_frame_prep = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_frame_prep = cv2.GaussianBlur(new_frame_prep, (21, 21), 0)

         new_frame_prep = cv2.GaussianBlur(frame, (5, 5), 0)
        new_frame_prep = cv2.cvtColor(new_frame_prep,cv2.COLOR_BGR2GRAY)
        _, new_frame_prep = cv2.threshold(new_frame_prep,140,255,cv2.THRESH_BINARY_INV)

        try:
            difference = cv2.absdiff(frame,old_frame)
            # Find the background difference.
            grey_comparision = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
            blur_comparision = cv2.GaussianBlur(grey_comparision, (5, 5), 0)
            _, thresh = cv2.threshold(blur_comparision, 20, 255, cv2.THRESH_BINARY)
            dilated_comparision = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated_comparision, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 900:
                    continue
                print("motion")
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            image = cv2.resize(frame, (1280, 720))
            cv2.imshow("feed",frame)
            old_frame = frame

        except:
            pass

    # Closes all openCV windows.
    cv2.destroyAllWindows()


main()
"""

# Imported needed library.
import cv2
from datetime import datetime


# This function looks for a change in frame.
def change_in_frame(frame1, frame2):
    # Finds the absolute difference of the frame.
    difference = cv2.absdiff(frame1, frame2)
    # Blurs and turns the image into grey scale.
    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    blur_difference = cv2.GaussianBlur(gray_difference, (5, 5), 0)
    # Dilates and finds the threshold.
    _, thresh = cv2.threshold(blur_difference, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # Finds contours in images.
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Looks through list of contours and decided whether they are too big or not.
    for contour in contours:
        if cv2.contourArea(contour) < 900:
            continue
        return True


# Main function which links all code.
def main():
    # Find out time when the program was first ran.
    start_time = datetime.now()
    # Load webcam.
    source = cv2.VideoCapture(0)

    # Load first two frames.
    ret, frame1 = source.read()
    ret, frame2 = source.read()

    # Set boolean variable.
    constant_frame = True

    # Define the codec and create VideoWriter object
    output_settings = cv2.VideoWriter_fourcc(*'DIVX')
    output = cv2.VideoWriter('output.mp4', output_settings, 20.0, (640, 480))

    # Until frame is not constant.
    while constant_frame:
        # Add frame to capture.
        output.write(frame1)
        # Puts text on frame.
        frame_to_display = frame1
        frame_to_display = cv2.putText(frame_to_display, "PIN ENTRY SUCCESSFUL", (10, 450), cv2.FONT_HERSHEY_SIMPLEX,
                                       0.25,
                                       (0, 0, 255), 1,
                                       cv2.LINE_AA)
        frame_to_display = cv2.putText(frame_to_display, "Press 'q' to exit.", (550, 450), cv2.FONT_HERSHEY_SIMPLEX,
                                       0.25,
                                       (0, 0, 255), 1,
                                       cv2.LINE_AA)

        # Display window.
        cv2.imshow("Motion Tracking Has been activated", frame_to_display)

        # Gets next frame and saves the previous one/
        frame1 = frame2
        ret, frame2 = source.read()

        # Change variable depends on calculations
        if change_in_frame(frame1, frame2):
            # Finds the time difference.
            time_elapsed = datetime.now() - start_time
            # If the time difference is larger then 20 seconds , the next steps can be done.
            if time_elapsed.seconds > 20:
               #print("MOTION")
                # Record time of motion if the variable isn`t already taken.
               try:
                   test_variable = time_of_motion
               except:
                   time_of_motion = datetime.now()

        #Try to calculate the time since motion if it has been recorded.
        try:
            time_since_motion = datetime.now() - time_of_motion
            #print(time_since_motion)
            if time_since_motion.seconds > 20:
                constant_frame = False

        except:
            pass



        # If the q key is pressed exit loop.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Close OpenCV Window.
    cv2.destroyAllWindows()
