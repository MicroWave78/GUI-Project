import PySimpleGUI as sg
import time as t
import random as r

sg.theme('darkbrown2') 

sg.set_options(font=('Leelawadee', 12))
click_count = 0
click_value = 1 #click rate
click_upgrade = 1 #click rate upgrade
upgrade_cost = 25
uc_rate = 8 #upgrade cost ++
upgrade_level = 1

# function to format big numbers
def format_num(number):
    if abs(number) >= 1e15:
        return f'{number / 1/15:.2f}Q'
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
    [sg.Text('')],
    [sg.Text(' ', size= (50,1)), sg.Text('Welcome To Clicker Game GUI\nBy Dragos Chelariu', font= ('Leelawadee', 14))]
]

# layout for main game window
layout = [
    [sg.Text('')],
    [sg.Text('Click Count:', size=(15, 1)), sg.Text(click_count, size=(10, 1), key='COUNT')],
    [sg.Button('Click!', key='CLICK', size= (10, 1))],
    [sg.Text('Click Value: ', size=(15, 1)), sg.Text(click_value, size=(10, 1), key='VALUE')],
    [sg.Button(f'Upgrade Click Value [Lv. {upgrade_level}] ({format_num(upgrade_cost)} clicks)', key='UPGRADE')],
    [sg.Text('', key = 'COST')],
    [sg.Text('', size = (1, 18))],
    [sg.Button('Exit Game', size = (10, 1))]
]

# open menu window
menu_window = sg.Window('Clicker Game GUI', menu_layout, size = (1200, 600), resizable= False)  # menu window
check_play = True   # variable to check if the user wants to play or exit

while True:
    event, values = menu_window.read()

    if event in (sg.WIN_CLOSED, 'Exit Game'):
        check_play = False
        break



menu_window.close()


# open main game window
window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= False)    # main game window
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