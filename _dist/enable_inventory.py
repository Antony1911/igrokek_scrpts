#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
# [Enable inventory select]
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
import os.path
def main():

    script_path = r"d:\script_path.txt"

    if os.path.exists(script_path) and len(open(script_path).read()) > 3 and os.path.exists(open(script_path).read()):

        exists_content = open(script_path).read()
        print("Continue with path? ", exists_content)
        u_input = input()

        if len(u_input) == 0:
            cl = exists_content
        elif len(u_input) > 0:
            cl = input("Client path? \n")
            out_file = open(script_path, "w")
            out_file.write(cl)
            out_file.close()

    else:
        print("Recreating script path", str(r"d:\script_path.txt"))

        cl = input("Client path? \n")
        out_file = open(script_path, "w")
        out_file.write(cl)
        out_file.close()
        

    editor = cl + r"Game\config\editor.cfg"

    try:
        if str("i_enable_inventory_select 1") in open(editor, 'r').read():
            pass
        else:
            f = open(editor, 'a').write('\ni_enable_inventory_select 1\n')
            f.close()
    except(AttributeError):
        pass


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
# [add_weapons_to_lua]
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    path = str(cl + r"Game\Libs\Config\presets\EditorSoldier.lua")

    search_items = 'items'
    search_ammo = 'ammo'
    search_att = 'attachments'

    content = open(path, 'r+', encoding="utf-8").readlines()
    cont_list = []

    weapons = input("Insert your weapons\n >")


# Creating weapon list
    weapon_list = weapons.strip().split()
    ammo_list = []
    att_list = []


# Creating attachment list
    for i in weapon_list:
        if "sr" in i:
            att_list.append(i)


# Creating ammo list
    for i in weapon_list:
        a = i.strip('1234567890kn')
        ammo_list.append(a)

    str_nums = 0
    for line in content:
        str_nums += 1

        if search_items in line:
            items = str_nums
        cont_list.append(line)

        if search_att in line:
            attachments = str_nums

        if search_ammo in line:
            ammo = str_nums
    # cont_list.append(line)

    N = len(weapon_list)
    #M = len(att_list)


# Adding Items
    try:
        for i in weapon_list:
            txt_items = '\t\t\t{ name = ' + f'"{i}"' + ',' + " ui_name = " + f'"@{i}_shop_name"' + '},\n'
            if txt_items not in cont_list:
                cont_list.insert(items + 1, txt_items)
    except:
        pass


# Adding Attachments, only ss04 for sr
    try:
        for i in att_list:
            txt_att = '\t\t\t{ name = "ss04",' + f' attachTo="{i}",' + ' id=12},\n'
            if txt_att not in cont_list:
                cont_list.insert(attachments + 1 + N, txt_att)
    except:
        pass


# Adding Ammo
    try:
        for i in ammo_list:
            txt_ammo = '\t\t\t{ name = ' + f'"bullet_{i}"' + ',' + ' amount = 150 },\n'
            if txt_ammo not in cont_list:
                cont_list.insert(ammo + N, txt_ammo)
    except:
        pass

    open(path, 'w', encoding="utf-8").writelines(cont_list)
    print('...Done')


if __name__ == '__main__':
    main()
