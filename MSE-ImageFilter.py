import os
from PIL import Image
import numpy as np
import time
import asyncio

sep = os.path.sep

def compareImage(imageFile, imageName, path=os.path.dirname(__file__)):
    global smallest, img1, c
    image1 = np.array(imageFile)
    i1shape = np.shape(imageFile)
    compared = dict()
    smallest = 200
    sameIMG = dict()
    filesize = os.stat(path + sep + imageName).st_size
    samesize = dict()
    print("new image")
    samesize[imageName] = filesize
    for i2 in os.listdir(path):
        size = os.stat(path + sep + i2).st_size
        if os.path.isdir(path + sep + str(i2)):
            continue
        if size != samesize[imageName]:
            continue
        if size == samesize[imageName]:
            samesize[i2] = size
            continue

    for item in samesize:
        image2 = Image.open(path + sep + item)
        i2shape = np.shape(image2)
        if i2shape != i1shape:
            continue
        image2 = np.array(image2)
        Result = mse(image1, image2)
        if Result is None:
            continue
        compared[item] = Result
        print("Anzahl in Compared: " + str(len(compared)))
    for item in compared:
        if compared[item] < smallest:
            smallest = compared[item]
        if compared[item] > smallest:
            continue
    if smallest < 199: # This Value gave the best Result during the Creatiion of this Script 
        for item in compared:
            if compared[item] <= smallest:
                sameIMG[item] = compared[item]
        if len(sameIMG) >= 1:
            img1 = sameIMG[imageName]

        if len(sameIMG) > 1:
            c = 0
            for g in range(0, len(sameIMG) - 2):
                if list(sameIMG)[g] in samesize:
                    try:
                        os.remove(path + sep + str(list(sameIMG)[g]))
                        c = c + 1
                        continue
                    except:
                        print("Image couldnt be deleted")
                        continue
                else:
                    continue
            print(str(c) + " Images deleted")
            # await asyncio.sleep(2)
    if smallest >= 200:
        print("Comparing stopped")
        # await asyncio.sleep(2)


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = None
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    # err 0 == the Same
    return err

if __name__ == "__main__":
    pass
