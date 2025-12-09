import random #random generation
import time #for slow print effect
import os #for color

#for color application in terminal
os.system('') 

RED = "\033[91m" #hp
BLUE = "\033[94m" #mp 
PURPLE = "\033[95m" #boss
YELLOW = "\033[93m" #rank
RESET = "\033[0m" #default

GAME_WIDTH = 60 #default game terminal width for formatting 


def slow_print(text, delay=0.03, newline=True):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    if newline:
        print()

#player data structure
player = {
    "name": "",
    "rank": "Rookie",
    "health": 120,
    "max_health": 120,
    "mana": 60,
    "max_mana": 60,
    "attack": 15,
    "defense": 5,
    "inventory": [],
    "gold": 100,
    "level": 1,
    "experience": 0,
    "skills": [
        {"name": "Power Strike", "cost": 10, "dmg_mult": 1.5, "type": "dmg"},
        {"name": "Double Slash", "cost": 20, "dmg_mult": 2.2, "type": "dmg"},
        {"name": "Holy Light", "cost": 30, "heal": 40, "type": "heal"},
        {"name": "Ultimate Nuke", "cost": 50, "dmg_mult": 4.0, "type": "dmg"}
    ]
}

#world data with mobs, bosses and the specific locations
world_data = {
    "Forest": {
        "mobs": [
            {"name": "Slime", "health": 20, "attack": 4, "defense": 0, "gold": 5, "exp": 10},
            {"name": "Wild Wolf", "health": 35, "attack": 8, "defense": 1, "gold": 10, "exp": 18},
            {"name": "Goblin Scavenger", "health": 40, "attack": 6, "defense": 2, "gold": 15, "exp": 18},
            {"name": "Orc Grunt", "health": 55, "attack": 10, "defense": 4, "gold": 25, "exp": 25},
            {"name": "Forest Bear", "health": 70, "attack": 12, "defense": 8, "gold": 40, "exp": 35},
            {"name": "Bandit", "health": 45, "attack": 11, "defense": 3, "gold": 30, "exp": 25},
        ],
        "boss": {"name": "Forest Hydra", "health": 350, "attack": 25, "defense": 10, "gold": 600, "exp": 500}
    },
    "Cave": {
        "mobs": [
            {"name": "Giant Bat", "health": 50, "attack": 14, "defense": 2, "gold": 35, "exp": 30},
            {"name": "Rock Basilisk", "health": 80, "attack": 18, "defense": 15, "gold": 65, "exp": 55},
            {"name": "Cave Troll", "health": 120, "attack": 25, "defense": 5, "gold": 80, "exp": 70},
            {"name": "Deep Spider", "health": 60, "attack": 20, "defense": 4, "gold": 50, "exp": 45},
            {"name": "Kobold Miner", "health": 55, "attack": 12, "defense": 8, "gold": 90, "exp": 40},
        ],
        "boss": {"name": "Crystal Warden", "health": 550, "attack": 50, "defense": 30, "gold": 1200, "exp": 900}
    },
    "Village": {
        "mobs": [
            {"name": "Possessed Villager", "health": 60, "attack": 15, "defense": 4, "gold": 50, "exp": 40},
            {"name": "Revenant", "health": 80, "attack": 20, "defense": 10, "gold": 100, "exp": 60},
            {"name": "Witch", "health": 65, "attack": 35, "defense": 2, "gold": 130, "exp": 80},
            {"name": "Cursed Dog", "health": 50, "attack": 18, "defense": 5, "gold": 40, "exp": 35},
            {"name": "Headless Horseman", "health": 110, "attack": 28, "defense": 12, "gold": 180, "exp": 100},
        ],
        "boss": {"name": "Hallow Man", "health": 700, "attack": 60, "defense": 15, "gold": 2000, "exp": 1500}
    },
    "Castle Ruins": {
        "mobs": [
            {"name": "Skeleton Warrior", "health": 90, "attack": 22, "defense": 12, "gold": 110, "exp": 90},
            {"name": "Spectral Knight", "health": 130, "attack": 30, "defense": 25, "gold": 220, "exp": 180},
            {"name": "Gargoyle", "health": 110, "attack": 25, "defense": 30, "gold": 160, "exp": 140},
            {"name": "Dark Mage", "health": 80, "attack": 45, "defense": 5, "gold": 250, "exp": 200},
            {"name": "Ironclad Golem", "health": 180, "attack": 28, "defense": 40, "gold": 300, "exp": 250},
        ],
        "boss": {"name": "Corrupted Gargoyle", "health": 1200, "attack": 75, "defense": 50, "gold": 4000, "exp": 3000}
    },
    "Dark Swamp": {
        "mobs": [
            {"name": "Mudshroud", "health": 150, "attack": 35, "defense": 15, "gold": 300, "exp": 280},
            {"name": "Siren", "health": 120, "attack": 50, "defense": 10, "gold": 400, "exp": 350},
            {"name": "Bog Raptor", "health": 140, "attack": 45, "defense": 10, "gold": 350, "exp": 320},
            {"name": "Abyssal Worm", "health": 250, "attack": 30, "defense": 40, "gold": 500, "exp": 400},
            {"name": "Gromp", "health": 300, "attack": 25, "defense": 50, "gold": 450, "exp": 450},
        ],
        "boss": {"name": "Behemoth", "health": 5000, "attack": 120, "defense": 80, "gold": 15000, "exp": 10000}
    },
}

