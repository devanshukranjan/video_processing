"""
   => I have imported Tkinter framework for creating GUI and OpenCV for video processing

    ~ Devanshu Kumar Ranjan
      devanshukranjan@gmail.com
      6206938457
"""

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import time
import cv2
import os
import shutil
import random
from PIL import ImageTk, Image

#Creating GUI with tkinter
w = Tk()
w.title('Video To Frames Converter')
w.geometry('850x400')

# Creating Separators for spliting window frames
separator = Separator(w, orient='horizontal')
separator.place(relx=0, rely=0.25, relwidth=0.50, relheight=1)

separator = Separator(w, orient='horizontal')
separator.place(relx=0, rely=0.60, relwidth=0.50, relheight=1)
 
separator = Separator(w, orient='vertical')
separator.place(relx=0.50, rely=0, relwidth=0.3, relheight=1)


path=os.path.basename('C:')
path_new="C:/GUI_frame"
file_name=""

#For choosing video file
def video_path():
    global path
    #covering various video extension files
    path = filedialog.askopenfilename(title='Open a file', filetypes=[('Video Files', ['*.mp4','*.mkv','*.mov','*.wmv','*.flv','*.avi','*.avchd','*.webm','*.'])])
    dl['state']='normal'
    dl.insert(END, path)
    dl['state']='disabled'
    upload['state']='normal'
    Label(w, text='Click on Upload Video', foreground='red', font=("Arial",12,"")).place(relx=0.15, rely=0.32, relwidth=0.25, relheight=0.09)

#Uploading video to a directory
def uploadVideo():
    global path_new
    global file_name
    dlbtn['state']='disabled'
    upload['state']='disabled'
    
    Label(w, text='Video Uploading....', foreground='blue', font=("Arial",12,"")).place(relx=0.15, rely=0.32, relwidth=0.25, relheight=0.09)
    
    #Spliting directory and file
    (dirname,filename) =os.path.split(path)
    file_name=filename;
    try:
        if not os.path.exists(path_new):
            os.makedirs(path_new)
    except OSError:
        print(f"ERROR: creating directory with name {path_new}")
    
    shutil.copy(path, path_new)
    Label(w, text='Video Uploaded Successfully!', foreground='green', font=("Arial",12,"")).place(relx=0.12, rely=0.32, relwidth=0.27, relheight=0.09)
    frbtn['state']='normal'

# Function for Creating frames from video file
frames=0;

def Create_frame():
    global frames
    frbtn['state']='disabled'
    vid=cv2.VideoCapture(f"{path_new}/{file_name}")
    frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    #Creating Progressbar for showing progress of frame created
    pb2 = Progressbar(
        w, 
        orient=HORIZONTAL, 
        length=200, 
        mode='determinate'
        )
    pb2.place(relx=0.145, rely=0.667, relwidth=0.20, relheight=0.04)
    #Creating frames
    for i in range(0,frames-1):
        w.update_idletasks()
        success, frame = vid.read()
        if success==False:
            break
        cv2.imwrite(f"{path_new}/frame_{i}.jpg", frame)
        pb2['value'] = ((i*100)/frames)
    pb2.destroy()
    Label(w, text='Frames Created!', foreground='green', font=("Arial",12,"")).place(relx=0.18, rely=0.65, relwidth=0.35, relheight=0.09)
    vid.release()
    cv2.destroyAllWindows()
    shbtn['state']='normal'
    
# For showing any random frame
def show_any_frame():
    r=random.randint(0, frames-1)
    image1 = Image.open(f"{path_new}/frame_{r}.jpg")
    resized_image= image1.resize((370,225), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(resized_image)

    label1 = Label(image=test)
    label1.image = test
    label1.place(relx=0.52, rely=0.10, relwidth=0.60, relheight=0.60)

# Creating Text Box
dl = Text(w, height = 1, width = 35, state="disabled")
dl.place(relx=0.01, rely=0.08, relwidth=0.35, relheight=0.08)

# Creating Buttons

dlbtn = Button(w, text ='Choose File', command = lambda:video_path()) 
dlbtn.place(relx=0.37, rely=0.08, relwidth=0.10, relheight=0.085)

upload = Button(w, text=' Upload Video ', state='disabled', command=uploadVideo)
upload.place(relx=0.17, rely=0.45, relwidth=0.15, relheight=0.085)

frbtn = Button(w, text=' Create Frames ', state='disabled', command=Create_frame)
frbtn.place(relx=0.17, rely=0.80, relwidth=0.15, relheight=0.085)

shbtn = Button(w, text=' Show Random Frames ', state='disabled', command=show_any_frame)
shbtn.place(relx=0.68, rely=0.80, relwidth=0.15, relheight=0.085)

w.mainloop()