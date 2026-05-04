# TripVerse - Day 2 - Complete System
import json

# ==========================================
# Load files required for the application
# ==========================================

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ==========================================
# Load files required for the language
# ==========================================

def select_language():
    languages = load_json("languages.json")
    lang_list = list(languages.keys())
    
    print("\n" + "=" * 45)
    print("  SELECT LANGUAGE / भाषा चुनें")
    print("=" * 45)
    
    for i, lang in enumerate(lang_list, 1):
        print(f"  {i}. {lang}")
    
    while True:
        try:
            choice = int(input("\n  Enter number: "))
            if 1 <= choice <= len(lang_list):
                selected = lang_list[choice - 1]
                print(f"\n  ✅ Selected: {selected}")
                return selected, languages[selected]
            else:
                print("  ❌ Invalid! Try again.")
        except:
            print("  ❌ Please enter a valid number!")

# =====================================
# FIRST TIME SETUP - ADMIN
# =====================================

def first_time_setup(L):
    print("\n" + "=" * 45)
    print(f"  {L['setup_title']}")
    print("=" * 45)
    print(f"\n  {L['setup_welcome']}")

    config = load_json("Admin_config.json")

    name     = input(f"\n  {L['setup_name']}: ")
    username = input(f"  {L['setup_username']}: ")
    password = input(f"  {L['setup_password']}: ")
    config["admin"]["name"] = name
    config["admin"]["username"] = username
    config["admin"]["password"] = password
    config["is_setup_done"] = True
    
    save_json("Admin_config.json", config)
    print(f"\n  ✅ Setup complete! Welcome, {name}!")

# =====================================
# ADMIN LOGIN
# =====================================

def admin_login(L):
    config = load_json("Admin_config.json")
    
    print("\n" + "=" * 45)
    print(f"  {L['admin']}")
    print("=" * 45)
    
    username = input("\n  Username: ")
    password = input("  Password: ")
    
    if (username == config["admin"]["username"] and 
        password == config["admin"]["password"]):
        print(f"\n  ✅ Welcome, {config['admin']['name']}!")
        return True
    else:
        print("\n  ❌ Invalid credentials!")
        return False

# =====================================
# ADMIN DASHBOARD
# =====================================

def admin_dashboard(L):
    if not admin_login(L):
        return
    
    config = load_json("Admin_config.json")
    
    while True:
        print("\n" + "=" * 45)
        print(f"  {L['admin']}")
        print("=" * 45)
        print(f"\n  1. View & Update Budget Plans")
        print(f"  2. View All Users")
        print(f"  3. View All Vendors")
        print(f"  4. Change Admin Password")
        print(f"  5. Back to Main Menu")
        
        choice = input("\n  Please enter your choice: ")
        
        if choice == "1":
            update_budget(L, config)
        elif choice == "2":
            view_users(L)
        elif choice == "3":
            view_vendors(L)
        elif choice == "4":
            change_password(L, config)
        elif choice == "5":
            break
        else:
            print("  ❌ Invalid choice!")

# =====================================
# BUDGET UPDATE
# =====================================

def update_budget(L, config):
    print("\n" + "=" * 45)
    print("  BUDGET PLANS")
    print("=" * 45)
    
    for utype, budget in config["budget_plans"].items():
        print(f"  {utype:12}: Rs.{budget['min']:>8} - Rs.{budget['max']:>8}")
    
    print(f"\n  {L['update_budget']}:")
    for i, utype in enumerate(config["budget_plans"].keys(), 1):
        print(f"  {i}. {utype}")
    
    utype = input("\n  Enter category name: ")
    
    if utype in config["budget_plans"]:
        new_min = int(input(f"  {L['new_min']}: Rs. "))
        new_max = int(input(f"  {L['new_max']}: Rs. "))
        
        config["budget_plans"][utype]["min"] = new_min
        config["budget_plans"][utype]["max"] = new_max
        save_json("Admin_config.json", config)
        
        print(f"\n  ✅ {L['success']}")
        print(f"  {utype}: Rs.{new_min} - Rs.{new_max}")
    else:
        print("  ❌ Category not found!")

# =====================================
# VIEW USERS
# =====================================

