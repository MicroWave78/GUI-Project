import PySimpleGUI as sg
import random as r
import threading as tr
import time as t
import concurrent.futures

sg.theme('darkbrown2') 
sg.set_options(font=('Leelawadee', 12), element_padding=(0,0), keep_on_top= True)

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

class Var:
    click_count = 0
    click_value = 1 #click rate
    click_crit = 0


    # upgrades value
    adventurer = 0
    hero = 0
    champ = 0
    chall = 0
    uc_rate = 8 #upgrade cost ++

    # upgrades cost
    adventurer_cost = 50
    hero_cost = 30000
    chall_cost = 100000000
    champ_cost = 20000000000

    # upgrades click rate
    click_adventurer = 1
    click_hero = 1
    click_champ = 1
    click_chall = 1

    # autoclicker tiers cost
    T1_cost = 2500
    T2_cost = 500000
    T3_cost = 2500000
    T4_cost = 100000000

    # autoclicker value
    T1 = 1
    T2 = 0
    T3 = 0
    T4 = 0

    # currency
    diamonds = 0    # ❖
    count = 0
    random_count = r.randint(1, 200) # when to trigger diamond +1 
    multi = diamonds*2   # multiplier for each diamond

    # boss variables
    boss_hp = 10
    boss_trigger = r.randint(1,20)
    boss_click_count = 0
    boss_names = ['Grayskin', 'Crowspeak', 'Lightshorn', 'One-Eye', 'Thornblight', 'Skinrender', 'Raverclaw', 'Dreadnaught', 'Morticia', 'Mordath', 'Wolftamer', 'Portent', 'Typhus', 'Corpsebreath', 'Marroweater', 'Archlich', 'Abolusha', 'Grendle', 'Polyphemus', 'Limper', 'Wintercall', 'Craven', 'Bramblejack', 'Hallowskull', 'Ferrous', 'Tempest', 'ScarRidge', 'Embergaze', 'Deathmire', 'Sylvanus', 'Kane', 'Tarsus', 'Ashencroft', 'Gluttonous', 'Damnerstake', 'Extraveous']
    boss_titles =  ['the Conqueror', 'Ragewalker', 'the Impaler', 'Heirtaker', "- the Reaper's Kiss", 'the Flameborne', 'the Deceiver', 'the Miser', '- Blesser of Pain', 'the Undefeated', 'Knightslayer', 'the Cannibal', 'Horsegutter', 'Skullgrinder', 'the Deathbringer', 'the Great Hammer', '- Oracle of Curses', 'Bloodmount', 'Hordemaster', 'Stormbringer', 'Faeriestalker', 'of the Black Stars', 'the Wicked', 'Fangbrood', 'the Corrupter', 'Bileblossom', '- Sunderer of Shields', 'the Branded', 'Wyrmtongue', 'Teardrinker', 'the Hobbled', 'the Dark Eye', 'Soulbinder', 'Blackheart', 'of the Iron Cage', 'the Patriarch']
    random_crit = r.randint(1,100)  # when to trigger crit (click value x10)

class Menu:
    check_play = True
    def menu_window():
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

        menu_window = sg.Window('Clicker Game GUI', menu_layout, size = (1200, 600), resizable= False, no_titlebar= False)  # menu window
        
        while True:
            event, values = menu_window.read()
            if event in (sg.WIN_CLOSED, 'Exit Game'):
                Menu.check_play = False
                break
            
            if event == 'Start':
                break
        menu_window.close()

