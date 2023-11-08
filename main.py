import PySimpleGUI as sg
import time as t
import random as r


sg.theme('darkpurple1') 


font_name = 'Helvetica'
click_count = 0
click_value = 1 #click rate
click_upgrade = 1 #click rate upgrade
upgrade_cost = 25
uc_rate = 8 #upgrade cost rate
upgrade_level = 1


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
        return str(number)


layout = [
    [sg.Text('')],
    [sg.Text('Click Count:', size=(15, 1), font= font_name), sg.Text(click_count, size=(10, 1), key='COUNT', font= font_name)],
    [sg.Button('Click!', key='CLICK', size= (10, 1), font= font_name)],
    [sg.Text('Click Value: ', size=(15, 1), font= font_name), sg.Text(click_value, size=(10, 1), key='VALUE', font= font_name)],
    [sg.Button(f'Upgrade Click Value [Lv. {upgrade_level}] ({format_num(upgrade_cost)} clicks)', key='UPGRADE', font= font_name)],
    [sg.Text('', key = 'COST')],
    [sg.Button('Quit', size = (10, 1), font= font_name)]
]


window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= False, font= font_name)


while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Quit'):
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
            window['COST'].update('Not enough clicks.', font= font_name)

window.close()