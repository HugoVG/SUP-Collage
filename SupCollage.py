# ___  ___  ___  ___  ________  ________     
#|\  \|\  \|\  \|\  \|\   ____\|\   __  \    
#\ \  \\\  \ \  \\\  \ \  \___|\ \  \|\  \   
# \ \   __  \ \  \\\  \ \  \  __\ \  \\\  \  
#  \ \  \ \  \ \  \\\  \ \  \|\  \ \  \\\  \ 
#   \ \__\ \__\ \_______\ \_______\ \_______\
#    \|__|\|__|\|_______|\|_______|\|_______|
#
#    
#
#     
import numpy as np
import cv2
import time, sys
from math import *
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import datetime

#maakt een input en een output als deze niet bestaan in de DIR
def collage():
    global suppath
    global paddlepath
    global pumppath
    global finpath
    global leashpath
    global bagpath

    try:
        imSUP = cv2.imread(suppath)
    except:
        imSUP = cv2.imread("./NP Zero/nsup.jpg")

    try:
        imPaddle = cv2.imread(paddlepath)
    except:
        imPaddle = cv2.imread("./NP Zero/npaddle.jpg")

    try:
        imPump = cv2.imread(pumppath)
    except:
        imPump = cv2.imread("./NP Zero/npump.jpg")

    try:
        imBP = cv2.imread(bagpath)
    except:
        imBP = cv2.imread("./NP Zero/nBP.jpg")
    try:
        imLeash = cv2.imread(leashpath)
    except:
        imLeash = cv2.imread("./NP Zero/nleash.jpg")

    try:
        imFin = cv2.imread(finpath)
    except:
        imFin = cv2.imread("./NP Zero/nfin.jpg")


    #alle variabele moeten worden geinitaliseerd#
    heightSUP, widthSUP, channelsSUP = imSUP.shape
    heightPaddle, widthPaddle, channelsPaddle = imPaddle.shape
    heightPump, widthPump, channelsPump = imPump.shape
    heightBP, widthBP, channelsBP = imBP.shape
    heightLeash, widthLeash, channelsLeash = imLeash.shape
    heightFin, widthFin, channelsFin = imFin.shape

    ###########SUP HEIGHT#############
    MaxHeight = heightSUP
    print("Is de max hoogte " + str(MaxHeight))

    ###########PADDLE HEIGHT##########
    print( str(widthPaddle) + " Originele size")
    heightPaddleResize = ceil(MaxHeight / 100 * 80)
    heightprocentPaddle = ceil(heightPaddleResize / heightPaddle * 100)
    widthPaddleResize =  ceil(widthPaddle / 100 * heightprocentPaddle)
    print( str(widthPaddleResize) + " Width paddle resize" )
    print( str(heightprocentPaddle) + " verkleining procent" )
    print( str(heightPaddleResize) + " Height paddle resize")
    Paddleresize = cv2.resize(imPaddle, (widthPaddleResize, heightPaddleResize))

    #empty space above paddle
    heightblank = MaxHeight - heightPaddleResize
    print(str(heightblank) + " is blank height")
    blank_image = np.zeros((heightblank,widthPaddleResize,3), np.uint8)
    blank_image.fill(255)

    #Stackt wit boven paddle met paddle img#
    paddle = np.vstack((blank_image, Paddleresize))

    #plakt sup en paddle aan elkaar#
    SUP_Paddle = np.hstack((imSUP, paddle))

    #############################################################################
    #           Deel 2 Backpack and Pump                                        #
    #############################################################################
    
    maxwidthD2 = ceil(widthSUP + widthPaddleResize)
    print(str(maxwidthD2) + " width voor deel 2")

    ##########Back Pack############################
    heightBPResize = floor(MaxHeight / 100 * 35)
    print((str(heightBPResize) + " height BP"))
    heightprocentBP = ceil(heightBPResize / heightBP * 100)
    widthBPResize =  ceil(widthBP / 100 * heightprocentBP)
    print((str(widthBPResize) + " width BP"))
    #############Pump#################################
    heightPumpResize = floor(MaxHeight / 100 * 35)
    print((str(heightPumpResize) + " height pump resize"))
    heightprocentPump = ceil(heightPumpResize / heightPump * 100)
    widthPumpResize = ceil(widthPump / 100 * heightprocentPump)
    print((str(widthPumpResize) + " width BP"))
    
    if widthBPResize > maxwidthD2:
        BPResize = cv2.resize(imBP,(maxwidthD2, heightBPResize))
        BlankwidthBP = 0
    else:
        BPResize = cv2.resize(imBP,(widthBPResize, heightBPResize))
        BlankwidthBP = ceil(maxwidthD2 - widthBPResize)
    if widthPumpResize > maxwidthD2:
        PumpResize = cv2.resize(imPump, (maxwidthD2, heightPumpResize))
        blankwidthPUMP = 0
    else:
        PumpResize = cv2.resize(imPump, (widthPumpResize, heightPumpResize))
        blankwidthPUMP = ceil(maxwidthD2 - widthPumpResize)
    
    print(str(blankwidthPUMP) + " Blank width Pump")
    blank_imagePump = np.zeros((heightPumpResize,blankwidthPUMP,3), np.uint8)
    blank_imagePump.fill(255)

    Pump = np.hstack(( blank_imagePump, PumpResize))

    print(str(BlankwidthBP) + " Blank width BP")
    blank_imageBP = np.zeros((heightBPResize,BlankwidthBP,3), np.uint8)
    blank_imageBP.fill(255)

    Backpack = np.hstack(( blank_imageBP, BPResize))

    Pump_Backpack = np.vstack((Pump, Backpack))
    
    #############################################################################
    #           Deel 3 Fin and Leash                                            #
    #############################################################################
    heightPB, widthPB, channelsPB = Pump_Backpack.shape
    print(str(heightPB) + " Height PB!!!!!!!!!!!!!!!!!!!!!!!!!!")

    ############LEASH #############################################################
    heightLeashResize = floor(MaxHeight / 100 * 10)
    heightprocentLeash = ceil(heightLeashResize / heightLeash * 100)
    widthLeashResize =  ceil(widthLeash / 100 * heightprocentLeash)
    print( str(widthLeashResize) + " Width Leash resize" )
    print( str(heightprocentLeash) + " verkleining procent" )
    print( str(heightLeashResize) + " Height Leash resize")

    if widthLeashResize > ceil(widthPB / 2):
        widthLeashResize = ceil(widthPB / 2)
        Leashresize = cv2.resize(imLeash,(widthLeashResize, heightLeashResize))
        BlankwidthFL = 0
    else:
        Leashresize = cv2.resize(imBP,(widthLeashResize, heightLeashResize))

    
    ##############FIN###########################################################################
    heightFinResize = floor(MaxHeight / 100 * 20)
    heightprocentFin = ceil(heightFinResize / heightFin * 100)
    widthFinResize =  ceil(widthFin / 100 * heightprocentFin)
    print( str(widthFinResize) + " Width Fin resize" )
    print( str(heightprocentFin) + " verkleining procent" )
    print( str(heightFinResize) + " Height Fin resize")

    if widthFinResize > floor(widthPB / 2):
        widthFinResize = floor(widthPB / 2)
        Finresize = cv2.resize(imFin,(widthFinResize, heightFinResize))
        BlankwidthFL = 0
    else:
        Finresize = cv2.resize(imBP,(widthFinResize, heightFinResize))

    ######################################################################################
    #                               Stackable                                            #
    ######################################################################################

    blank_imageLeashH = floor(heightFinResize - heightLeashResize)
    
    print( str(blank_imageLeashH) + " Blank Leash Height")
    blank_imageLeash = np.zeros((blank_imageLeashH,widthLeashResize,3), np.uint8)
    blank_imageLeash.fill(255)

    Leashresize = np.vstack((blank_imageLeash, Leashresize))

    print(str(heightLeashResize) + " Leash Height " + str(heightFinResize) + " Height fin")
    FL = np.hstack((Leashresize, Finresize))

    heightFL, widthFL, channelsFL = FL.shape
    print(str(heightFL) + " Height FL!!!!!!!!!!!!!!!!")
    print(str(widthPB) + "WIDTH PB@!@!")
    print(str(widthFL) + " WIDTH FL !@!" )
    blank_imageD2Width = ceil(widthPB - widthFL)
    blank_imageD2 = np.zeros((heightFL, blank_imageD2Width, 3), np.uint8)
    blank_imageD2.fill(255)

    FL = np.hstack((FL, blank_imageD2))

    Deel2 = np.vstack((FL, Pump_Backpack))

        
    
    heightDeel2, widthDeel2, channelDeel2 = Deel2.shape
    print( str(MaxHeight) + "Max Height " + str(heightDeel2) + " Height deel 2")

    BlankimageControlheight = ceil(MaxHeight - heightDeel2)
    BlankimageControlwidth = ceil(widthDeel2)

    blank_imageControl = np.zeros((BlankimageControlheight,BlankimageControlwidth,3), np.uint8)
    blank_imageControl.fill(255)
    ############################################################################################
    #                   Eind deel FINISHER                                                     #
    ############################################################################################
    Deel2 = np.vstack((blank_imageControl, Deel2))
    current_time = datetime.datetime.now() 
    a = os.path.basename(suppath)
    Testalles = np.hstack((SUP_Paddle, Deel2))
    cv2.imwrite("./output/"+ str(a), Testalles)