#reward system for ranks let's goooo
rank_rewards_data = {
    "Scout": [ 
        {"name": "Health Potion", "type": "heal", "value": 50, "price": 0},
        {"name": "Mana Potion", "type": "mana", "value": 30, "price": 0},
        {"name": "Scout's Allowance", "gold": 100}
    ],
    "Soldier": [
        {"name": "Iron Sword", "type": "weapon", "value": 5, "price": 50}, 
        {"name": "Minor Strength Potion", "type": "buff_str", "value": 2, "price": 50}
    ],
    "Adventurer": [
        {"name": "Steel Shield", "type": "armor", "value": 5, "price": 100},
        {"name": "Major Strength Potion", "type": "buff_str", "value": 5, "price": 150},
        {"name": "Adventurer's Stipend", "gold": 150}
    ],
    "Veteran": [
        {"name": "Steel Armor", "type": "armor", "value": 10, "price": 200},
        {"name": "Survival Pouch", "gold": 250}
    ],
    "Knight": [ 
        {"name": "Gold Sword", "type": "weapon", "value": 10, "price": 150},
        {"name": "Honor Pouch", "gold": 400}
    ],
    "Elite": [
        {"name": "Gold Armor", "type": "armor", "value": 20, "price": 500},
        {"name": "Greater Health Potion", "type": "heal", "value": 100, "price": 50}
    ],
    "Champion": [ 
        {"name": "Platinum Sword", "type": "weapon", "value": 20, "price": 400},
        {"name": "Mega Strength Potion", "type": "buff_str", "value": 10, "price": 400}
    ],
    "Warlord": [ 
        {"name": "Diamond Armor", "type": "armor", "value": 40, "price": 1500},
        {"name": "War Chest", "gold": 1000}
    ],
    "Hero": [ 
        {"name": "Diamond Sword", "type": "weapon", "value": 35, "price": 1000},
        {"name": "Hero's Bounty", "gold": 2000}
    ],
    "Master": [ 
        {"name": "Black Diamond Armor", "type": "armor", "value": 70, "price": 4000},
        {"name": "Superior Health Potion", "type": "heal", "value": 200, "price": 120}
    ],
    "Legend": [
        {"name": "Excalibur", "type": "weapon", "value": 80, "price": 5000},
        {"name": "Legendary Treasure", "gold": 5000}
    ],
    "Mythic": [ 
        {"name": "Cosmic Sword", "type": "weapon", "value": 150, "price": 10000},
        {"name": "Godly Power", "gold": 99999}
    ]
}

