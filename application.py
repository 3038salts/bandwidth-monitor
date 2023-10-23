from tkinter import *
from PIL import Image, ImageTk
import time, psutil, threading

root = Tk()
root.title("Bandwidth Statistics")
root.geometry("350x150") # window size
root.resizable(False, False)

# open image and resize
original = Image.open("wifi.png")
resize_image = original.resize((original.width // 10, original.height // 10))
img = ImageTk.PhotoImage(resize_image)

# image grid
Label(root, image = img).grid(row = 0, column = 1)

# updated variables
downloadVar = StringVar()
uploadVar = StringVar()
totalVar = StringVar()

totalDownloadVar = StringVar()
totalUploadVar = StringVar()
totalTotalVar = StringVar()

def refresh():
    # initial
    initialReceived = psutil.net_io_counters().bytes_recv
    initialSent = psutil.net_io_counters().bytes_sent
    initialTotal = initialReceived + initialSent

    # total bandwidth accumulated since program started running
    totalDown = totalUp = totalTotal = 0

    # for conversion value, 0th is download, 1st is upload, 2nd is total
    reducerList = [0, 0, 0]
    unitList = ["a", "b", "c"]

    while True:
        # refreshed
        updatedReceived = psutil.net_io_counters().bytes_recv
        updatedSent = psutil.net_io_counters().bytes_sent
        updatedTotal = updatedReceived + updatedSent

        # calculate change to determine bytes per unit of time
        download = updatedReceived - initialReceived
        upload = updatedSent - initialSent
        total = updatedTotal - initialTotal

        # add to total bandwidth
        totalDown += download
        totalUp += upload
        totalTotal += total

        download /= 1024 ** 2
        upload /= 1024 ** 2
        total /= 1024 ** 2

        temp = None
        for x in range(3):
            if x == 0:
                temp = totalDown
            elif x == 1:
                temp = totalUp
            else:
                temp = totalTotal

            if temp > 1024 ** 3:
                # convert to GB
                reducerList[x] = 3
                unitList[x] = "GB"
            elif temp > 1024 ** 2:
                # convert to MB
                reducerList[x] = 2
                unitList[x] = "MB"
            else:
                # convert to KB
                reducerList[x] = 1
                unitList[x] = "KB"

        convertedTotalDown = totalDown / 1024 ** reducerList[0]
        convertedTotalUp = totalUp / 1024 ** reducerList[1]
        convertedTotalTotal = totalTotal / 1024 ** reducerList[2]
        
        # output
        downloadVar.set(f"Download: {download:.3f} MB/sec")
        uploadVar.set(f"Upload: {upload:.3f} MB/sec")
        totalVar.set(f"Total: {total:.3f} MB/sec")
        totalDownloadVar.set(f"Total Received: {convertedTotalDown:.3f} {unitList[0]}")
        totalUploadVar.set(f"Total Sent: {convertedTotalUp:.3f} {unitList[1]}")
        totalTotalVar.set(f"Total Usage: {convertedTotalTotal:.3f} {unitList[2]}")

        # updated becomes initial for next unit of time
        initialReceived = updatedReceived
        initialSent = updatedSent
        initialTotal = updatedTotal
        
        # only updates once per second
        time.sleep(1)

# threading
refreshThread = threading.Thread(target = refresh)
refreshThread.daemon = True
refreshThread.start()

# text
title = Label(root, text = "Bandwidth Statistics!")
down = Label(root, textvariable = downloadVar)
up = Label(root, textvariable = uploadVar)
together = Label(root, textvariable = totalVar)
totalDown = Label(root, textvariable = totalDownloadVar)
totalUp = Label(root, textvariable = totalUploadVar)
totalTogether = Label(root, textvariable = totalTotalVar)

# text grid
title.grid(row = 0, column = 0)
down.grid(row = 1, column = 0)
up.grid(row = 2, column = 0)
together.grid(row = 3, column = 0)
totalDown.grid(row = 1, column = 1)
totalUp.grid(row = 2, column = 1)
totalTogether.grid(row = 3, column = 1)

root.mainloop()