##############Test voor SUP Collage##########################

root = Tk()
#Tk().withdraw() # geen volledig GUI alleen het dialog Box
frame = Frame(width=900, height=700, bg="snow")

def paddle_file():
    global paddlepath
    paddlepath = askopenfilename()
    print(paddlepath)
    open_img("paddle")

def leash_file():
    global leashpath
    leashpath = askopenfilename()
    print(leashpath)
    open_img("leash")

def sup_file():
    global suppath
    suppath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(suppath)
    open_img("sup")

def fin_file():
    global finpath
    finpath = askopenfilename()
    print(finpath)
    open_img("fin")

def pump_file():
    global pumppath
    pumppath = askopenfilename()
    print(pumppath)
    open_img("pump")

def bag_file():
    global bagpath
    bagpath = askopenfilename()
    print(bagpath)
    open_img("bag")

def open_img(item):
    global suppath
    global paddlepath
    global leashpath
    global finpath
    if item == "sup":
        try:
            print("sup")
            imgSUP = Image.open(suppath)
            imgSUP = imgSUP.resize((200, 600), Image.ANTIALIAS)
            imgSUP = ImageTk.PhotoImage(imgSUP)
            panelSUP = Label(frame, image=imgSUP)
            panelSUP.image = imgSUP
            panelSUP.place(x=25,y=75)
        except NameError:
            print("do nothing SUP")
    if item == "paddle":
        try:
            print("paddle")
            imgPaddle = Image.open(paddlepath)
            imgPaddle = imgPaddle.resize((120, 490), Image.ANTIALIAS)
            imgPaddle = ImageTk.PhotoImage(imgPaddle)
            panelPaddle = Label(frame, image=imgPaddle)
            panelPaddle.image = imgPaddle
            panelPaddle.place(x=235, y=190)
        except NameError:
            print("do nothing PADDLE")
    if item == "leash":
        try:
            print("leashpath")
            imgleash = Image.open(leashpath)
            imgleash = imgleash.resize((175, 100), Image.ANTIALIAS)
            imgleash = ImageTk.PhotoImage(imgleash)
            panelLeash = Label(frame, image=imgleash)
            panelLeash.image = imgleash
            panelLeash.place(x=365, y=125)
        except:
            print("do nothing leash")
    if item == "fin":
        try:
            print("finpath")
            imgFin = Image.open(finpath)
            imgFin = imgFin.resize((160, 150), Image.ANTIALIAS)
            imgFin = ImageTk.PhotoImage(imgFin)
            panelFin = Label(frame, image=imgFin)
            panelFin.image = imgFin
            panelFin.place(x=534, y=84)
        except:
            print("do nothing finpath")
    if item == "pump":
        try:
            print("pumppath")
            imgpump = Image.open(pumppath)
            imgpump = imgpump.resize((200, 200), Image.ANTIALIAS)
            imgpump = ImageTk.PhotoImage(imgpump)
            panelPump = Label(frame, image=imgpump)
            panelPump.image = imgpump
            panelPump.place(x=365, y=240)
        except:
            print("Do Nothing Pump")
    if item == "bag":
        try:
            print("bagpath")
            imgBag = Image.open(bagpath)
            imgBag = imgBag.resize((200, 200), Image.ANTIALIAS)
            imgBag = ImageTk.PhotoImage(imgBag)
            panelbag = Label(frame, image=imgBag)
            panelbag.image = imgBag
            panelbag.place(x=365, y=470)
        except:
            print("do nothing bag")
    



