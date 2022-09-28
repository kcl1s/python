import cv2
import imutils
import PySimpleGUI as sg
thresh=255
gotImg=False
gotTImg=False
sg.theme('DarkGreen5')
photoO=[[sg.Image('',k='orig')]]
photoU=[[sg.Image('',background_color='black',k='updated')]]
layout=[[sg.Input(size=80,key='fileB',enable_events=True),sg.FileBrowse(button_text='Browse All')],
        [sg.Frame('Original',photoO,size=(640,360),element_justification='center'),
            sg.Frame('Updated',photoU,size=(640,360),element_justification='center')],
        [sg.Radio('Remove White Background','bgc',enable_events=True,default=True,k='w'),
            sg.Radio('Remove Black Background','bgc',enable_events=True,k='b'),
            sg.Slider(range=(0,255),orientation='h',default_value=255,enable_events=True,resolution=5,k='sw')],
        [sg.Save(),sg.Exit()]]

window=sg.Window('Transparent Background Converter',layout,	relative_location=(0,-100),finalize=True)

while True:
    event,values= window.read()
    if event == 'fileB':
        img=cv2.imread(values['fileB'])
        height,width,x=img.shape
        if width > 640:
            img = imutils.resize(img, width=640)
        if height > 360:
            img = imutils.resize(img, height=360)
        height,width,x=img.shape
        window['orig'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        window['updated'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        gotImg=True
        fPath=values['fileB'].rsplit('/',1)[0]
    if event == 'sw' and gotImg:
        thresh=int(values['sw'])
        imgBGRA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        height,width,x=imgBGRA.shape
        for h in range(height):
            for w in range(width):
                pData=imgBGRA[h][w]
                if values['w']:
                    if pData[0] > thresh and pData[1] > thresh and pData[2] > thresh:
                        pData[3]=0
                        imgBGRA[h][w]=pData
                if values['b']:
                    if pData[0] < thresh and pData[1] < thresh and pData[2] < thresh:
                        pData[3]=0
                        imgBGRA[h][w]=pData
        window['updated'].update(data=cv2.imencode('.png', imgBGRA)[1].tobytes())
        gotTImg=True
    if event == 'Save' and gotTImg:
        saveFile= sg.popup_get_file('',save_as=True,no_window=True,
                        initial_folder=fPath,default_extension='.png')
        cv2.imwrite(saveFile,imgBGRA)
    if event == 'w':
        window['sw'].update(value=255)
        window['updated'].Widget.config(background='black')
    if event == 'b':
        window['sw'].update(value=0)
        window['updated'].Widget.config(background='white')
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()