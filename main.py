import os
import pickle

import cv2
import face_recognition
import sys

def detect_person_in_video():
    data = pickle.loads(open("person_encodings.pickle", "rb").read())
    #video = cv2.VideoCapture('videos.mp4')
    video = cv2.VideoCapture(0)

    count = 0

    if not os.path.exists("frames"):
        os.mkdir("frames")

    while True:
        ret, image = video.read()

        fps = video.get(cv2.CAP_PROP_FPS)
        multiplier = fps * 3

        # if ret:
        #     image_id = int(round(video.get(1)))
        #     multiplier = int(round(video.get(1))) # если нужно по кадрово пишем  multiplier = int(round(cap.get(1)))
        #     #print(f"frame_id = {frame_id}, multiplier = {multiplier}")
        #     #cv2.imshow("frame", image)
        #
        #     if image_id % multiplier == 0:
        #         cv2.imwrite(f"frames/{count}.jpg", image)
        #         print(f"Take a screenshot {count}")
        #         count += 1
        #
        # else:
        #     print("[Error] Can't get the frame...")
        #     break

        #video.release()

        locations = face_recognition.face_locations(image, model="hog") #на процессорах hog, на видеокартрах cnn
        encodings = face_recognition.face_encodings(image, locations)

        kolichestvo_v_slovare = int(len(data)/2)

        for x in range(kolichestvo_v_slovare):          

            for face_encoding, face_location in zip(encodings, locations):
                result = face_recognition.compare_faces(data[f"encodings_{x}"], face_encoding)
                match = None

                if True in result:
                    match = data[f"person_{x}"]
                    print(f"Это {match}!")

                    image_id = int(round(video.get(1)))
                    multiplier = int(
                        round(video.get(1)))  # если нужно по кадрово пишем  multiplier = int(round(cap.get(1)))
                    # print(f"frame_id = {frame_id}, multiplier = {multiplier}")
                    # cv2.imshow("frame", image)

                    left_top = (face_location[3], face_location[0])
                    right_bottom = (face_location[1], face_location[2])
                    color = [0, 255, 0]
                    cv2.rectangle(image, left_top, right_bottom, color, 4)

                    left_bottom = (face_location[3], face_location[2])
                    right_bottom = (face_location[1], face_location[2] + 20)
                    cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)

                    cv2.putText(
                        image,
                        match,
                        (face_location[3] + 10, face_location[2] - 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        4
                    )

                    if multiplier == 0:
                        multiplier = 1
                    if image_id % multiplier == 0:
                        cv2.imwrite(f"frames/{count}.jpg", image)
                        print(f"Take a screenshot {count}")
                        count += 1


                left_top = (face_location[3], face_location[0])
                right_bottom = (face_location[1], face_location[2])
                color = [0, 255, 0]
                cv2.rectangle(image, left_top, right_bottom, color, 4)

                left_bottom = (face_location[3], face_location[2])
                right_bottom = (face_location[1], face_location[2] + 20)
                cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
                cv2.putText(
                    image,
                    match,
                    (face_location[3] + 10, face_location[2] + 15),
                     cv2.FONT_HERSHEY_SIMPLEX,
                     1,
                     (255, 255, 255),
                     4
                )

            cv2.imshow("detect_person_in_video is running", image)

            k = cv2.waitKey(33)

        if k == ord("q"):
            print("Выход из программы")
            break




def main():
    detect_person_in_video()

if __name__ == '__main__':
    main()