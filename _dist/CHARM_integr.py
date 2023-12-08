import os
import xml.etree.ElementTree as ET
import os.path
import PySimpleGUI as sg
import shutil
from colorama import Back, Style, Fore
sg.theme('DarkGrey13')

#=========================================================
# SETUP
#=========================================================
def Ask_Path():
    layout = [
        [sg.Text("[WFPC_master] path", text_color='yellow')],
        [sg.InputText(default_text = r"e:\\partner_WPC\\wfpc_mrg\\main", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Temp Folder", text_color='yellow')],
        [sg.InputText(default_text = r"d:\\temp_charm", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 integCharms', layout)

    while True:
        event, values = window.read(close=True)
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
        if event == 'OK':
            return master, mod_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            exit(0)
        
    # window.close()
#---------------------------------------------------------
def list_to_string(l):
    str1 = '\n'
    return (str1.join(l))
#---------------------------------------------------------
def fileStructure(createTempFolders):

    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
        else:
            os.makedirs(pppath)
    
    def copyFile(temp, master):
        if os.path.exists(temp):
            pass
        else:
            shutil.copyfile(master, temp)
    
    for tempFolder in createTempFolders:
        check_and_create(tempFolder)
    
    # ItemFilter
    copyFile(temp_ItemsFilter_charm, master_ItemsFilter_charm)
    # UI
    copyFile(temp_UIcharm, master_UIcharm) 
    # catalog_offers_IGR
    copyFile(temp_catalog_offers_IGR, master_catalog_offers_IGR)
#---------------------------------------------------------
def remove_lastline(path):
    fd=open(path,"r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    s="\n".join(m[:-1])
    fd=open(path,"w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()
#---------------------------------------------------------
def writeChanges(path, template):
    try:
        open(path, 'a').close()
        open(path, 'r+').write(template)
        print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.BLUE + " ...Added" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def modifyChanges(path, template, charm, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + charm + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.MAGENTA + " ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def getCharms():
    for _, dirs, _ in os.walk(f"{temp}\\Game\\Objects\\Attachments\\charms\\"):
        dirs = dirs
        break
    
    for i in dirs:
        print(f"get charm... {i}")
    return dirs
#---------------------------------------------------------
def modifyChanges(path, template, charm, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + charm + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.MAGENTA + " ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def scanCharms(obj_att_Skin):
    for root, dirs, files in os.walk(obj_att_Skin):
        dirs = dirs
        for mtl_file in files:
            if mtl_file.endswith('.mtl') and '_tp' not in mtl_file:
                
                sources_xml = []
                obj_xml_dest = os.path.join(root, mtl_file).replace(".mtl", ".xml")
                it_xml_dest = obj_xml_dest.replace(f"Objects\\Attachments\\Charms\\{mtl_file.split('.')[0]}", "Items\\Accessories")
                itShop_xml_dest = it_xml_dest.replace(".xml", "_shop.xml")
                
                sources_xml.append(obj_xml_dest)
                sources_xml.append(it_xml_dest)
                sources_xml.append(itShop_xml_dest)

                material = mtl_file.split(".")[0]
                sources.update({material:sources_xml})
#---------------------------------------------------------
def create_xml():
    for elem in sources:
        for path in sources[elem]:
            open(path, 'a').close()
    
    for elem in sources:

        # Objects _xml
        obj_pattern = f"""<item_view name="{elem}">
    <geometry>
    \t<firstperson slot="bottom" name="objects/Attachments/charms/{elem}/{elem}.cgf" offset="0.00000,0.00000,0.00000" angles="0.000,0.000,0.000" fov="60"/>
    \t<thirdperson slot="bottom_tp" name="objects/Attachments/charms/{elem}/{elem}_tp.cgf"/>
    </geometry>
    <helpers>
    \t<helper name="charm" offset="0.00000,0.00000,0.00000" angles="0.000,0.000,0.000"/>
    </helpers>
    <materials>
    \t<material name="default" file="objects/Attachments/charms/{elem}/{elem}.mtl" tpfile="objects/Attachments/charms/{elem}/{elem}_tp.mtl"/>
    </materials>
    </item_view>"""
        palette_Objects = sources[elem][0]
        open(palette_Objects, 'w').write(obj_pattern)

        # Items _xml
        it_pattern = f"""<item class="K01_Item" name="{elem}" type="attachment" net_policy="weapon" view_settings="objects/Attachments/charms/{elem}/{elem}.xml">
	<drop_params>
	\t<item name="{elem}" type="attachment"/>
	</drop_params>
	<settings>
	\t<param name="charm" value="1"/>
	</settings>
	<types>
	\t<type helper="charm" name="charm"/>
	</types>
    <charm_params>
    \t<param name="use_simulation" value="1"/>
    \t<param name="max_angle" value="45.0"/>
    \t<param name="mass" value="0.05"/>
    \t<param name="damping" value="0.995"/>
    \t<param name="stiffness" value="0.3"/>
	\t<param name="bounce_on_weapon_mult" value="0.5"/>
	\t<param name="bounce_on_landing_min_vel" value="8.25"/>
	\t<param name="bounce_on_fire_min_vel" value="1.25"/>
    \t<param name="capsule" value="0.02, 0.02, 0"/>
    </charm_params>\n</item>"""
        palette_Items = sources[elem][1]
        open(palette_Items, 'w').write(it_pattern)

        # ItemsShop _xml
        itShop_pattern = f"""<shop_item name="{elem}_shop" type="charm">
	<mmo_stats>
	\t<param name="item_category" value="charm"/>
	\t<param name="shopcontent" value="1"/>
	\t<param name="max_buy_amount" value="5"/>
	\t<param name="classes" value="SRME"/>
	</mmo_stats>
	<UI_stats>
	\t<param name="category" value="charm"/>
	\t<param name="name" value="@{elem}_name"/>
	\t<param name="description" value="@ui_accessories_{elem}"/>
	\t<param name="icon" value="{elem}"/>
	</UI_stats>
	<content>
	\t<item name="{elem}"/>
	</content>
	<charm>
	\t<param name="thumbnail_icon" value="{elem}_thumbnail"/>
	\t<param name="modified_stats_description" value="@ui_accessories_charm_no_stats"/>
	</charm>\n</shop_item>"""
        palette_ItemsShop = sources[elem][2]
        open(palette_ItemsShop, 'w').write(itShop_pattern)
#---------------------------------------------------------


#---------------------------------------------------------
# ItemsFilter
#---------------------------------------------------------
def intagrate_ItemFilter():
    for charm in charms_list:
        
        template_ItemFilter = f"""\n\t<Item name="{charm}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy/>\n\t</Item>\n</ClassFilters>"""

        modifyChanges(temp_ItemsFilter_charm, template_ItemFilter, charm, '', '')
#---------------------------------------------------------
# UI
#---------------------------------------------------------
def intagrate_UI():
    for charm in charms_list:
    
        template_UI = f"""\n\t<image name="{charm}" file="Libs/Icons/charms/{charm}.tif" pos="0,0" size="200,200"/>
	<image name="{charm}_thumbnail" file="Libs/Icons/charms/{charm}.tif" pos="30,40" size="140,140"/>\n</images>"""

        modifyChanges(temp_UIcharm, template_UI, charm, '', '')
#---------------------------------------------------------
# catalog_offers_IGR
#---------------------------------------------------------
def intagrate_catalog_offers_IGR():

    root = ET.parse(temp_catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)
    
    for charm in charms_list:
        num = charms_list.index(charm) + 1
        
        commiten = f"<!-- charm... {charm} -->"
        template_offer = f"""\n\t{commiten}\n\t<offer store_id="{store_id + num}" item_name="{charm}_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" game_money="0" cry_money="123" crown_money="0"/>\n</offers>"""

        modifyChanges(temp_catalog_offers_IGR, template_offer, charm, '', '')
#=========================================================
# DRIVE
#=========================================================
def main():
    print(Fore.BLUE + f"--- Intagrating Charms..." + Style.RESET_ALL)
    fileStructure(createTempFolders)
    scanCharms(temp + '\\Game\\Objects\\Attachments\\Charms')
    create_xml()
    intagrate_ItemFilter()
    intagrate_UI()
    intagrate_catalog_offers_IGR()
    input(Fore.LIGHTBLUE_EX + '...Complete ' + Style.RESET_ALL)

if __name__ == "__main__":
    
    gSpace = "\t"
    master, temp = Ask_Path()
    charms_list = getCharms()
    
    sources = {}

    ItemsFilter_charm = "\\Game\\Libs\\Config\\ItemsFilter_charm.xml"
    UIcharm = "\\Game\\Libs\\Config\\UI\\charms\\icons_charms.xml"
    catalog_offers_IGR = "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"
# ----------------
    master_ItemsFilter_charm = master + ItemsFilter_charm
    master_UIcharm = master + UIcharm
    master_catalog_offers_IGR = master + catalog_offers_IGR

    temp_ItemsFilter_charm = temp + ItemsFilter_charm
    temp_UIcharm = temp + UIcharm
    temp_catalog_offers_IGR = temp + catalog_offers_IGR

    createTempFolders = [temp + '\\Game\\Items\\Accessories',
                        temp + '\\Game\\Objects\\Attachments\\Charms',
                        temp + '\\Game\\Libs\\Icons',
                        temp + "\\Game\\Libs\\Config\\UI\\charms",
                        temp + "\\Game\\Libs\\Config\\Shop"]
    main()