class Main:
    
    def main_window(layout, window):
        
        while Menu.check_play == True:
            event, values = window.read()
            # changes color of CLICK button to random
            colors = ["#"+''.join([r.choice('0123456789ABCDEF') for j in range(6)]) for i in range(50)]
            color_r = r.choice(colors)
            
            if event in (sg.WIN_CLOSED, 'Exit Game'):
                break

            if event == 'CLICK':
                Var.click_count += Var.click_value
                Var.count += 1  # clicks to diamond trigger
                print(Var.boss_click_count)
                print(Var.boss_trigger)
                Var.boss_click_count += 1
                Var.click_crit += 1

                window['COUNT'].update(format_num(Var.click_count))
                window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]', button_color= color_r)

            if Var.boss_click_count == Var.boss_trigger:
                Boss.start_window()

            elif event == 'adventurer':
                if Var.click_count >= Var.adventurer_cost:

                    Var.click_value -= Var.adventurer
                    Var.adventurer += r.randint(Var.click_adventurer+1, Var.click_adventurer+40)
                    Var.click_adventurer += 25

                    Var.click_value += Var.adventurer
                    Var.click_count -= Var.adventurer_cost
                    
                    Var.uc_rate += r.randint(100, 700)
                    Var.adventurer_cost += Var.uc_rate
                    

                    window['COUNT'].update(format_num(Var.click_count))
                    window['adv_value'].update(f' {format_num(Var.adventurer)}')
                    window['adventurer'].update(f'Upgrade [{format_num(Var.adventurer_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # hero upgrade
            elif event == 'hero':
                if Var.click_count >= Var.hero_cost:

                    Var.click_value -= Var.hero
                    Var.hero += r.randint(Var.click_hero+1, Var.click_hero+80)
                    Var.click_hero += 40

                    Var.click_value += Var.hero
                    Var.click_count -= Var.hero_cost

                    Var.uc_rate += r.randint(1000, 3000)
                    Var.hero_cost += Var.uc_rate

                    window['COUNT'].update(format_num(Var.click_count))
                    window['hero_value'].update(f' {format_num(Var.hero)}')
                    window['hero'].update(f'Upgrade [{format_num(Var.hero_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # challanger upgrade
            elif event == 'challanger':
                if Var.click_count >= Var.chall_cost:

                    Var.click_value -= Var.chall
                    Var.chall += r.randint(Var.click_chall+1, Var.click_chall+100)
                    Var.click_chall += 100

                    Var.click_value += Var.chall
                    Var.click_count -= Var.chall_cost

                    Var.uc_rate += r.randint(5000, 10000)
                    Var.chall_cost += Var.uc_rate
                    
                    window['COUNT'].update(format_num(Var.click_count))
                    window['chall_value'].update(f' {format_num(Var.chall)}')
                    window['challanger'].update(f'Upgrade [{format_num(Var.chall_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # champion upgrade
            elif event == 'champion':
                if Var.click_count >= Var.champ_cost:

                    Var.click_value -= Var.champ
                    Var.champ += r.randint(Var.click_champ+1, Var.click_champ+200)
                    Var.click_champ += 300

                    Var.click_value += Var.champ
                    Var.click_count -= Var.champ_cost

                    Var.uc_rate += r.randint(10000, 1000000)
                    Var.champ_cost += Var.uc_rate

                    window['COUNT'].update(format_num(Var.click_count))
                    window['champ_value'].update(f' {format_num(Var.champ)}')
                    window['champion'].update(f'Upgrade [{format_num(Var.champ_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')
            if Var.count == Var.random_count:
                diamonds_win = r.randint(1,100)
                Var.diamonds += diamonds_win
                
                sg.popup(f'You found {diamonds_win} diamonds!', text_color='aqua', auto_close= True, no_titlebar= True, auto_close_duration= 0.8, button_type= 5)
                Var.count = 0
                Var.random_count = r.randint(1,100)
                window['diamonds'].update(f'❖{format_num(Var.diamonds)}', font=('Leelawadee', 15), text_color= 'aqua')
        window.close()

        
class Boss:
    def start_window():
    
        sg.theme(r.choice(sg.theme_list())) # random theme each time
        boss_layout = [
            [sg.Text('', pad = (100,0)),sg.Text(f'{r.choice(Var.boss_names)+' '+r.choice(Var.boss_titles)}', key= 'boss_name', background_color= 'grey')],
            [sg.Text('', pad= (75,0)),
            sg.ProgressBar(Var.boss_hp, 'h', size=(20, 5), key='bossHP'),
            sg.Text(f' HP Left: {format_num(Var.boss_hp)}', key='bossHPvalue')],
            [sg.Text('', pad= (110,30)),
            sg.Button(f'Attack! [{format_num(Var.click_value)} DMG]', auto_size_button=True, key = 'Attack')],
            [sg.Text('', pad= (250,50)),sg.Button('Surrender', button_color= 'red')]
            ]
        boss_window = sg.Window('Boss Fight', boss_layout, size=(600, 300), resizable= False)
            
        while True:
            event, values = boss_window.read()

            if event == 'Attack':
                Var.boss_hp -= Var.click_value
                Var.click_crit += 1
                boss_window['bossHP'].update(Var.boss_hp)
                boss_window['bossHPvalue'].update(f' HP Left: {format_num(Var.boss_hp)}')
            
            if Var.click_crit == Var.random_crit:
                Var.boss_hp -= Var.click_value*10
                boss_window['bossHP'].update(Var.boss_hp)
                boss_window['bossHPvalue'].update(format_num(Var.boss_hp))
                sg.popup('Crit!', auto_close=True, no_titlebar= True, auto_close_duration= 0.2, button_type=5, text_color= 'red')
                Var.click_crit = 0
                Var.random_crit = r.randint(1,100)
            
            if Var.boss_hp <= 0:
                Var.boss_reward = r.randint(Var.diamonds+5, Var.diamonds+40)
                sg.popup(f"You beat the boss! Here's {Var.boss_reward} diamonds", auto_close=True, no_titlebar= True, auto_close_duration= 1, button_type= 5)
                Var.diamonds += Var.boss_reward
                window['diamonds'].update(f'❖{format_num(Var.diamonds)}', font=('Leelawadee', 15), text_color= 'aqua')
                sg.theme('darkbrown2')
                break

            if event in (sg.WIN_CLOSED, 'Surrender'):
                sg.theme('darkbrown2')
                break

        Var.boss_click_count = 0
        Var.boss_trigger = r.randint(1,200)
        Var.boss_hp = r.randint(Var.click_value*30, Var.click_value*200)
        boss_window.close()

class Click:
    def crit():
        if Var.click_crit == Var.random_crit:
            Var.click_count += Var.click_value*10
            sg.popup('Crit!', auto_close=True, no_titlebar= True, auto_close_duration= 0.2, button_type=5, text_color= 'gold')
            Var.click_crit = 0
            Var.random_crit = r.randint(1,100)

layout = [
        [sg.Text()],
        [sg.Text('', pad = (50,0)),sg.Text('AutoClickers:', font= ('Leelawadee', 14, 'bold'), background_color= '#4a87a8'), 
        sg.Text('', pad = (120,0)), sg.Text('Clicker Game GUI', font= ('Leelawadee', 16, 'bold'), background_color= '#e6a23e'),
        sg.Text('', pad = (140,0)),sg.Text('Upgrades', font= ('Leelawadee', 14, 'bold'), background_color= 'silver', key= 'upv')],

        [sg.Text()],
        [sg.Text('', pad= (15,15)), sg.Text('- Tier 1: 0\t  ', key= 'T1', font=('Leelawadee', 12)), sg.Button(f'❖{format_num(Var.T1_cost)}', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background())), 
        sg.Text('', pad = (325,0)), sg.Text(f'- Adventurer:', background_color='#48addb', font=('Leelawadee', 13)),
        sg.Text(' 0', key= 'adv_value'),sg.Text(' '*5),
        sg.Button(f'Purchase [{format_num(Var.adventurer_cost)}]', auto_size_button=True, key= 'adventurer')],

        [sg.Text('', pad= (15,15)), sg.Text('- Tier 2: 0\t  ', key= 'T2', font=('Leelawadee', 12)), sg.Button(f'❖{format_num(Var.T2_cost)}', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background())),
        sg.Text('', pad= (147,1)), sg.Text('Click Count: ', font= ('Leelawadee', 14, 'bold')), sg.Text(Var.click_count, font= ('Leelawadee', 14, 'bold'), size=(10, 1), key='COUNT'),
        sg.Text('', pad = (52,0)), sg.Text('- Hero:', background_color='#48db68', font=('Leelawadee', 13)), 
        sg.Text(' 0', key= 'hero_value'), sg.Text(' '*17), 
        sg.Button(f'Purchase [{format_num(Var.hero_cost)}]', auto_size_button=True, key= 'hero')],

        [sg.Text('', pad= (15,15)), sg.Text('- Tier 3: 0\t  ', key= 'T3', font=('Leelawadee', 12)), sg.Button(f'❖{format_num(Var.T3_cost)}', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background())),
        sg.Text('', pad= (155,1)), sg.Button(f'Click!\n[{Var.click_value}]',font= ('Leelawadee', 12, 'bold'), key='CLICK', size= (12, 2)),
        sg.Text('', pad = (104,0)), sg.Text('- Challanger:',background_color='#e63df2', font=('Leelawadee', 13)), 
        sg.Text(' 0', key= 'chall_value'), sg.Text(' '*5), 
        sg.Button(f'Purchase [{format_num(Var.chall_cost)}]', auto_size_button=True, key= 'challanger')],

        [sg.Text('', pad= (15,15)), sg.Text('- Tier 4: 0\t  ', key= 'T4', font=('Leelawadee', 12)), sg.Button(f'❖{format_num(Var.T4_cost)}', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background())), 
        sg.Text('', pad = (315,0)), sg.Text('- Champion:', background_color='#e8892a', font=('Leelawadee', 13)), 
        sg.Text(' 0', key= 'champ_value'), sg.Text(' '*6), 
        sg.Button(f'Purchase [{format_num(Var.champ_cost)}]',auto_size_button=True, key= 'champion')],

        [sg.Text('', pad= (267,1)), sg.Text(f"❖{format_num(Var.diamonds)}", key= 'diamonds', font=('Leelawadee', 15), text_color= 'aqua')],

        [sg.Text(' ', pad= (0,100))],
        [sg.Text('', pad=(520,0)), sg.Button('Exit Game', size = (10, 1), button_color= 'red', mouseover_colors='darkred')]
        ]
window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= True, no_titlebar= False)    # main game window


# open menu window
Menu.menu_window()

# open main game window
Main.main_window(layout, window)

Click.crit()
Click.diamonds()