import PySimpleGUI as sg
import random as r
import time as t
import multiprocessing as mp

sg.theme('darkbrown2') 
sg.set_options(font=('Leelawadee UI', 12), element_padding=(0,0), keep_on_top= True)

next_multi_value = 1

# function to format big numbers
def format_num(number):
    
    prefixes = [
        (1e33, 'D'),  # Decillion
        (1e30, 'No'),  # Nonillion
        (1e27, 'Oc'),  # Octillion
        (1e24, 'Sp'),  # Septillion
        (1e21, 'Sx'),  # Sextillion
        (1e18, 'Qi'),  # Quintillion
        (1e15, 'Qa'),  # Quadrillion
        (1e12, 'T'),   # Trillion
        (1e9, 'B'),    # Billion
        (1e6, 'M'),    # Million
        (1e3, 'K')
    ]

    for prefix, symbol in prefixes:
        if abs(number) >= prefix:
            return f'{number / prefix:.2f}{symbol}'

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
    adept_cost = 3e4  # 30K
    rare_cost = 1e8   # 1M
    mythic_cost = 2e10   # 20B
    astral_cost = 1e11  # 100B
    celestial_cost = 5e11   # 500B
    eth_cost = 1e12    # 1T

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
    T2_cost = 500000    # 500K
    T3_cost = 2500000   # 2.5M
    T4_cost = 100000000 # 100M
    T5_cost = 1e9   # 1B
    T6_cost = 25e9  # 25B
    T7_cost = 1e11  # 100B

    # autoclicker value
    T1 = 10
    T2 = 0
    T3 = 0
    T4 = 0
    T5 = 0
    T6 = 0
    T7 = 0

    # currency
    diamonds = 0    # ❖
    count = 0
    random_count = r.randint(1, 200) # when to trigger diamond +

    # boss variables
    boss_hp = 10
    boss_trigger = r.randint(1,20)
    boss_click_count = 0
    boss_names = ['Grayskin', 'Crowspeak', 'Lightshorn', 'Vlad', 'One-Eye', 'Thornblight', 'Skinrender', 'Raverclaw', 'Dreadnaught', 'Morticia', 'Mordath', 'Wolftamer', 'Portent', 'Typhus', 'Corpsebreath', 'Marroweater', 'Archlich', 'Abolusha', 'Grendle', 'Polyphemus', 'Limper', 'Wintercall', 'Craven', 'Bramblejack', 'Hallowskull', 'Ferrous', 'Tempest', 'ScarRidge', 'Embergaze', 'Deathmire', 'Sylvanus', 'Kane', 'Tarsus', 'Ashencroft', 'Gluttonous', 'Damnerstake', 'Extraveous']
    boss_titles =  ['the Conqueror', 'Ragewalker', 'the Impaler', 'Heirtaker', "- the Reaper's Kiss", 'the Flameborne', 'the Deceiver', 'the Miser', '- Blesser of Pain', 'the Undefeated', 'Knightslayer', 'the Cannibal', 'Horsegutter', 'Skullgrinder', 'the Deathbringer', 'the Great Hammer', '- Oracle of Curses', 'Bloodmount', 'Hordemaster', 'Stormbringer', 'Faeriestalker', 'of the Black Stars', 'the Wicked', 'Fangbrood', 'the Corrupter', 'Bileblossom', '- Sunderer of Shields', 'the Branded', 'Wyrmtongue', 'Teardrinker', 'the Hobbled', 'the Dark Eye', 'Soulbinder', 'Blackheart', 'of the Iron Cage', 'the Patriarch']
    random_crit = r.randint(1,100)  # when to trigger crit (click value x10)

