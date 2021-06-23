import cv2, time, pandas
from datetime import datetime


first_frame = None #creating a var with None as the value, so when it's used later, python will know it exists

status_list = [None, None]

times = []

df = pandas.DataFrame(columns = ["Start", "End"])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW) #method to capture video from camera. 0 is for one camera. 1 would be two cameras, etc
#if using a saved video, pass the file path instead
#needed to add cv2.CAP_DSHOW because of a bug in cv2 library. not usually needed


while True: #setting while loop to true makes the loop run until it's broken
    check, frame = video.read() #check is a bool data type
    status = 0 #setting a variable(status) to 0 for the first frame, when there's no movement
    #check is checking to make sure video is running. If true, create frame for video with read method
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #change frame to grayscale
    gray = cv2.GaussianBlur(gray, (21,21), 0)#blurs the image to make it smoother for reading movement
    #pass image to blur(gray) and width and height of blur(21,21)

    if first_frame is None:
        first_frame = gray #assign gray var to first_frame in the very first loop since first_frame is None
        #after the loop has run once though, first_frame will be equal to gray variable, so this condition will not be true
        continue #start the while loop over if first_frame is None and don't run rest of code in loop

    delta_frame = cv2.absdiff(first_frame, gray) #comparing first_frame image and gray image
    #this will create another image and set it to delta_frame var

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    #.threshold() returns a tuple with 2 values. We need to specify that we need the second(index 1) value of this tuple
    #which is the actual frame we are creating(thresh_delta) 255 sets value to white. 30 is threshold limit
    #if value in array is 30 or greater, make it white in the frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #finding all contours in the thresh_frame image and assigning it to cnts
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
    #if contour area of a contour found in thresh_frame is less than 10000, go to next contour and don't run following code
        status = 1 #changing status var to one when movement is detected

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 3)
        #draw rectangle on frame with the coords of upper left point and lower right point of face

    status_list.append(status) #appending status to the empty list status_list

    status_list = status_list[-2:] #changing status_list to just last two items of the list

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now()) #when status changes from 0 to 1(movement detected), append the datetime to times list
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now()) #when status changes from 1 to 0(movement stops), append datetime to times list


    cv2.imshow("Gray Frame", gray) #creating window with gray variable showing in it
    cv2.imshow("Delta Frame", delta_frame)#create window for delta_frame image
    cv2.imshow("Delta Threshold", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1) #one millisecond, then the loop starts over
    #This while loop basically creates an image from the webcam every millisecond and shows it in the imshow window.
    #Images will keep showing in the window until q is pressed and the loop is broken

    if key == ord('q'): #break while loop if key is 'q'(if q key is pressed)
        if status == 1:
            times.append(datetime.now()) #if window is closed while there is movement, it will append that time to the list too
        break
#ord returns the unicode value of a one-character string(q). If that value is equal to key variable, break loop.
#So if q is pressed, break loop and continue on to rest of python code below

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index= True)

df.to_csv("Times.csv") #create a csv file and export df to it

video.release() #releasing camera. stopping the camera. Put after waitKey, so video isn't released before button is pressed
cv2.destroyAllWindows()#close window when button is pressed