def view_users(L):
    data = load_json("users.json")
    print("\n" + "=" * 45)
    print("  ALL USERS")
    print("=" * 45)
    
    if len(data["users"]) == 0:
        print("\n  No users registered yet!")
    else:
        for i, user in enumerate(data["users"], 1):
            print(f"\n  {i}. {user['name']} | {user['email']} | {user['type']}")

# =====================================
# VIEW VENDORS
# =====================================

def view_vendors(L):
    data = load_json("vendors.json")
    print("\n" + "=" * 45)
    print("  ALL VENDORS")
    print("=" * 45)
    
    for category, vendors in data.items():
        print(f"\n  {category.upper()}: {len(vendors)} registered")

# =====================================
# CHANGE PASSWORD
# =====================================

def change_password(L, config):
    old = input("\n  Enter current password: ")
    
    if old == config["admin"]["password"]:
        new = input("  Enter new password: ")
        confirm = input("  Confirm new password: ")
        
        if new == confirm:
            config["admin"]["password"] = new
            save_json("Admin_config.json", config)
            print(f"\n  ✅ {L['success']}")
        else:
            print("\n  ❌ Passwords do not match!")
    else:
        print("\n  ❌ Incorrect current password!")

# =====================================
# USER PANEL
# =====================================

def user_panel(L):
    config = load_json("Admin_config.json")
    users_data = load_json("users.json")
    
    print("\n" + "=" * 45)
    print(f"  {L['user']}")
    print("=" * 45)
    
    # User registration
    print("\n  Please enter your details:")
    name = input("  Full Name: ")
    email = input("  Email: ")
    
    print(f"\n  {L['select_user_type']}:")
    user_types = list(config["budget_plans"].keys())
    for i, utype in enumerate(user_types, 1):
        budget = config["budget_plans"][utype]
        print(f"  {i}. {utype} (Rs.{budget['min']} - Rs.{budget['max']})")
    
    utype_choice = int(input("\n  Enter number: ")) - 1
    user_type = user_types[utype_choice]
    
    print(f"\n  {L['enter_budget']}:")
    user_budget = int(input("  Rs. "))
    
    print(f"\n  {L['enter_days']}:")
    days = int(input("  "))
    
    # Save user
    users_data["users"].append({
        "name": name,
        "email": email,
        "type": user_type,
        "budget": user_budget,
        "days": days
    })
    save_json("users.json", users_data)
    
    # Suggestion
    min_b = config["budget_plans"][user_type]["min"]
    max_b = config["budget_plans"][user_type]["max"]
    daily = user_budget // days
    
    print("\n" + "=" * 45)
    print("  TRIPVERSE SUGGESTION")
    print("=" * 45)
    
    if user_budget < min_b:
        print(f"\n  ⚠️  {L['budget_low']}")
        print(f"  Minimum Required: Rs.{min_b}")
    elif user_budget > max_b:
        print(f"\n  💎 {L['budget_high']}")
        print(f"  {L['per_day']}: Rs.{daily}")
    else:
        print(f"\n  ✅ {L['budget_perfect']}")
        print(f"\n  Name     : {name}")
        print(f"  Category : {user_type}")
        print(f"  Budget   : Rs.{user_budget}")
        print(f"  Days     : {days}")
        print(f"  {L['per_day']}: Rs.{daily}")

# =====================================
# MAIN PROGRAM
# =====================================

# Language select karo
selected_lang, L = select_language()

# First time setup check
config = load_json("Admin_config.json")
if not config["is_setup_done"]:
    first_time_setup(L)

# Main loop
while True:
    print("\n" + "=" * 45)
    print(f"  {L['welcome']}")
    print("=" * 45)
    print(f"\n  1. {L['admin']}")
    print(f"  2. {L['user']}")
    print(f"  3. Change Language")
    print(f"  4. {L['exit']}")
    
    choice = input("\n  Please enter your choice (1/2/3/4): ")
    
    if choice == "1":
        admin_dashboard(L)
    elif choice == "2":
        user_panel(L)
    elif choice == "3":
        selected_lang, L = select_language()
    elif choice == "4":
        print(f"\n  {L['goodbye']}")
        break
    else:
        print("  ❌ Invalid choice!")