locations = list(world_data.keys())
# shop items data
shop_items_inventory = [
    # potions
    {"name": "Health Potion", "type": "heal", "value": 50, "price": 20},
    {"name": "Greater Health Potion", "type": "heal", "value": 100, "price": 50},
    {"name": "Superior Health Potion", "type": "heal", "value": 200, "price": 120},
    {"name": "Mana Potion", "type": "mana", "value": 30, "price": 30},
    {"name": "Greater Mana Potion", "type": "mana", "value": 70, "price": 70},
    {"name": "Minor Strength Potion", "type": "buff_str", "value": 2, "price": 50},
    {"name": "Major Strength Potion", "type": "buff_str", "value": 5, "price": 150},
    {"name": "Mega Strength Potion", "type": "buff_str", "value": 10, "price": 400},

    # scrolls
    {"name": "Fireball Scroll", "type": "scroll", "value": 50, "price": 100},
    {"name": "Lightning Scroll", "type": "scroll", "value": 150, "price": 300},
    {"name": "Meteor Scroll", "type": "scroll", "value": 300, "price": 800},

    # weapons
    {"name": "Iron Sword", "type": "weapon", "value": 5, "price": 50},
    {"name": "Gold Sword", "type": "weapon", "value": 10, "price": 150},
    {"name": "Platinum Sword", "type": "weapon", "value": 20, "price": 400},
    {"name": "Diamond Sword", "type": "weapon", "value": 35, "price": 1000},
    {"name": "Adamantite Sword", "type": "weapon", "value": 55, "price": 2500},
    {"name": "Excalibur", "type": "weapon", "value": 80, "price": 5000},
    {"name": "Cosmic Sword", "type": "weapon", "value": 150, "price": 10000},

    # armors
    {"name": "Cloth Tunic", "type": "armor", "value": 2, "price": 20},
    {"name": "Steel Armor", "type": "armor", "value": 10, "price": 200},
    {"name": "Gold Armor", "type": "armor", "value": 20, "price": 500},
    {"name": "Diamond Armor", "type": "armor", "value": 40, "price": 1500},
    {"name": "Black Diamond Armor", "type": "armor", "value": 70, "price": 4000},

    # shields
    {"name": "Steel Shield", "type": "armor", "value": 5, "price": 100},
    {"name": "Bone Keeper", "type": "armor", "value": 15, "price": 600},
    {"name": "Eclipse", "type": "armor", "value": 30, "price": 2000},
    {"name": "Oblivion", "type": "armor", "value": 50, "price": 5000},
]

game_running = True
current_location = "Forest"


#main game function

def get_player_name():
    print("\n" * 2)
    print("=" * GAME_WIDTH)
    print("PHANTOM SAGA".center(GAME_WIDTH))
    print("=" * GAME_WIDTH)
    slow_print("One must prepare for the glory and dangers".center(GAME_WIDTH))
    print("=" * GAME_WIDTH)
    name = input(f"\n Enter your hero's name > ")
    if not name.strip():
        name = "Unknown Hero"
    player["name"] = name
    print()
    print("=" * GAME_WIDTH)
    slow_print(f"Welcome, {player['name']}! Your destiny awaits.".center(GAME_WIDTH))
    print("=" * GAME_WIDTH)
    time.sleep(1)


def show_status():
    print()
    print("-" * GAME_WIDTH)
    print("HERO STATUS".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)
    
    print(f" Name: {player['name']} ({YELLOW}{player['rank']:}{RESET}){'':<7} Level: {player['level']}")
    
    print(f" {RED}HP{RESET}:   {player['health']}/{player['max_health']:<16} Gold:  {player['gold']}")
    print(f" {BLUE}MP{RESET}:   {player['mana']}/{player['max_mana']:<17} EXP:   {player['experience']}/{player['level'] * 100}")
    
    print(f" ATK:  {player['attack']:<20} DEF:   {player['defense']}")
    print("-" * GAME_WIDTH)

    print("[ INVENTORY ]".center(GAME_WIDTH))
    if not player["inventory"]:
        print("(Empty)".center(GAME_WIDTH))
    else:
        inv_counts = {}
        for item in player["inventory"]:
            inv_counts[item['name']] = inv_counts.get(item['name'], 0) + 1
        items_list = [f"{name} x{count}" for name, count in inv_counts.items()]
        print(", ".join(items_list).center(GAME_WIDTH))

    print("-" * GAME_WIDTH)
    print("[ SKILLS ]".center(GAME_WIDTH))
    
    for skill in player['skills']:
        skill_display = f"{skill['name']} ({skill['cost']} {BLUE}MP{RESET})"
        
        raw_text = f"{skill['name']} ({skill['cost']} MP)"
        gap = (GAME_WIDTH - len(raw_text)) // 2
        
        print(" " * gap + skill_display)

    print("=" * GAME_WIDTH)


