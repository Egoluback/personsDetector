from imutils.video import VideoStream
from MakePhoto import MakePhoto

import numpy as np
import cv2, time, imutils, argparse, telebot

ap = argparse.ArgumentParser()

ap.add_argument('-p', '--prototxt', default = "deploy.prototxt.txt", help = 'Caffe model description.')
ap.add_argument('-m', '--model', default = "res10_300x300_ssd_iter_140000.caffemodel", help = 'Path to pre-trained Caffe NN.')
ap.add_argument('-c', '--confidence', type=float, default=0.5, help = 'min prob filter weak')

args = vars(ap.parse_args())

bot = telebot.TeleBot("YOUR-TOKEN")

CHAT_ID = 426085120

@bot.message_handler(commands = ["start"])
def startMessage(message):
    bot.send_message(message.chat.id, "Hello! I remembered your chat id.")

@bot.message_handler(commands = ["make_photo"])
def sendPhoto(message):
    res = MakePhoto(args, "person.png").Photo()
    if (not res):
        bot.send_message(CHAT_ID, "no people found")
    image = open("person.png", "rb")
    bot.send_photo(CHAT_ID, image)

bot.polling()
