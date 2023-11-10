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
total_u = adventurer+hero+chall+champ

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

# autoclicker tiers cost
T1_cost = 2500000
T2_cost = 500000000
T3_cost = 25000000000
T4_cost = 1000000000000

# currency
diamonds = 0    # alt+4  ♦
count = 0
random_count = r.randint(1,100) # when to trigger diamond +1 (line 157)
multi = diamonds*0.2    # multiplier for each diamond

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
    [sg.Text(' ', pad = (250,1)), sg.Button('Start Game', size= (15,2), button_color='lightgreen', mouseover_colors='#099430', font= ('Leelawadee', 13,'bold'), key= 'Start')],

    [sg.Text(' ')],
    [sg.Text(' ', pad= (250,1)), sg.Button('Exit Game', size= (15,1), button_color= 'red', mouseover_colors='darkred', font= ('Leelawadee', 13))]
]

# layout for main game window
layout = [

    [sg.Text()],
    [sg.Text('', pad = (50,0)),sg.Text('AutoClickers:', font= ('Leelawadee', 14, 'bold'), background_color= '#4a87a8'), 
     sg.Text('', pad = (120,0)), sg.Text('Clicker Game GUI', font= ('Leelawadee', 16, 'bold'), background_color= '#e6a23e'),
     sg.Text('', pad = (140,0)),sg.Text('Upgrades', font= ('Leelawadee', 14, 'bold'), background_color= 'silver', key= 'upv')],

    [sg.Text()],
    [sg.Text('', pad= (15,15)), sg.Text('- T1\t', key= 'T1'), sg.Button(f'Purchase [{format_num(T1_cost)}]'), 
     sg.Text('', pad = (296,0)), sg.Text(f'- Adventurer:', background_color='#48addb', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'adv_value'),sg.Text(' '*5), 
     sg.Button(f'Purchase [{format_num(adventurer_cost)}]', auto_size_button=True, key= 'adventurer')],

    [sg.Text('', pad= (15,15)), sg.Text('- T2\t', key= 'T2'), sg.Button(f'Purchase [{format_num(T2_cost)}]'),
     sg.Text('', pad= (115,1)), sg.Text('Click Count: ', font= ('Leelawadee', 14, 'bold')), sg.Text(click_count, font= ('Leelawadee', 14, 'bold'), size=(10, 1), key='COUNT'),
     sg.Text('', pad = (55,0)), sg.Text('- Hero:', background_color='#48db68', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'hero_value'), sg.Text(' '*17), 
     sg.Button(f'Purchase [{format_num(hero_cost)}]', key= 'hero')],

    [sg.Text('', pad= (15,15)), sg.Text('- T3\t', key= 'T3'), sg.Button(f'Purchase [{format_num(T3_cost)}]'),
     sg.Text('', pad= (125,1)), sg.Button(f'Click!\n[{click_value}]',font= ('Leelawadee', 12, 'bold'), key='CLICK', size= (12, 2)),
     sg.Text('', pad = (105,0)), sg.Text('- Challanger:',background_color='#e63df2', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'chall_value'), sg.Text(' '*5), 
     sg.Button(f'Purchase [{format_num(chall_cost)}]', auto_size_button=True, key= 'challanger')],

    [sg.Text('', pad= (15,15)), sg.Text('- T4\t', key= 'T4'), sg.Button(f'Purchase [{format_num(T4_cost)}]'), 
     sg.Text('', pad = (300,0)), sg.Text('- Champion:', background_color='#e8892a', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'champ_value'), sg.Text(' '*6), 
     sg.Button(f'Purchase [{format_num(champ_cost)}]',auto_size_button=True, key= 'champion')],

    [sg.Text('', pad= (270,1)), sg.Text(f"❖{format_num(diamonds)}", key= 'diamonds', font=('Leelawadee', 15), text_color= 'aqua')],

    [sg.Text(' ', pad= (0,100))],
    [sg.Text('', pad=(520,0)), sg.Button('Exit Game', size = (10, 1), button_color= 'red', mouseover_colors='darkred')]

]

boss_layout = [

    
]

window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= False, no_titlebar= True)    # main game window
menu_window = sg.Window('Clicker Game GUI', menu_layout, size = (1200, 600), resizable= False, no_titlebar= True)  # menu window

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

    # changes color of CLICK button to random
    colors = ["#"+''.join([r.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(50)]
    color_r = r.choice(colors)

    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit Game'):
        break

    if event == 'CLICK':
        click_count += click_value
        count += 1
        print(count)
        window['COUNT'].update(format_num(click_count))
        window['CLICK'].update(f'Click!\n[{format_num(click_value)}]', button_color= color_r)
        
    if count == random_count:
        diamonds +=1
        
        sg.popup('You found a diamond!', text_color='aqua', auto_close= True, no_titlebar= True, auto_close_duration= 0.8, button_type= 5)
        count = 0
        random_count = r.randint(1,100)
        window['diamonds'].update(f'❖{format_num(diamonds)}', font=('Leelawadee', 15), text_color= 'aqua')

# adventurer upgrade
    elif event == 'adventurer':
        if click_count >= adventurer_cost:

            click_value -= adventurer
            adventurer += r.randint(click_adventurer+1, click_adventurer+40)
            click_adventurer += 25

            click_value += adventurer
            click_count -= adventurer_cost
            
            uc_rate += r.randint(100, 1000)
            adventurer_cost += uc_rate
            

            window['COUNT'].update(format_num(click_count))
            window['adv_value'].update(f' {format_num(adventurer)}')
            window['adventurer'].update(f'Upgrade [{format_num(adventurer_cost)}]')

# hero upgrade
    elif event == 'hero':
        if click_count >= hero_cost:

            click_value -= hero
            hero += r.randint(click_hero+1, click_hero+80)
            click_hero += 30

            click_value += hero
            click_count -= hero_cost

            uc_rate += r.randint(1000, 5000)
            hero_cost += uc_rate

            window['COUNT'].update(format_num(click_count))
            window['hero_value'].update(f' {format_num(hero)}')
            window['hero'].update(f'Upgrade [{format_num(hero_cost)}]')

# challanger upgrade
    elif event == 'challanger':
        if click_count >= chall_cost:

            click_value -= chall
            chall += r.randint(click_chall+1, click_chall+100)
            click_chall += 80

            click_value += chall
            click_count -= chall_cost

            uc_rate += r.randint(5000, 10000)
            chall_cost += uc_rate
            
            window['COUNT'].update(format_num(click_count))
            window['chall_value'].update(f' {format_num(chall)}')
            window['challanger'].update(f'Upgrade [{format_num(chall_cost)}]')

# champion upgrade
    elif event == 'champion':
        if click_count >= champ_cost:

            click_value -= champ
            champ += r.randint(click_champ+1, click_champ+200)
            click_champ += 300

            click_value += champ
            click_count -= champ_cost

            uc_rate += r.randint(10000, 1000000)
            champ_cost += uc_rate

            window['COUNT'].update(format_num(click_count))
            window['champ_value'].update(f' {format_num(champ)}')
            window['champion'].update(f'Upgrade [{format_num(champ_cost)}]')
window.close()