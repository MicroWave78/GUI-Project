import PySimpleGUI as sg
import time as t


sg.theme('darkpurple1')  # Choose a theme

# Initialize variables
click_count = 0
click_value = 1
click_upgrade = 1
upgrade_cost = 25
upgrade_level = 1

def formatNum(number):
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

# Define the layout of the GUI
layout = [
    [sg.Text('Click Count:', size=(15, 1)), sg.Text(click_count, size=(10, 1), key='COUNT')],
    [sg.Button('Click!', key='CLICK')],
    [sg.Text('Click Value: ', size=(15, 1)), sg.Text(click_value, size=(10, 1), key='VALUE')],
    [sg.Button(f'Upgrade Click Value [Lv. {upgrade_level}] ({formatNum(upgrade_cost)} clicks)', key='UPGRADE')],
    [sg.Text('', key = 'COST')],
    [sg.Button('Quit')]
]


# Create the window
window = sg.Window('Clicker Game GUI', layout, size = (1000,500))

# Event loop
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Quit'):
        break

    if event == 'CLICK':
        click_count += click_value
        window['COUNT'].update(formatNum(click_count))
        window['COST'].update('')
    elif event == 'UPGRADE':
        if click_count >= upgrade_cost:
            click_value += click_upgrade
            click_upgrade += 1
            click_count -= upgrade_cost
            upgrade_cost += 8
            upgrade_level += 1
            window['VALUE'].update(formatNum(click_value))
            window['COUNT'].update(formatNum(click_count))
            window['UPGRADE'].update(f'Upgrade Click Value [Lv. {upgrade_level}] ({formatNum(upgrade_cost)} clicks)')
        else:
            window['COST'].update('Not enough clicks.')
window.close()