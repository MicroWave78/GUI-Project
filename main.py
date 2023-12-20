import PySimpleGUI as sg
import random as r
import time as t
import multiprocessing as mp
import concurrent.futures
import itertools

sg.theme('darkbrown2') 
sg.set_options(font=('Leelawadee', 12), element_padding=(0,0), keep_on_top= True)

# function to format big numbers
def format_num(number):
    if abs(number) >= 1e33:
        return f'{number / 1e33:.2f}D'  # Decillion
    if abs(number) >= 1e30:
        return f'{number / 1e30:.2f}No' # Nonillion
    if abs(number) >= 1e27:
        return f'{number / 1e27:.2f}Oc' # Octillion
    if abs(number) >= 1e24:
        return f'{number / 1e24:.2f}Sp' # Septillion
    if abs(number) >= 1e21:
        return f'{number / 1e21:.2f}Sx' # Sextillion
    if abs(number) >= 1e18:
        return f'{number / 1e18:.2f}Qi' # Quintillion
    if abs(number) >= 1e15:
        return f'{number / 1e15:.2f}Qa' # Quadrillion
    elif abs(number) >= 1e12:
        return f'{number / 1e12:.2f}T'  # Trillion
    elif abs(number) >= 1e9:
        return f'{number / 1e9:.2f}B'   # Billion
    elif abs(number) >= 1e6:
        return f'{number / 1e6:.2f}M'   # Million
    elif abs(number) >= 1e3:
        return f'{number / 1e3:.2f}K'
    else:
        return number

class Var:
    click_count = 0
    click_value = 1 #click rate
    click_crit = 0


    # upgrades value
    basic = 0
    adept = 0
    mythic = 0
    rare = 0
    astral = 0
    celestial = 0
    ethereal = 0
    uc_rate = 8 #upgrade cost ++

    # upgrades cost
    basic_cost = 50
    adept_cost = 30000  # 30K
    rare_cost = 100000000   # 1M
    mythic_cost = 20000000000   # 20B
    astral_cost = 100000000000  # 100B
    celestial_cost = 500000000000   # 500B
    eth_cost = 1000000000000    # 1T

    # upgrades click rate
    click_basic = 1
    click_adept = 1
    click_mythic = 1
    click_rare = 1
    click_astral = 1
    click_celestial = 1
    click_eth = 1

    # autoclicker tiers cost
    T1_cost = 2500
    T2_cost = 500000
    T3_cost = 2500000
    T4_cost = 100000000

    # autoclicker value
    T1 = 10
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

class Autos:
    def auto(T):
        while True:
            Var.click_count += T
            window['COUNT'].update(f'{format_num(Var.click_count)}')
            t.sleep(1)
            if Main.event in (sg.WIN_CLOSED, 'Exit Game'):
                break

