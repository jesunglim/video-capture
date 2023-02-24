# -*- coding: utf-8 -*-
# @author : Jesung Lim (jesunglimkorea@gmail.com)
import argparse
import os
import cv2
from pandas import Series, DataFrame


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def video_capture(vidpath, frame_cut, name, gaussian, comp_res, out_res, original_dir, blur_dir, vidcnt, vidlen, list4k, list1080p):
    vidcap = cv2.VideoCapture(vidpath)
    count = 0

    while(vidcap.isOpened()):
        ret, image = vidcap.read()

        if ret:
            if int(vidcap.get(1)) % frame_cut == 0:
                image = cv2.resize(image, (3840,2160))
                cv2.imwrite("{}{}{}.jpg".format(original_dir, name, count), image)  # 4k image

                if gaussian == "None":
                    image_blur = cv2.resize(image, comp_res)
                    image_blur = cv2.resize(image_blur, out_res)
                else:
                    try:
                        g_num = int(gaussian)
                        image_blur = cv2.GaussianBlur(image,(0,0), g_num)
                        image_blur = cv2.resize(image_blur, out_res)
                    except:
                        print("\n\n[ only support positive number! ]\n\n")

                cv2.imwrite("{}{}{}.jpg".format(blur_dir, name, count), image_blur, [cv2.IMWRITE_JPEG_QUALITY, 40])  # 1080p image & compress
                print("{}{}({}) saved. [{}/{}]".format(blur_dir, name, count, vidcnt, vidlen))

                list4k.append( "{}{}{}.jpg".format(original_dir, name, count) )
                list1080p.append( "{}{}{}.jpg".format(blur_dir, name, count) )

                count += 1
        else:
            return list4k, list1080p

    vidcap.release()


def video_capture_split(vidpath, frame_cut, split_num, name, dirFHD, vidcnt, vidlen, listFHD):
    vidcap = cv2.VideoCapture(vidpath)
    count = 0


    if split_num == "4":
        while(vidcap.isOpened()):
            ret, image = vidcap.read()

            if ret:
                if int(vidcap.get(1)) % frame_cut == 0:
                    image = cv2.resize(image, (3840,2160))
                    
                    h,w,c = image.shape
                    # 원하는 영역을 자르기 위해서는 [ startY:endY, startX:endX ] 
                    # 이거 뭔가 이상해서 나중에 수정해야 할 수도 있음
                    # img = img[Y:hY, X:wX] 이게 맞음
                    quadrant1 = image[0:int(h/2), int(w/2):w]
                    quadrant2 = image[0:int(h/2), 0:int(w/2)]
                    quadrant3 = image[int(h/2):h, 0:int(w/2)]
                    quadrant4 = image[int(h/2):h, int(w/2):w]

                    quadrant1 = cv2.resize(quadrant1, (int(w/2),int(h/2)) )  # check FHD size
                    quadrant2 = cv2.resize(quadrant2, (int(w/2),int(h/2)) )  # if UHD = (1920,1080)
                    quadrant3 = cv2.resize(quadrant3, (int(w/2),int(h/2)) )
                    quadrant4 = cv2.resize(quadrant4, (int(w/2),int(h/2)) )

                    cv2.imwrite("{}{}{}{}.jpg".format(dirFHD, name,"_1_", count), quadrant1) 
                    cv2.imwrite("{}{}{}{}.jpg".format(dirFHD, name,"_2_", count), quadrant2)
                    cv2.imwrite("{}{}{}{}.jpg".format(dirFHD, name,"_3_", count), quadrant3)
                    cv2.imwrite("{}{}{}{}.jpg".format(dirFHD, name,"_4_", count), quadrant4)

                    print("{}({}) saved. [{}/{}]".format(name, count, vidcnt, vidlen))
                    listFHD.append( "{}{}{}{}.jpg".format(dirFHD, name,"_1_", count) )  # append file location list
                    listFHD.append( "{}{}{}{}.jpg".format(dirFHD, name,"_2_", count) )
                    listFHD.append( "{}{}{}{}.jpg".format(dirFHD, name,"_3_", count) )
                    listFHD.append( "{}{}{}{}.jpg".format(dirFHD, name,"_4_", count) )

                    count += 1
            else:
                return listFHD
        vidcap.release()

    else:
        print("can't divide this number")


def nomal_main(path, frame, gaussian, compres, outres):
    vidpath = path
    savepath = "./imgs/"
    frame_cut = frame      # capture per frame
    comp_res = compres     # compress resolution
    out_res = outres       # output resolution

    make_dir(savepath)
    make_dir(savepath + "original/")
    make_dir(savepath + "blur/")

    original_dir = os.path.join(savepath, "original/")
    blur_dir = os.path.join(savepath, "blur/")

    videos = os.listdir(vidpath)
    vidlen = len(videos)
    vidcnt = 1

    list4k = []
    list1080p = []

    for i in videos:
        print("now capture [{}]".format(i))
        i_path = os.path.join(vidpath, i)
        name = str(i.split('.')[0])
        l4k, l1080p = video_capture(i_path, frame_cut, name, gaussian, comp_res, out_res, original_dir, blur_dir, vidcnt, vidlen, list4k, list1080p)

        vidcnt += 1


    df = {'4k': list4k,
        '1080p': list1080p}
    df = DataFrame(df)
    df.to_csv("dir.csv")
    print("csv save done!")


def split_main(path, frame, split_num):
    vidpath = path
    savepath = "./imgs/"
    frame_cut = frame      # capture per frame

    make_dir(savepath)
    make_dir(savepath + "FHD/")

    dirFHD = os.path.join(savepath, "FHD/")

    videos = os.listdir(vidpath)
    vidlen = len(videos)
    vidcnt = 1

    listFHD = []

    for i in videos:
        print("now capture [{}]".format(i))
        i_path = os.path.join(vidpath, i)
        name = str(i.split('.')[0])
        l4k = video_capture_split(i_path, frame_cut, split_num, name, dirFHD, vidcnt, vidlen, listFHD)

        vidcnt += 1



def main(path, frame, split_num, gaussian, compres, outres):

    if split_num == "None":
        nomal_main(path, frame, gaussian, compres, outres)
    else:
        split_main(path, frame, split_num)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Dataset for Super Resolution")
    parser.add_argument('--path', default="C:\\Users\\jesung\\Videos\\4k", type=str, help="PATH of videos to capture")
    parser.add_argument('--frame', default=6, type=int, help="Capture per Frame")
    parser.add_argument('--split_num', default="None", type=str, help="numbers of divide screen")  # support : None, 4
    parser.add_argument('--gaussian', default="3", type=str, help="Low Resolution made with Gaussian Blur") # support : None, any positive number [recommend 1~3]

    parser.add_argument('--compres', default=(1280,720), type=tuple, help="compress resolution")
    parser.add_argument('--outres', default=(1920,1080), type=tuple, help="output resolution")

    args = parser.parse_args() 

    main(args.path, args.frame, args.split_num, args.gaussian, args.compres, args.outres)