def level_up():
    exp_to_level = player["level"] * 100
    if player["experience"] >= exp_to_level:
        player["level"] += 1
        player["max_health"] += 30
        player["max_mana"] += 15
        player["attack"] += 7
        player["defense"] += 4
        player["health"] = player["max_health"]
        player["mana"] = player["max_mana"]
        player["experience"] -= exp_to_level
        update_rank()

        print()
        print("*" * GAME_WIDTH)
        print(f"*** LEVEL UP! You are now level {player['level']}!  ***".center(GAME_WIDTH))
        print(f"Stats Increased! {RED}HP{RESET}/{BLUE}MP{RESET} Refilled!".center(GAME_WIDTH + 18))
        print("*" * GAME_WIDTH)
        print()
        time.sleep(1)
        show_status()

#function for ranking system
def update_rank():
    old_rank = player.get("rank", "Rookie")
    lvl = player["level"]
    new_rank = old_rank 

    if lvl < 5:
        new_rank = "Rookie"
    elif lvl < 10:
        new_rank = "Scout"
    elif lvl < 15:
        new_rank = "Soldier"
    elif lvl < 20:
        new_rank = "Adventurer"
    elif lvl < 25:
        new_rank = "Veteran"
    elif lvl < 30:
        new_rank = "Knight"
    elif lvl < 35:
        new_rank = "Elite"
    elif lvl < 40:
        new_rank = "Champion"
    elif lvl < 45:
        new_rank = "Warlord"
    elif lvl < 50:
        new_rank = "Hero"
    elif lvl < 60:
        new_rank = "Master"
    elif lvl < 85:
        new_rank = "Legends"
    else:
        new_rank = "Mythic"

    if new_rank != old_rank:
        player["rank"] = new_rank 
        
        if new_rank in rank_rewards_data:
            print()
            print("+" * GAME_WIDTH)
            print(f" CONGRATULATIONS! RANK UP: {YELLOW}{new_rank.upper()}{RESET} ".center(GAME_WIDTH))
            print("+" * GAME_WIDTH)
            time.sleep(0.5)
            
            rewards = rank_rewards_data[new_rank]
            for item in rewards:
                if "gold" in item:
                    player["gold"] += item["gold"]
                    print(f" > Reward: {YELLOW}{item['name']} ({item['gold']} G){RESET}".center(GAME_WIDTH))
                else:
                    player["inventory"].append(item.copy())
                    print(f" > Reward: {BLUE}{item['name']}{RESET}".center(GAME_WIDTH))
                time.sleep(0.3)
            
            print("+" * GAME_WIDTH)
            print()
            input(" Press Enter to continue... ")

#function for option 2 in game menu
def choose_location():
    print()
    print("-" * GAME_WIDTH)
    print("TRAVEL MAP".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)
    print("Where would you like to go?".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)
    for idx, loc in enumerate(locations, 1):
        print(f" {idx}. {loc}")
    print("-" * GAME_WIDTH)

    choice = input(f"\n Choose a location number > ")
    if choice.isdigit() and 1 <= int(choice) <= len(locations):
        return locations[int(choice) - 1]
    else:
        slow_print("Invalid choice. Staying at current location.")
        return None


def encounter_enemy(location_name):
    location_data = world_data[location_name]

    if random.random() < 0.05:
        enemy_template = location_data["boss"]
        is_boss = True
    else:
        enemy_template = random.choice(location_data["mobs"])
        is_boss = False

    enemy = enemy_template.copy()

    if player['level'] > 1:
        level_mult = player['level'] - 1
        enemy['health'] += int(level_mult * 8)
        enemy['attack'] += int(level_mult * 1.5)
        enemy['gold'] += int(level_mult * 3)
        enemy['exp'] += int(level_mult * 4)

    if is_boss:
        print()
        print("!" * GAME_WIDTH)
        print(f"{PURPLE}{'!!! BOSS ENCOUNTER !!!'.center(GAME_WIDTH)}{RESET}")
        print(f"{PURPLE}{f'The {enemy['name']} has appeared!'.center(GAME_WIDTH)}{RESET}")
        print("!" * GAME_WIDTH)
    else:
        print("-" * GAME_WIDTH)
        slow_print(f"A wild {enemy['name']} appears!")

    battle(enemy, is_boss=is_boss)