class Menu:
    check_play = True

    def menu_window(menu_layout, menu_window):
        
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

            if Var.click_crit == Var.random_crit:
                Var.click_count += Var.click_value*10
                sg.popup('Crit!', auto_close=True, no_titlebar= True, auto_close_duration= 0.2, button_type=5, text_color= 'gold')
                Var.click_crit = 0
                Var.random_crit = r.randint(1,100)

            if event == 'CLICK':
                Var.click_count += Var.click_value
                Var.count += 1  # clicks to diamond trigger
                Var.boss_click_count += 1
                Var.click_crit += 1
                print(Var.boss_click_count)
                print(Var.boss_trigger)

                window['COUNT'].update(format_num(Var.click_count))
                window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]', button_color= color_r)

            if Var.boss_click_count == Var.boss_trigger:
                Boss.start_window()

            elif event == 'basic':
                if Var.click_count >= Var.basic_cost:

                    Var.click_value -= Var.basic
                    Var.basic += r.randint(Var.click_basic+1, Var.click_basic+40)
                    Var.click_basic += 25

                    Var.click_value += Var.basic
                    Var.click_count -= Var.basic_cost
                    
                    Var.uc_rate += r.randint(100, 700)
                    Var.basic_cost += Var.uc_rate
                    

                    window['COUNT'].update(format_num(Var.click_count))
                    window['basic_value'].update(f' {format_num(Var.basic+1)}')
                    window['basic'].update(f'Upgrade [{format_num(Var.basic_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # adept upgrade
            elif event == 'adept':
                if Var.click_count >= Var.adept_cost:

                    Var.click_value -= Var.adept
                    Var.adept += r.randint(Var.click_adept+5, Var.click_adept+90)
                    Var.click_adept += 40

                    Var.click_value += Var.adept
                    Var.click_count -= Var.adept_cost

                    Var.uc_rate += r.randint(1e3, 3e3)
                    Var.adept_cost += Var.uc_rate

                    window['COUNT'].update(format_num(Var.click_count))
                    window['adept_value'].update(f' {format_num(Var.adept)}')
                    window['adept'].update(f'Upgrade [{format_num(Var.adept_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # rare upgrade
            elif event == 'rare':
                if Var.click_count >= Var.rare_cost:

                    Var.click_value -= Var.rare
                    Var.rare += r.randint(Var.click_rare+10, Var.click_rare+120)
                    Var.click_rare += 100

                    Var.click_value += Var.rare
                    Var.click_count -= Var.rare_cost

                    Var.uc_rate += r.randint(5e3, 1e4)
                    Var.rare_cost += Var.uc_rate
                    
                    window['COUNT'].update(format_num(Var.click_count))
                    window['rare_value'].update(f' {format_num(Var.rare)}')
                    window['rare'].update(f'Upgrade [{format_num(Var.rare_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # mythic upgrade
            elif event == 'mythic':
                if Var.click_count >= Var.mythic_cost:

                    Var.click_value -= Var.mythic
                    Var.mythic += r.randint(Var.click_mythic+20, Var.click_mythic+250)
                    Var.click_mythic += 300

                    Var.click_value += Var.mythic
                    Var.click_count -= Var.mythic_cost

                    Var.uc_rate += r.randint(1e4, 1e6)    # 10k, 1m
                    Var.mythic_cost += Var.uc_rate

                    window['COUNT'].update(format_num(Var.click_count))
                    window['mythic_value'].update(f' {format_num(Var.mythic)}')
                    window['mythic'].update(f'Upgrade [{format_num(Var.mythic_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # astral upgrade
            elif event == 'astral':
                if Var.click_count >= Var.astral_cost:

                    Var.click_value -= Var.astral
                    Var.astral += r.randint(Var.click_astral+50, Var.click_astral+900)
                    Var.click_astral += 500

                    Var.click_value += Var.astral
                    Var.click_count -= Var.astral_cost
                    
                    Var.uc_rate += r.randint(1e6, 8e6)    # 1m, 8m
                    Var.astral_cost += Var.uc_rate
                    

                    window['COUNT'].update(format_num(Var.click_count))
                    window['astral_value'].update(f' {format_num(Var.astral)}')
                    window['astral'].update(f'Upgrade [{format_num(Var.astral_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # celestial upgrade
            elif event == 'celestial':
                if Var.click_count >= Var.celestial_cost:

                    Var.click_value -= Var.celestial
                    Var.celestial += r.randint(Var.click_celestial+100, Var.click_celestial+2500)
                    Var.click_celestial += 1000

                    Var.click_value += Var.celestial
                    Var.click_count -= Var.celestial_cost
                    
                    Var.uc_rate += r.randint(1e7, 5e7)  # 10m, 50m
                    Var.celestial_cost += Var.uc_rate

                    window['COUNT'].update(format_num(Var.click_count))
                    window['mythic_value'].update(f' {format_num(Var.mythic)}')
                    window['mythic'].update(f'Upgrade [{format_num(Var.mythic_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

        # ethereal upgrade
            elif event == 'ethereal':
                if Var.click_count >= Var.eth_cost:

                    Var.click_value -= Var.ethereal
                    Var.ethereal += r.randint(Var.click_eth+500, Var.click_eth+4000)
                    Var.click_eth += 1000

                    Var.click_value += Var.ethereal
                    Var.click_count -= Var.eth_cost
                    
                    Var.uc_rate += r.randint(1e8, 5e8)  # 100m, 500m
                    Var.eth_cost += Var.uc_rate
                    

                    window['COUNT'].update(format_num(Var.click_count))
                    window['eth_value'].update(f' {format_num(Var.ethereal)}')
                    window['ethereal'].update(f'Upgrade [{format_num(Var.eth_cost)}]')
                    window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')

            elif event == 'T1up':
                executor = concurrent.futures.ProcessPoolExecutor(1)
                futures = executor.submit(Autos.auto, Var.T1)
                concurrent.futures.wait(futures)
                

        # diamonds trigger
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
        boss_name = r.choice(Var.boss_names)+' '+r.choice(Var.boss_titles)
        boss_layout = [
            [sg.Text(pad=(0,1))],
            [sg.Text(pad = (110,0)),
             sg.Text(f'{boss_name}', background_color= '#D01C1F')],

            [sg.Text('', pad= (60,0)),
            sg.ProgressBar(Var.boss_hp, 'h', size=(25, 7), key='bossHP'),
            sg.Text(f' HP Left: {format_num(Var.boss_hp)}', key='bossHPvalue')],

            [sg.Text('', pad= (120,30)),
            sg.Button(f'Attack! [{format_num(Var.click_value)} DMG]', auto_size_button=True, key = 'Attack')],

            [sg.Text('', pad= (250,50)),sg.Button('Surrender', button_color= 'red')]
        ]
        boss_window = sg.Window(f'{boss_name}', boss_layout, size=(600, 300), resizable= False, auto_close= True)
            
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

upgrades_column = [
    [sg.Text(pad=(0,15)),
     sg.Text(f'- Basic:', background_color='#4F3727', font=('Leelawadee', 13)),
     sg.Text(' 0', key= 'basic_value'),sg.Text('  '*7),
     sg.Button(f'Purchase [{format_num(Var.basic_cost)}]',disabled=[True if Var.click_count < Var.basic_cost else False], auto_size_button=True, key= 'basic')],

     [sg.Text(pad=(0,15)),
      sg.Text('- Adept:', background_color='#48a8d0', font=('Leelawadee', 13)), 
      sg.Text(' 0', key= 'adept_value'), sg.Text('  '*6),
      sg.Button(f'Purchase [{format_num(Var.adept_cost)}]', auto_size_button=True, key= 'adept')],

    [sg.Text(pad=(0,15)),
     sg.Text('- Rarefinder:',background_color='#12674a', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'rare_value'), sg.Text(' '*4), 
     sg.Button(f'Purchase [{format_num(Var.rare_cost)}]', auto_size_button=True, key= 'rare')],

    [sg.Text(pad=(0,15)),
     sg.Text('- Mythic:', background_color='#7851A9', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'mythic_value'), sg.Text(' '*11), 
     sg.Button(f'Purchase [{format_num(Var.mythic_cost)}]',auto_size_button=True, key= 'mythic')],

    [sg.Text(pad=(0,15)),
     sg.Text('- Astral:', background_color='#4B0082', font=('Leelawadee', 13)), 
     sg.Text(' 0', key= 'astral_value'), sg.Text(' '*13), 
     sg.Button(f'Purchase [{format_num(Var.astral_cost)}]',auto_size_button=True, key= 'astral')],

    [sg.Text(pad=(0,15)),
     sg.Text('- Celestial:', background_color='#FFD700', font=('Leelawadee', 13), text_color='black'), 
     sg.Text(' 0', key= 'celestial_value'), sg.Text(' '*8), 
     sg.Button(f'Purchase [{format_num(Var.celestial_cost)}]',auto_size_button=True, key= 'celestial')],

    [sg.Text(pad=(0,15)),
     sg.Text('- Ethereal:', background_color='#FFFFFF', font=('Leelawadee', 13), text_color='black'), 
     sg.Text(' 0', key= 'eth_value'), sg.Text(' '*8), 
     sg.Button(f'Purchase [{format_num(Var.eth_cost)}]',auto_size_button=True, key= 'ethereal')],
]

autos_column = [
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 1: 0\t  ', key= 'T1val', font=('Leelawadee', 12)), 
     sg.Button(f'❖{format_num(Var.T1_cost)}', key = 'T1up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 2: 0\t  ', key= 'T2val', font=('Leelawadee', 12)), 
     sg.Button(f'❖{format_num(Var.T2_cost)}', key = 'T2up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 3: 0\t  ', key= 'T3val', font=('Leelawadee', 12)), 
     sg.Button(f'❖{format_num(Var.T3_cost)}', key = 'T3up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 4: 0\t  ', key= 'T4val', font=('Leelawadee', 12)), 
     sg.Button(f'❖{format_num(Var.T4_cost)}', key = 'T4up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))]
]

clicker_column = [
    [sg.Text(pad=(0,0))],
    [sg.Text('Click Count: ', font= ('Leelawadee', 14, 'bold')), sg.Text(Var.click_count, font= ('Leelawadee', 14, 'bold'), size=(10, 1), key='COUNT')],
    [sg.Text()],
    [sg.Text(pad=(1,0)),sg.Button(f'Click!\n[{Var.click_value}]',font= ('Leelawadee', 12, 'bold'), key='CLICK', size= (12, 2))],
    [sg.Text()],
    [sg.Text(pad=(18,0)),
     sg.Text(f"❖{format_num(Var.diamonds)}", key= 'diamonds', font=('Leelawadee', 15), text_color= 'aqua')]
]

layout = [
        [sg.Text(pad=(0,5))],
        [sg.Text('', pad = (50,0)),sg.Text('AutoClickers:', font= ('Leelawadee', 14, 'bold'), background_color= '#4a87a8'),
         sg.Text('', pad = (120,0)), sg.Text('Clicker Game GUI', font= ('Leelawadee', 16, 'bold'), background_color= '#e6a23e'),
         sg.Text('', pad = (140,0)),sg.Text('Upgrades', font= ('Leelawadee', 14, 'bold'), background_color= '#bb8af2', key= 'upv')],

        [sg.Text()],
        [sg.HorizontalSeparator()],
        [sg.Text()],

        [sg.Column(autos_column),
         sg.Text(pad=(143,0)),
         sg.Column(clicker_column),
         sg.Text(pad=(50,0)),
         sg.Column(upgrades_column)],

        [sg.Text(' ', pad= (0,15))],
        [sg.Text('', pad=(520,0)),
         sg.Button('Exit Game', size = (10, 1), button_color= 'red', mouseover_colors='darkred')]
    ]

window = sg.Window('Clicker Game GUI', layout, size = (1200, 600), resizable= False, no_titlebar= False)    # main game window


# open menu window
Menu.menu_window(menu_layout, menu_window)

# open main game window
Main.main_window(layout, window)