class Upgrade:
    
    tiers = {'basic':[Var.basic_cost, Var.basic, Var.click_basic, 'basic_value', Var.click_basic+1, Var.click_basic+40, 25, 200],
            'adept':[Var.adept_cost, Var.adept, Var.click_adept, 'adept_value', Var.click_adept+50, Var.click_adept+400, 100, 400],
            'rare':[Var.rare_cost, Var.rare, Var.click_rare, 'rare_value', Var.click_rare+500, Var.click_rare+2500, 5000, 600],
            'mythic':[Var.mythic_cost, Var.mythic, Var.click_mythic, 'mythic_value', Var.click_mythic+3000, Var.click_mythic+8e3, 100e3, 800],
            'astral':[Var.astral_cost, Var.astral, Var.click_astral, 'astral_value', Var.click_astral+10e3, Var.click_astral+300e3, 500e3, 1500],
            'celestial':[Var.celestial_cost, Var.celestial, Var.click_celestial, 'celestial_value', Var.click_celestial+500e3, Var.click_celestial+900e3, 1e6, 3000],
            'ethereal':[Var.eth_cost, Var.ethereal, Var.click_eth, 'eth_value', Var.click_eth+1e6, Var.click_eth+500e6, 50e6, 5000]}
    
    def Template(event, upgrade):
         if event == upgrade:
            if Var.click_value == 1:
                Var.click_value = 0 # because it was always +1

            if Var.click_count >= Upgrade.tiers[upgrade][0] * next_multi_value:

                Var.click_value -= Upgrade.tiers[upgrade][1]
                Upgrade.tiers[upgrade][1] += r.randint(Upgrade.tiers[upgrade][4] * next_multi_value, Upgrade.tiers[upgrade][5] * next_multi_value) 
                Upgrade.tiers[upgrade][2] += Upgrade.tiers[upgrade][6] * next_multi_value
                
                Var.click_value += Upgrade.tiers[upgrade][1]
                Var.click_count -= Upgrade.tiers[upgrade][0]
                
                Var.uc_rate += r.randint(100, Upgrade.tiers[upgrade][7]) * next_multi_value
                Upgrade.tiers[upgrade][0] += Var.uc_rate * next_multi_value
            
                window['COUNT'].update(format_num(Var.click_count))
                window[Upgrade.tiers[upgrade][3]].update(f'{format_num(Upgrade.tiers[upgrade][1])}')
                window[upgrade].update(f'Upgrade [{format_num(Upgrade.tiers[upgrade][0] * next_multi_value)}]', disabled=(True if Var.click_count < Upgrade.tiers[upgrade][0] else False))
                window['CLICK'].update(f'Click!\n[{format_num(Var.click_value)}]')
                
    def upgradeTimes(event, button):
        global next_multi_value
        if event == button:
            multi = {'x1': 1,
                    'x5': 5,
                    'x10': 10,
                    'x100': 100}

            keys = list(multi.keys())
            next_multi_index = (keys.index(window[button].ButtonText) + 1) % len(keys)
            next_multi_text = keys[next_multi_index]
            next_multi_value = multi[next_multi_text]
            window[button].update(next_multi_text)
            
            for upgrade in Upgrade.tiers:
                cost = Upgrade.tiers[upgrade][0] * next_multi_value
                window[upgrade].update(f'Upgrade [{format_num(cost)}]', disabled=(True if Var.click_count < cost else False))

# class Autos:
#     tiers = {'T1up' : [Var.T1, Var.T1_cost],  
#              'T2up' : [Var.T2, Var.T2_cost], 
#              'T3up' : [Var.T3, Var.T3_cost], 
#              'T4up' : [Var.T4, Var.T4_cost], 
#              'T5up' : [Var.T5, Var.T5_cost], 
#              'T6up' : [Var.T6, Var.T6_cost], 
#              'T7up' : [Var.T7, Var.T7_cost]}
#     def autoclick(event, T):    
#             for tier in Autos.tiers:
#                 Var.click_count += T
#                 t.sleep(1)
#                 window['COUNT'].update(f'{format_num(Var.click_count)}')
#                 if event in (sg.WIN_CLOSED, 'Exit Game'):
#                     break
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

                window['COUNT'].update(format_num(Var.click_count))
                window['CLICK'].update(button_color= color_r)
            
            if Var.boss_click_count == Var.boss_trigger:
                Boss.start_window()
            
            for upgrade in Upgrade.tiers:
                window[upgrade].update(disabled=(True if Var.click_count < Upgrade.tiers[upgrade][0] * next_multi_value else False))
                if event == upgrade:
                    Upgrade.Template(event, upgrade)
                    window[upgrade].update(disabled=(True if Var.click_count < Upgrade.tiers[upgrade][0] * next_multi_value else False))
                    
            Upgrade.upgradeTimes(event, 'multi')
            
            # for T in Autos.tiers:
            #     if event == T:
            #         Autos.autoclick(event, Autos.tiers[T])
            
        # diamonds trigger
            if Var.count == Var.random_count:
                diamonds_win = r.randint(1,100)
                Var.diamonds += diamonds_win
                
                sg.popup(f'+{diamonds_win}❖', text_color='aqua', auto_close= True, no_titlebar= True, auto_close_duration= 0.8, button_type= 5)
                Var.count = 0
                Var.random_count = r.randint(1,100)
                window['diamonds'].update(f'❖{format_num(Var.diamonds)}', font=('Leelawadee UI', 15), text_color= 'aqua')
                
        window.close()

        