def use_skill(enemy):
    print()
    print("-" * GAME_WIDTH)
    print("SKILLS MENU".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)

    for idx, skill in enumerate(player["skills"], 1):
        desc = ""
        if skill["type"] == "dmg":
            desc = f"Deals {skill['dmg_mult']}x Dmg"
        elif skill["type"] == "heal":
            desc = f"Heals {skill['heal']} {RED}HP{RESET}"

        print(f" {idx}. {skill['name']:<15} | Cost: {skill['cost']} {BLUE}MP{RESET} | {desc}")

    print(" 0. Cancel")
    choice = input(f"\n Choose skill > ")

    if choice == "0":
        return False

    if choice.isdigit() and 1 <= int(choice) <= len(player["skills"]):
        skill = player["skills"][int(choice) - 1]

        if player["mana"] >= skill["cost"]:
            player["mana"] -= skill["cost"]

            if skill["type"] == "dmg":
                dmg = int(player["attack"] * skill["dmg_mult"])
                enemy["health"] -= dmg
                slow_print(f" > Used {skill['name']}! BLAM! Dealt {dmg} damage!")
                return True

            elif skill["type"] == "heal":
                amount = skill["heal"]
                player["health"] = min(player["max_health"], player["health"] + amount)
                slow_print(f" > Used {skill['name']}! Healed {amount} {RED}HP{RESET}!")
                return True
        else:
            slow_print(" > Not enough Mana!")
            return False
    else:
        slow_print("Invalid choice!")
        return False


def battle(enemy, is_boss=False):
    global current_location, game_running

    while enemy["health"] > 0 and player["health"] > 0:
        print()
        print("-" * GAME_WIDTH)
        
        enemy_name = enemy['name'].upper()
        name_color = PURPLE if is_boss else ""
        enemy_str = f"{name_color}{enemy_name}{RESET} ({RED}HP: {enemy['health']}{RESET})"
        
        player_str = f"{player['name']} ({RED}HP: {player['health']}{RESET} | {BLUE}MP: {player['mana']}{RESET})"
        raw_enemy = f"{enemy['name']} (HP: {enemy['health']})"
        raw_player = f"{player['name']} (HP: {player['health']} | MP: {player['mana']})"
        
        gap = GAME_WIDTH - len(raw_enemy) - len(raw_player) - 2
        if gap < 2: gap = 2

        print(f" {enemy_str}" + " " * gap + f"{player_str}")
        print("-" * GAME_WIDTH)

        print(" 1. Attack")
        print(" 2. Skills")
        print(" 3. Use Item")
        print(" 4. Run")

        choice = input(f"\n Choose Action > ")
        player_turn_done = False

        if choice == "1":
            damage = max(1, player["attack"] - enemy["defense"])
            enemy["health"] -= damage
            slow_print(f" > You hit {enemy['name']} for {damage} damage!")
            player_turn_done = True

        elif choice == "2":
            used = use_skill(enemy)
            if used:
                player_turn_done = True

        elif choice == "3":
            used = use_item(enemy)
            if used:
                player_turn_done = True

        elif choice == "4":
            if is_boss:
                #chance to escape boss
                if random.random() < 0.30:
                    slow_print(f" > Miraculously, you escaped the {enemy['name']}!")
                    return #exit
                else:
                    slow_print(f" > Failed to escape the Boss! (Luck: 30%)")
                    player_turn_done = True 
            
            #chance to escape mob
            elif random.random() < 0.50:
                slow_print(" > You successfully escaped!")
                return #exit
            else:
                slow_print(" > Failed to escape!")
                player_turn_done = True 
                
        else:
            slow_print("Invalid action!")

        if enemy["health"] > 0 and player_turn_done:
            damage = max(0, enemy["attack"] - player["defense"])
            player["health"] -= damage
            slow_print(f" > {enemy['name']} attacks you for {damage} damage!")

    # new feature thank u neil
    if player["health"] <= 0:
        print()
        print("X" * GAME_WIDTH)
        print("YOU HAVE BEEN DEFEATED".center(GAME_WIDTH))
        print("GAME OVER".center(GAME_WIDTH))
        print("X" * GAME_WIDTH)
        
        while True:
            retry = input("\n Do you want to try again? (y/n) > ").lower()
            
            if retry == "y":
                player["health"] = 120
                player["max_health"] = 120
                player["mana"] = 60
                player["max_mana"] = 60
                player["attack"] = 15
                player["defense"] = 5
                player["inventory"] = []
                player["gold"] = 100
                player["level"] = 1
                player["experience"] = 0
                player["rank"] = "Rookie"
                current_location = "Forest"
                
                slow_print("\n... You gasp for air, waking up at the start of your journey ...")
                time.sleep(1)
                return
                
            elif retry == "n":
                game_running = False
                return
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

    
    if enemy["health"] <= 0:
        print()
        print("*" * GAME_WIDTH)
        print(f"VICTORY! You defeated {enemy['name']}!".center(GAME_WIDTH))
        print("*" * GAME_WIDTH)
        player["gold"] += enemy["gold"]
        player["experience"] += enemy["exp"]
        slow_print(f"Found: {enemy['gold']} Gold | Gained: {enemy['exp']} EXP")
        level_up()