############## <- Button voor de action voor dit
#filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
sup_select_but = Button(frame, text="Selecteer SUP", command=sup_file)
sup_select_but.place(x=75, y=10)

paddle_select_but = Button(frame, text="Selecteer Paddle", command=paddle_file)
paddle_select_but.place(x=230, y=10)

leash_select_but = Button(frame, text="Selecteer Leash", command=leash_file)
leash_select_but.place(x=400, y=10)

fin_select_but = Button(frame, text="Selecteer Fin", command=fin_file)
fin_select_but.place(x=550, y=10)

pump_select_but = Button(frame, text="Selecteer Pomp", command=pump_file)
pump_select_but.place(x=650, y=10)

bag_select_but = Button(frame, text="Selecteer Tas", command=bag_file)
bag_select_but.place(x=775, y=10)


panelSUP = Label(frame, text="SUP", width=25,height=30)
panelSUP.place(x=25,y=75)

panelPaddle=Label(frame, text="Paddle", width=15,height=24)
panelPaddle.place(x=235,y=190)

panelLeash = Label(frame, text="leash", width=20, height=5)
panelLeash.place(x=365, y=125)

panelFin = Label(frame, text="Fin", width=20, height=7 )
panelFin.place(x=534,y=84)

panelPump = Label(frame, text="Pomp", width=25, height=10)
panelPump.place(x=365, y=240)

panelbag = Label(frame, text="Tas", width=25, height=10)
panelbag.place(x=365, y=470)

endbut = Button(frame, text="maak Collage", command=collage)
endbut.place(x=775, y=650)

frame.pack()
#dit voorkomt dat de frame geresized kan worden verkomt lelijkheid
root.resizable(False, False)
root.title("Collage Maker")
# v belangrijkste van het userform
root.mainloop()

############## <- Button voor de action voor dit
#filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)