class Boss:
    def start_window():
        
        sg.theme(r.choice(sg.theme_list())) # random theme each time
        boss_name = r.choice(Var.boss_names)+' '+r.choice(Var.boss_titles)
        boss_layout = [
            [sg.Text(pad=(0,1))],
            [sg.Text(pad = (110,0)),
            sg.Text(f'{boss_name}', text_color = sg.theme_text_color())],

            [sg.Text('', pad= (60,0)),
            sg.ProgressBar(Var.boss_hp, 'h', size=(25, 7), key='bossHP'),
            sg.Text(f' HP Left: {format_num(Var.boss_hp)}', key='bossHPvalue')],

            [sg.Text('', pad= (120,30)),
            sg.Button(f'Attack! [{format_num(Var.click_value)} DMG]', auto_size_button=True, key = 'Attack')],

            [sg.Text('', pad= (250,50)),sg.Button('Surrender', button_color= 'red')]
        ]
        boss_window = sg.Window(f'Boss Fight - {boss_name}', boss_layout, size=(600, 300), resizable = False, location=(450,270))
            
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
                window['diamonds'].update(f'❖{format_num(Var.diamonds)}', font=('Leelawadee UI', 15), text_color= 'aqua')
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

        [sg.Text(' ', pad= (225,1)), sg.Text('Welcome To Clicker Game GUI', font= ('Leelawadee UI', 15, 'bold'))],
        [sg.Text(' ', pad= (246,1)), sg.Text('By', font= ('Leelawadee UI', 15, 'bold')),
                                    sg.Text('Dragos Chelariu', font= ('Leelawadee UI', 15, 'italic'))],

        [sg.Text(' ')],
        [sg.Text(' ', pad = (250,1)), sg.Button('Start Game', size= (15,2), button_color='lightgreen', mouseover_colors='#099430', font= ('Leelawadee UI', 13,'bold'), key= 'Start')],

        [sg.Text(' ')],
        [sg.Text(' ', pad= (250,1)), sg.Button('Exit Game', size= (15,1), button_color= 'red', mouseover_colors='darkred', font= ('Leelawadee UI', 13))]
        ]

menu_window = sg.Window('Clicker Game GUI', menu_layout, size = (1200, 650), resizable= False, no_titlebar= True, location=(160,70))  # menu window

upgrades_column = [
    [sg.Text(pad=(0,15)),
    sg.Text(f'- Basic:', background_color='#4F3727', font=('Leelawadee UI', 13)),
    sg.Text(' 0', key= 'basic_value'),sg.Text('  '*7),
    sg.Button(f'Upgrade [{format_num(Var.basic_cost)}]', auto_size_button=True, key= 'basic', disabled = True, expand_x=False)],

    [sg.Text(pad=(0,15)),
    sg.Text('- Adept:', background_color='#48a8d0', font=('Leelawadee UI', 13)), 
    sg.Text(' 0', key= 'adept_value'), sg.Text('  '*6),
    sg.Button(f'Upgrade [{format_num(Var.adept_cost)}]', auto_size_button=True, key= 'adept', disabled = True)],

    [sg.Text(pad=(0,15)),
    sg.Text('- Rarefinder:',background_color='#12674a', font=('Leelawadee UI', 13)), 
    sg.Text(' 0', key= 'rare_value'), sg.Text(' '*4), 
    sg.Button(f'Upgrade [{format_num(Var.rare_cost)}]', auto_size_button=True, key= 'rare', disabled = True)],

    [sg.Text(pad=(0,15)),
    sg.Text('- Mythic:', background_color='#7851A9', font=('Leelawadee UI', 13)), 
    sg.Text(' 0', key= 'mythic_value'), sg.Text(' '*11), 
    sg.Button(f'Upgrade [{format_num(Var.mythic_cost)}]',auto_size_button=True, key= 'mythic', disabled = True)],

    [sg.Text(pad=(0,15)),
    sg.Text('- Astral:', background_color='#4B0082', font=('Leelawadee UI', 13)), 
    sg.Text(' 0', key= 'astral_value'), sg.Text(' '*13), 
    sg.Button(f'Upgrade [{format_num(Var.astral_cost)}]',auto_size_button=True, key= 'astral', disabled = True)],

    [sg.Text(pad=(0,15)),
    sg.Text('- Celestial:', background_color='#FFD700', font=('Leelawadee UI', 13), text_color='black'), 
    sg.Text(' 0', key= 'celestial_value'), sg.Text(' '*8), 
    sg.Button(f'Upgrade [{format_num(Var.celestial_cost)}]',auto_size_button=True, key= 'celestial', disabled = True)],

    [sg.Text(pad=(0,15)),
    sg.Text('- Ethereal:', background_color='#FFFFFF', font=('Leelawadee UI', 13), text_color='black'), 
    sg.Text(' 0', key= 'eth_value'), sg.Text(' '*8), 
    sg.Button(f'Upgrade [{format_num(Var.eth_cost)}]',auto_size_button=True, key= 'ethereal', disabled = True)],
]