# function for using items in inventory 
def use_item(target_enemy=None):
    if not player["inventory"]:
        slow_print("You have no items!")
        return False

    print()
    print("-" * GAME_WIDTH)
    print("INVENTORY".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)
    unique_items = []
    for item in player["inventory"]:
        if item not in unique_items:
            unique_items.append(item)

    for idx, item in enumerate(unique_items, 1):
        count = player["inventory"].count(item)
        print(f" {idx}. {item['name']} x{count} (Power: {item['value']})")

    print(" 0. Cancel")
    choice = input(f"\n Choose item > ")

    if choice == "0":
        return False

    if choice.isdigit() and 1 <= int(choice) <= len(unique_items):
        selected_template = unique_items[int(choice) - 1]

        item_index = -1
        for i, inv_item in enumerate(player["inventory"]):
            if inv_item['name'] == selected_template['name']:
                item_index = i
                break
        item = player["inventory"].pop(item_index)

        if item["type"] == "heal":
            player["health"] = min(player["max_health"], player["health"] + item["value"])
            slow_print(f"Used {item['name']}. Healed {item['value']} {RED}HP{RESET}!")
            return True
        elif item["type"] == "mana":
            player["mana"] = min(player["max_mana"], player["mana"] + item["value"])
            slow_print(f"Used {item['name']}. Restored {item['value']} {BLUE}MP{RESET}!")
            return True
        elif item["type"] == "buff_str":
            player["attack"] += item["value"]
            slow_print(f"Drank {item['name']}. ATK +{item['value']} (Permanent)!")
            return True
        elif item["type"] == "scroll":
            if target_enemy:
                slow_print(f"Cast {item['name']}! Dealt {item['value']} damage!")
                target_enemy["health"] -= item["value"]
                return True
            else:
                slow_print("Scrolls can only be used in battle!")
                player["inventory"].append(item)
                return False
        elif item["type"] == "weapon":
            player["attack"] += item["value"]
            slow_print(f"Equipped {item['name']}. ATK +{item['value']}!")
            return True
        elif item["type"] == "armor":
            player["defense"] += item["value"]
            slow_print(f"Equipped {item['name']}. DEF +{item['value']}!")
            return True
        elif item["type"] == "exp":
            player["experience"] += item["value"]
            slow_print(f"Used {item['name']}. Gained {item['value']} EXP!")
            level_up()
            return True
    else:
        slow_print("Invalid choice!")
        return False


