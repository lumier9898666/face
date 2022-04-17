import os
import pickle
import sys
import face_recognition
from cv2 import cv2

import time





def train_model_by_img(name):

    # if not os.path.exists("dataset"):
    #     os.mkdir("dataset")
    #     print("Созданна директория dataset")

    know_encodings = []
    images = os.listdir(f"{name}")

    kol = 0



    #print(images)

    for (i, image) in enumerate(images):

        tic = time.perf_counter()

        kol += 1 

        print(f"[+] processing img {i + 1}/{len(images)}")
        print(image)

        face_img = face_recognition.load_image_file(f"{name}/{image}")
        face_enc = face_recognition.face_encodings(face_img)[0]

        toc = time.perf_counter()
        print("количество итераций" , kol)
        print(f"Вычисление заняло {toc - tic:0.4f} секунд")

        #print(face_enc)

        if len(know_encodings) == 0:
            know_encodings.append(face_enc)
        else:
            for item in range(0, len(know_encodings)):
                result = face_recognition.compare_faces([face_enc], know_encodings[item])
                print(result)

                if result[0]:
                    know_encodings.append(face_enc)
                    #print("Same person!")
                    break
                else:
                    #print("Another person!")
                    break



    #print(know_encodings)
    #print(f"Lenght {len(know_encodings)}")

    # data = {
    #     "name": name,
    #     "encodings": know_encodings
    # }

    #print(data)

    #with open(f"person_encodings.pickle", "ab") as file:
     #   file.write(pickle.dumps(data))


 

    return know_encodings

   # return f"[INFO] File person_encodings.pickle successfull"



def take_screenshot_from_video():
    cap = cv2.VideoCapture(0)
    count = 0

    if not os.path.exists("dataset_from_video"):
        os.mkdir("dataset_from_video")

    while True:
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        multiplier = fps * 3
        #print(fps)

        if ret:
            frame_id = int(round(cap.get(1)))
            multiplier = int(multiplier) # если нужно по кадрово пишем  multiplier = int(round(cap.get(1)))
            #print(f"frame_id = {frame_id}, multiplier = {multiplier}")
            cv2.imshow("frame", frame)
            k = cv2.waitKey(20)

            if frame_id % multiplier == 0:
                cv2.imwrite(f"dataset_from_video/{count}.jpg", frame)
                print(f"Take a screenshot {count}")
                count += 1

            if k == ord(" "):
                cv2.imwrite(f"dataset_from_video/{count}.jpg", frame)
                print(f"Take an extra screenshots {count}")
                count += 1

            elif k == ord("q") or k == ord("й") or k == ord("Й"):
                print("Выход из программы")
                break

        else:
            print("[Error] Can't get the frame...")
            break
    cap.release()
    cv2.destroyAllWindows()



def main():
    result = []
    obsh = {}
    kolichestvo_ludey = int(input("Введите количество людей\n"))
    for x in range(kolichestvo_ludey):
        name = input("Введите имя\n")
        result = train_model_by_img(name)

        data = {
            f"person_{x}": name,
            f"encodings_{x}": result  
        }


        obsh.update(data)

    with open(f"person_encodings.pickle", "wb") as file:
        file.write(pickle.dumps(obsh))


        
    
    #take_screenshot_from_video()

    # print(obsh)


if __name__ == '__main__':
    main()