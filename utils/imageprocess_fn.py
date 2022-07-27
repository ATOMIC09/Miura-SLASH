import cv2
import numpy as np
import qrcode
import math
from utils import deepfryer_fn
from petpetgif import petpet

def imginfo_channel(path):
    image = cv2.imread(path,cv2.IMREAD_UNCHANGED)
    try:
        # Save the transparency channel alpha
        b_channel, g_channel, r_channel , alpha = cv2.split(image)
        img_RGBA = cv2.merge((b_channel, g_channel, r_channel, alpha))
    except:
        # If have no alpha channel
        b_channel, g_channel, r_channel = cv2.split(image)
        img_RGBA = cv2.merge((b_channel, g_channel, r_channel))

    height, width, channels = img_RGBA.shape
    if channels == 1:
        return "Grayscale"
    elif channels == 2:
        return "Grayscale Alpha"
    elif channels == 3:
        return "RGB"
    elif channels == 4:
        return "RGBA"

def imginfo_height(path):
    image = cv2.imread(path,cv2.IMREAD_UNCHANGED)

    height, width, channels = image.shape
    return height

def imginfo_width(path):
    image = cv2.imread(path,cv2.IMREAD_UNCHANGED)

    height, width, channels = image.shape
    return width
    
def grayscale(path):
    img = cv2.imread(path,cv2.IMREAD_UNCHANGED)

    # Save the transparency channel alpha
    *_, alpha = cv2.split(img)

    gray_layer = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.merge((gray_layer, gray_layer, gray_layer, alpha))
    
    cv2.imwrite(path,img)

def colorize(path):
    net = cv2.dnn.readNet("asset/colorize/model/colorization_deploy_v2.prototxt", "asset/colorize/model/colorization_release_v2.caffemodel")
    pts = np.load("asset/colorize/model/pts_in_hull.npy")

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    image = cv2.imread(path)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    colorized = (255 * colorized).astype("uint8")

    cv2.imwrite(path, colorized)

def removebg(path):
    # load image
    img = cv2.imread(path)

    # convert to graky
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold input image as mask
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # negate mask
    mask = 255 - mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # save resulting masked image
    cv2.imwrite(path, result)

def qr(text):
    img = qrcode.make(text)
    img.save("temp/autosave/miura_qr.png")

def wide(path,stretch):
    image = cv2.imread(path,cv2.IMREAD_UNCHANGED)
    try:
        # Save the transparency channel alpha
        b_channel, g_channel, r_channel , alpha = cv2.split(image)
        img_RGBA = cv2.merge((b_channel, g_channel, r_channel, alpha))
    except:
        # If have no alpha channel
        b_channel, g_channel, r_channel = cv2.split(image)
        img_RGBA = cv2.merge((b_channel, g_channel, r_channel))

    height, width, channels = img_RGBA.shape
    size = (math.ceil(width*2), math.ceil(height/stretch))

    res = cv2.resize(img_RGBA, size)
    cv2.imwrite(path,res)

def deepfry(path):
    imageNormal = cv2.imread(path)
    deepfryer_fn.printFolders("asset/deepfry/deepfryer_input", "asset/deepfry/deepfryer_output")
    deepfryer_fn.processArgs()
    deepfryer_fn.fryImage(path)
    deepfryer_fn.badPosterize(imageNormal)

    if "_deepfryer" in path:
        deepfryer_fn.folderCheck("asset/deepfry/deepfryer_input", "asset/deepfry/deepfryer_output", '.png')
    else:
        deepfryer_fn.folderCheck("asset/deepfry/deepfryer_input", "asset/deepfry/deepfryer_output", '_deepfryer.png')

def petpet_def(path,filename):
    petpet.make(path, f'temp/autosave/{filename}_petpet.gif')

def scale(path,scale):
    image = cv2.imread(path)
    height, width, channels = image.shape
    size = (math.ceil(width*scale/100), math.ceil(height*scale/100))
    res = cv2.resize(image, size)
    cv2.imwrite(path,res)

def resize(path,width,height):
    img = cv2.imread(path)
    resized = cv2.resize(img, (width, height))
    cv2.imwrite(path,resized)

def text(path,text,font,color,size,position,thickness):
    img = cv2.imread(path)
    
    # กำหนดตำแหน่งให้อยู่ตรงกลาง
    textsize = (cv2.getTextSize(text, font, size, thickness)[0])
    textX = int((img.shape[1] - textsize[0]) / 2)
    textY = int((img.shape[0] + textsize[1]) / position)

    cv2.putText(img, text, (textX, textY), font, size, color, thickness)
    cv2.imwrite(path,img)