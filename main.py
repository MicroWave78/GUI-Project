import PySimpleGUI as sg
import time as t
import random as r

sg.theme('darkbrown2') 
sg.set_options(font=('Leelawadee', 12), element_padding=(0,0))

# click related variables
click_count = 0
click_value = 1 #click rate
uc_rate = 8 #upgrade cost ++

# upgrades value
adventurer = 0
hero = 0
champ = 0
chall = 0

# upgrades cost
adventurer_cost = 50
hero_cost = 30000
chall_cost = 10000000
champ_cost = 2000000000

# upgrades click rate
click_adventurer = 1
click_hero = 1
click_champ = 1
click_chall = 1

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
    [sg.Text(' ', pad = (250,1)), sg.Button('Start Game', size= (15,2), mouseover_colors='lightgreen', button_color='silver', font= ('Leelawadee', 13,'bold'), key= 'Start')],

    [sg.Text(' ')],
    [sg.Text(' ', pad= (250,1)), sg.Button('Exit Game', size= (15,1), button_color= 'red', mouseover_colors='darkred', font= ('Leelawadee', 13))]
]

# layout for main game window
layout = [

    [sg.Text()],
    [sg.Text('', pad = (50,0)),sg.Text('AutoClickers:', font= ('Leelawadee', 14, 'bold'), background_color= '#4a87a8'), 
     sg.Text('', pad = (125,0)), sg.Text('Clicker Game GUI', font= ('Leelawadee', 16, 'bold'), background_color= '#e6a23e'),
     sg.Text('', pad = (140,0)),sg.Text('Upgrades:', font= ('Leelawadee', 14, 'bold'), background_color= 'silver', key= 'upv')],

    [sg.Text()],
    [sg.Text('', pad= (30,15)), sg.Text('- T1\t'), sg.Button(f'Purchase [{format_num(auto_cost)}]'), 
     sg.Text('', pad = (295,0)), sg.Text(f'- Adventurer:', background_color='#48addb', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'adv_value'),sg.Text(' '*5), 
     sg.Button(f'Purchase [{format_num(adventurer_cost)}]', key= 'adventurer')],

    [sg.Text('', pad= (30,15)), sg.Text('- T2\t'), sg.Button(f'Purchase [{format_num(auto_cost*3)}]'),
     sg.Text('', pad= (115,1)), sg.Text('Click Count: ', font= ('Leelawadee', 14, 'bold')), sg.Text(click_count, font= ('Leelawadee', 14, 'bold'), size=(10, 1), key='COUNT'),
     sg.Text('', pad = (62,0)), sg.Text('- Hero:', background_color='#48db68', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'hero_value'), sg.Text(' '*17), 
     sg.Button(f'Purchase [{format_num(hero_cost)}]', key= 'hero')],

    [sg.Text('', pad= (30,15)), sg.Text('- T3\t'), sg.Button(f'Purchase [{format_num(auto_cost*5)}]'),
     sg.Text('', pad= (120,1)), sg.Button('Click!',font= ('Leelawadee', 13, 'bold'), key='CLICK', size= (10, 1)),
     sg.Text('', pad = (120,0)), sg.Text('- Challanger:',background_color='#e63df2', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'chall_value'), sg.Text(' '*6), 
     sg.Button(f'Purchase [{format_num(chall_cost)}]', key= 'challanger')],

    [sg.Text('', pad= (30,15)), sg.Text('- T4\t'), sg.Button(f'Purchase [{format_num(auto_cost*10)}]'), 
     sg.Text('', pad = (290,0)), sg.Text('- Champion:', background_color='#e8892a', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'champ_value'), sg.Text(' '*6), 
     sg.Button(f'Purchase [{format_num(champ_cost)}]', key= 'champion')],

    [sg.Text('', pad= (255,300)), sg.Button('Exit Game', size = (10, 1))]
]

window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= True)    # main game window
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
    event, values = window.read(timeout=500)
    if event in (sg.WIN_CLOSED, 'Exit Game'):
        break

    if event == 'CLICK':
        click_count += click_value
        window['COUNT'].update(format_num(click_count))

# adventurer upgrade
    elif event == 'adventurer':
        if click_count >= adventurer_cost:

            click_value -= adventurer
            adventurer += r.randint(click_adventurer, click_adventurer+40)
            click_adventurer += 25

            click_value += adventurer
            click_count -= adventurer_cost
            
            uc_rate += r.randint(100, 1000)
            adventurer_cost += uc_rate
            

            window['COUNT'].update(format_num(click_count))
            window['adv_value'].update(f' {format_num(adventurer)}')
            window['adventurer'].update(f'Upgrade [{format_num(adventurer_cost)}]')
            window['upv'].update(f'Upgrades: {format_num(adventurer+hero+chall+champ)}')

# hero upgrade
    elif event == 'hero':
        if click_count >= hero_cost:

            click_value -= hero
            hero += r.randint(click_hero, click_hero+80)
            click_hero += 30

            click_value += hero
            click_count -= hero_cost

            uc_rate += r.randint(1000, 5000)
            hero_cost += uc_rate

            window['COUNT'].update(format_num(click_count))
            window['hero_value'].update(f' {format_num(hero)}')
            window['hero'].update(f'Upgrade [{format_num(hero_cost)}]')
            window['upv'].update(f'Upgrades: {format_num(adventurer+hero+chall+champ)}')

# challanger upgrade
    elif event == 'challanger':
        if click_count >= chall_cost:

            click_value -= chall
            chall += r.randint(click_chall, click_chall+100)
            click_chall += 80

            click_value += chall
            click_count -= chall_cost

            uc_rate += r.randint(5000, 10000)
            chall_cost += uc_rate
            
            window['COUNT'].update(format_num(click_count))
            window['chall_value'].update(f' {format_num(chall)}')
            window['challanger'].update(f'Upgrade [{format_num(chall_cost)}]')
            window['upv'].update(f'Upgrades: {format_num(adventurer+hero+chall+champ)}')

# champion upgrade
    elif event == 'champion':
        if click_count >= champ_cost:

            click_value -= champ
            champ += r.randint(click_champ, click_champ+200)
            click_champ += 300

            click_value += champ
            click_count -= champ_cost

            uc_rate += r.randint(10000, 1000000)
            champ_cost += uc_rate

            window['COUNT'].update(format_num(click_count))
            window['champ_value'].update(f' {format_num(champ)}')
            window['champion'].update(f'Upgrade [{format_num(champ_cost)}]')
            window['upv'].update(f'Upgrades: {format_num(adventurer+hero+chall+champ)}')
window.close()