import PySimpleGUI as sg
import time as t
import random as r

sg.theme('darkbrown2') 
sg.set_options(font=('Leelawadee', 12), element_padding=(0,0))

# click related variables
click_count = 0
click_value = 1 #click rate
click_upgrade = 1 #click rate upgrade
upgrade_cost = 25
uc_rate = 8 #upgrade cost ++
upgrade_level = 1

auto_cost = 1500


# function to format big numbers
def format_num(number):
    if abs(number) >= 1e15:
        return f'{number / 1e15:.2f}Q'
    elif abs(number) >= 1e12:
        return f'{number / 1e12:.2f}T'
    elif abs(number) >= 1e9:
        return f'{number / 1e9:.2f}B'
    elif abs(number) >= 1e6:
        return f'{number / 1e6:.2f}M'
    elif abs(number) >= 1e3:
        return f'{number / 1e3:.2f}K'
    else:
        return number

# layout for menu window
menu_layout = [
    [sg.Text(' ', size= (1,8))],

    [sg.Text(' ', pad= (225,1)), sg.Text('Welcome To Clicker Game GUI', font= ('Leelawadee', 15, 'bold'))],
    [sg.Text(' ', pad= (246,1)), sg.Text('By', font= ('Leelawadee', 15, 'bold')),
                                 sg.Text('Dragos Chelariu', font= ('Leelawadee', 15, 'italic'))],

    [sg.Text(' ')],
    [sg.Text(' ', pad = (250,1)), sg.Button('Start Game', size= (15,2), button_color='silver', font= ('Leelawadee', 13,'bold'), key= 'Start')],

    [sg.Text(' ')],
    [sg.Text(' ', pad= (250,1)), sg.Button('Exit Game', size= (15,1), button_color= 'red', mouseover_colors='darkred', font= ('Leelawadee', 13))]
]

# layout for main game window
layout = [
    [sg.Text()],
    
    [sg.Text('', pad = (50,0)),sg.Text('AutoClickers:', font= ('Leelawadee', 14, 'bold'), background_color= '#4a87a8'), 
     sg.Text('', pad = (125,0)), sg.Text('Clicker Game GUI', font= ('Leelawadee', 16, 'bold'), background_color= '#e6a23e'),
     sg.Text('', pad = (140,0)),sg.Text('Upgrades:', font= ('Leelawadee', 14, 'bold'), background_color= '#4a87a8')],

    [sg.Text()],
    [sg.Text('', pad= (30,15)), sg.Text('- T1\t'), sg.Button(f'Purchase [{format_num(auto_cost)}]'), 
     sg.Text('', pad = (300,0)), sg.Text('- Adventurer\t'), sg.Button(f'Purchase [{format_num(auto_cost)}]')],

    [sg.Text('', pad= (30,15)), sg.Text('- T2\t'), sg.Button(f'Purchase [{format_num(auto_cost*3)}]'),
     sg.Text('', pad= (115,1)), sg.Text('Click Count: ', font= ('Leelawadee', 14, 'bold')), sg.Text(click_count, font= ('Leelawadee', 14, 'bold'), size=(10, 1), key='COUNT'),
     sg.Text('', pad = (300,0)), sg.Text('- Hero\t\t'), sg.Button(f'Purchase [{format_num(auto_cost)}]')],

    [sg.Text('', pad= (30,15)), sg.Text('- T3\t'), sg.Button(f'Purchase [{format_num(auto_cost*5)}]'),
     sg.Text('', pad= (120,1)), sg.Button('Click!',font= ('Leelawadee', 13, 'bold'), key='CLICK', size= (10, 1)),
     sg.Text('', pad = (300,0)), sg.Text('- Champion\t'), sg.Button(f'Purchase [{format_num(auto_cost)}]')],

    [sg.Text('', pad= (30,15)), sg.Text('- T4\t'), sg.Button(f'Purchase [{format_num(auto_cost*10)}]'), 
     sg.Text('', pad = (296,0)), sg.Text('- Challanger\t'), sg.Button(f'Purchase [{format_num(auto_cost)}]')],

   

    
    [sg.Text('')],
    [sg.Text('', pad = (255,0)), sg.Text('Click Value: ', size=(15, 1)), sg.Text(click_value, size=(10, 1), key='VALUE')],
    [sg.Text('', pad = (210,0)), sg.Button(f'Upgrade Click Value [Lv. {upgrade_level}] ({format_num(upgrade_cost)} clicks)', key='UPGRADE')],
    [sg.Text('', pad = (245,0)), sg.Text('', key = 'COST')],

    [sg.Text('', pad= (0,25))],

    [sg.Button('Exit Game', size = (10, 1))]


]

window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= False)    # main game window
menu_window = sg.Window('Clicker Game GUI', menu_layout, size = (1200, 600), resizable= False)  # menu window

check_play = True   # variable to check if the user wants to play or exit

# open menu window
while True:
    event, values = menu_window.read()

    if event in (sg.WIN_CLOSED, 'Exit Game'):
        check_play = False
        break

    if event == 'Start':
        break


menu_window.close()


# open main game window

while check_play == True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit Game'):
        break

    if event == 'CLICK':
        click_count += click_value
        window['COUNT'].update(format_num(click_count))
        window['COST'].update('')
    elif event == 'UPGRADE':
        if click_count >= upgrade_cost:

            click_value += r.randint(click_upgrade, click_upgrade+2)
            click_upgrade += 1

            click_count -= upgrade_cost

            upgrade_cost += uc_rate
            uc_rate += r.randint(15, 50)

            upgrade_level += 1

            window['VALUE'].update(format_num(click_value))
            window['COUNT'].update(format_num(click_count))
            window['UPGRADE'].update(f'Upgrade Click Value [Lv. {upgrade_level}] ({format_num(upgrade_cost)} clicks)')
        else:
            window['COST'].update('Not enough clicks.')

window.close()