# random generate items function DXDXDXDX
def find_item():
    loot = random.choice([
        {"name": "Small Pouch 1", "gold": 25},
        {"name": "Small Pouch 2 ", "gold": 30},
        {"name": "Medium Pouch", "gold": 100},
        {"name": "Large Pouch", "gold": 200},
        {"name": "Epic Chest", "gold": 500},
        {"name": "Experience Potion", "type": "exp", "value": 50},
        {"name": "Greater Experience Potion", "type": "exp", "value": 100},
        {"name": "Superior Experience Potion", "type": "exp", "value": 200},
        {"name": "Health Potion", "type": "heal", "value": 30},
        {"name": "Mana Potion", "type": "mana", "value": 30}
    ])

    print("-" * GAME_WIDTH)
    if "gold" in loot:
        player["gold"] += loot["gold"]
        slow_print(f"You found a {loot['name']} with {loot['gold']} gold!")
    else:
        slow_print(f"You found a {loot['name']}!")
        player["inventory"].append(loot)


# function for random eventz
def random_event(location):
    event = random.randint(1, 3)
    if event == 1:
        encounter_enemy(location)
    elif event == 2:
        find_item()
    else:
        print(".", end=" ", flush=True)
        time.sleep(0.5)


# function for exploration
def explore_location(location):
    print()
    print("=" * GAME_WIDTH)
    print(f"EXPLORING: {location.upper()}".center(GAME_WIDTH))
    print("=" * GAME_WIDTH)
    for i in range(3):
        if not game_running: break
        random_event(location)
    print()

#FN visit shop function
def visit_shop():
    print()
    print("-" * GAME_WIDTH)
    print("MERCHANT'S SHOP".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)
    print(f"Your Gold: {player['gold']}".center(GAME_WIDTH))
    print("-" * GAME_WIDTH)

    last_category = ""
    for idx, item in enumerate(shop_items_inventory, 1):
        itype = item['type']
        
        category_map = {
            'heal': "POTIONS", 'mana': "POTIONS", 'buff_str': "POTIONS",
            'scroll': "SCROLLS", 'weapon': "WEAPONS", 'armor': "ARMOR"
        }
        current_category = category_map.get(itype, "OTHER")

        if current_category != last_category:
            print(f"\n --- {current_category} ---")
            last_category = current_category

        if itype == "armor":
            stat_label = "DEF"
        elif itype == "weapon":
            stat_label = "ATK" 
        elif itype == "heal":
            stat_label = "HP "   
        elif itype == "mana":
            stat_label = "MP "   
        elif itype == "buff_str":
            stat_label = "STR"
        elif itype == "scroll":
            stat_label = "DMG"   
        else:
            stat_label = "Val"


        print(f" {idx}. {item['name']:<25} | {stat_label}: {item['value']:<3} | {item['price']:>4} G")

    print("-" * GAME_WIDTH)
    print(" 0. Exit Shop")

    while True:
        choice = input(f"\n Buy item # (0 to exit) > ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return
            elif 1 <= choice <= len(shop_items_inventory):
                item = shop_items_inventory[choice - 1]
                if player["gold"] >= item["price"]:
                    player["gold"] -= item["price"]
                    player["inventory"].append(item.copy())
                    slow_print(f"Purchased {item['name']}!")
                    print(f"Remaining Gold: {player['gold']}")
                else:
                    slow_print("Not enough gold!")
            else:
                slow_print("Invalid choice!")
        else:
            slow_print("Invalid input!")


def game_menu():
    print()
    print("=" * GAME_WIDTH)
    print(f"LOCATION: {current_location.upper()}".center(GAME_WIDTH))
    print("=" * GAME_WIDTH)
    print(" 1. Explore Area")
    print(" 2. Travel")
    print(" 3. Shop") 
    print(" 4. Inventory")
    print(" 5. Status")
    print(" 6. Quit")
    print("-" * GAME_WIDTH)
    choice = input(f"\n Choose option > ")
    return choice


#start of the game
def main():
    get_player_name()
    update_rank()
    global current_location

    while game_running:
        choice = game_menu()

        if choice == "1":
            explore_location(current_location)
        elif choice == "2":
            new_loc = choose_location()
            if new_loc:
                current_location = new_loc
        elif choice == "3":
            visit_shop()
        elif choice == "4":
            use_item()
        elif choice == "5":
            show_status()
        elif choice == "6":
            print("=" * GAME_WIDTH)
            print("Thanks for playing!".center(GAME_WIDTH))
            print("=" * GAME_WIDTH)
            break
        else:
            slow_print("Invalid choice!")


if __name__ == "__main__":
    main()