autos_column = [
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 1: 0\t  ', key= 'T1val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T1_cost)}', key = 'T1up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 2: 0\t  ', key= 'T2val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T2_cost)}', key = 'T2up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 3: 0\t  ', key= 'T3val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T3_cost)}', key = 'T3up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 4: 0\t  ', key= 'T4val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T4_cost)}', key = 'T4up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 5: 0\t  ', key= 'T5val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T5_cost)}', key = 'T4up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 6: 0\t  ', key= 'T6val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T6_cost)}', key = 'T4up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))],
    [sg.Text('', pad= (15,15)), sg.Text('- Tier 7: 0\t  ', key= 'T7val', font=('Leelawadee UI', 12)), 
    sg.Button(f'❖{format_num(Var.T7_cost)}', key = 'T4up', auto_size_button=True, button_color= ('aqua', sg.theme_button_color_background()))]
]

clicker_column = [
    [sg.Text('Click Count: ', font= ('Leelawadee UI', 14, 'bold')), sg.Text(Var.click_count, font= ('Leelawadee UI', 14, 'bold'), size=(10, 1), key='COUNT')],
    [sg.Text()],
    [sg.Text(pad=(1,0)),sg.Button(f'Click!\n[{Var.click_value}]',font= ('Leelawadee UI', 12, 'bold'), key='CLICK', size= (12, 2))],
    [sg.Text()],
    [sg.Text(pad=(20,0)),
    sg.Text(f"❖{format_num(Var.diamonds)}", key= 'diamonds', font=('Leelawadee UI', 15), text_color= 'aqua')]
]

layout = [
    [sg.Text(pad=(0,5))],
    [sg.Text('', pad = (40,0)),sg.Text('AutoClickers', font= ('Leelawadee UI', 14, 'bold'), background_color= '#4a87a8'),
    sg.Text('', pad = (135,0)), sg.Text('Clicker Game GUI', font= ('Leelawadee UI', 16, 'bold'), background_color= '#e6a23e'),
    sg.Text('', pad = (135,0)),sg.Text('Upgrades', font= ('Leelawadee UI', 14, 'bold'), background_color= '#bb8af2', key= 'upv'),
    sg.Text(pad = (10,0)),
    sg.Button('x1', key='multi', auto_size_button=True, size = (5,1))],

    [sg.Text()],
    [sg.HorizontalSeparator()],
    [sg.Text()],

    [sg.Text(pad=(10,0)),sg.Column(autos_column),
    sg.Text(pad=(40,0)),
    sg.VerticalSeparator(),
    sg.Text(pad=(90,0)),
    sg.Column(clicker_column),
    sg.Text(pad=(40,0)),
    sg.VerticalSeparator(),
    sg.Text(pad=(20,0)),
    sg.Column(upgrades_column)],

    [sg.Text(' ', pad= (0, 25))],
    [sg.Text('', pad=(520,0)),
    sg.Button('Exit Game', size = (10, 1), button_color= 'red', mouseover_colors='darkred')]
]

window = sg.Window('Clicker Game GUI', layout, size = (1200, 650), resizable= False, no_titlebar= True, location=(160,70))

# open menu window
Menu.menu_window(menu_layout, menu_window)

# open main game window
Main.main_window(layout, window)