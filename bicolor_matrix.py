import PySimpleGUI as sg

cur_color = 'Black'
c_choices = ['Black', 'Green', 'Red', 'Orange']
x_vals = [128,64,32,16,8,4,2,1]
matrix_dict = {}
for x in x_vals:
    for y in range(8):
        matrix_dict[(x,y)] = 'Black'

grid_layout = []
for x in x_vals:
    grid_layout += [[sg.Graph((30,30),(19,19),(0,0), background_color='black',
                             enable_events= True, key=(x,y)) for y in range (8)]]

c_layout = [[sg.Button('Fill Current Color')]]
for cc in c_choices:
    c_layout += [[sg.Radio(cc,'c',key = cc, enable_events= True)]]
c_layout += [[sg.Button('Convert Image to Hex String', key = 'i-h')],
             [sg.Button('Convert Hex String to Image', key = 'h-i')]]

layout = [[sg.Frame('Matrix', grid_layout), sg.Frame('Controls', c_layout)],
          [sg.Input('', size = (64,1.5), key= 'hex_field', font = '16')]]

window=sg.Window('Bi-Color Matrix Designer',layout)

while True:
    event,values= window.read()
    print (event)
    if event in c_choices:
        cur_color = event

    if event == 'Fill Current Color':
        for x in x_vals:
            for y in range(8):
                window[(x,y)].update(background_color = cur_color)
                matrix_dict[(x,y)] = cur_color    

    for x in [128,64,32,16,8,4,2,1]:
        for y in range(8):
            if event == (x,y):
                window[event].update(background_color = cur_color)
                matrix_dict[event] = cur_color  

    if event == 'i-h':
        str_hex = ''
        for y in range(8):
            t_grn = 0
            t_red = 0
            for x in x_vals:
                if matrix_dict[(x,y)] == 'Green':
                    t_grn += x
                if matrix_dict[(x,y)] == 'Red':
                    t_red += x
                if matrix_dict[(x,y)] == 'Orange':
                    t_grn += x
                    t_red += x
            str_hex = str_hex + '\\x' + "{:02X}".format(t_grn)
            str_hex = str_hex + '\\x' + "{:02X}".format(t_red)
        print(str_hex)
        window['hex_field'].update(str_hex)

    if event == 'h-i':
        if len(values['hex_field']) == 64:
            hex_list = values['hex_field'].rsplit('\\x')
            hex_list.pop(0)
            int_list = [int(x, 16) for x in hex_list]
            print (int_list)
            for y in range (0,16,2):
                for i in range(8):
                    if int_list[y] >= x_vals[i]:
                        if int_list[y+1] >= x_vals[i]:
                            window[(x_vals[i],int(y/2))].update(background_color = 'Orange')
                            matrix_dict[(x_vals[i],int(y/2))] = 'Orange'
                            int_list[y] -= x_vals[i]
                            int_list[y+1] -= x_vals[i]
                        else:
                            window[(x_vals[i],int(y/2))].update(background_color = 'Green')
                            matrix_dict[(x_vals[i],int(y/2))] = 'Green'
                            int_list[y] -= x_vals[i]
                    elif int_list[y+1] >= x_vals[i]:
                        window[(x_vals[i],int(y/2))].update(background_color = 'Red')
                        matrix_dict[(x_vals[i],int(y/2))] = 'Red'
                        int_list[y+1] -= x_vals[i]

    if event in (sg.WIN_CLOSED, 'Exit'):
        break