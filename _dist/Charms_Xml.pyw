import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import PySimpleGUI as sg
from tkinter import*
# from PIL import Image
# from PIL.TiffTags import TAGS
sg.theme('LightPurple')

#---------------------------------------------------------
# def Ask_Path():
#     root = Tk()
#     root.geometry("400x400")
#     background = PhotoImage(file="d:\\.unsorted\\112.png")

#     canvas_01 = Canvas(root, width=400, height=400)
#     canvas_01.pack(fill="both", expand=True)
#     canvas_01.create_image(0, 0, image=background, anchor="nw")

#     root.mainloop()
#---------------------------------------------------------
def Ask_Path():

    layout = [
        # [sg.Image(data="d:\\.unsorted\\111.png")],
        [sg.Text("Skin absolute path ('Game' folder)", text_color='blue')],
        [sg.InputText(
            default_text = "Soul of the mind, key to life's ether",
            key = "-SKINS-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 Charms_XMLer', layout)

    while True:
        event, values = window.read(close=True)

        skin_repo = values["-SKINS-"]

        if event == 'OK':
            return skin_repo

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
#---------------------------------------------------------
def del_xml(skin_repo):
    for root, dirs, files in os.walk(skin_repo):
        for name in files:
            if name.endswith('xml'):
                item = os.path.join(root, name)
                print(f"\033[35mRemoving:\033[m\n{item}")
                os.remove(item)
#---------------------------------------------------------
def fileStructure(it_acc_Skin, obj_att_Skin):

    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
        else:
            os.makedirs(pppath)

    check_and_create(it_acc_Skin)
    check_and_create(obj_att_Skin)
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
# def checkTIF():

    # def checker(testTIF):
    #     with Image.open(testTIF) as img:
    #         meta_dict = {TAGS[key] : img.tag[key] for key in img.tag}
        
    #     ImageWidth = meta_dict['ImageWidth']
    #     ImageLength = meta_dict['ImageLength']
    #     ImageDimensions = ImageWidth + ImageLength
    #     BitsPerSample = meta_dict['BitsPerSample']
    #     PhotoshopInfo = meta_dict['PhotoshopInfo'].decode('utf-8')
        
    #     if ImageDimensions != (256, 256):
    #         sg.popup_error(f"ERROR{testTIF}\nImageDimensions", ImageDimensions, text_color="red")

    #     if BitsPerSample != (8, 8, 8, 8,):
    #         sg.popup_error(f"ERROR {testTIF}\nBitsPerSample", BitsPerSample, text_color="red")

    #     if "Diffuse" in PhotoshopInfo:
    #         sg.popup_error(f"ERROR {testTIF}\nPhotoshopInfo\n\n[Diffuse preset for Icons is forbiden]", text_color="red")

    # for root, dirs, files in os.walk(libs_icons):
    #     for tif_Name in files:
    #         if tif_Name.endswith('.tif'):
    #             testTIF = os.path.join(root, tif_Name)
    #             checker(testTIF)
#---------------------------------------------------------
def main():
    del_xml(skin_repo)
    fileStructure(it_acc_Skin, obj_att_Skin)
    scanCharms(obj_att_Skin)
    create_xml()
    # checkTIF()

    sg.popup_notify('Complete')

if __name__ == "__main__":

    skin_repo = Ask_Path()

    sources = {}

    # # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("e:\\wfpc-minsk\\Game")
    # skin_repo = os.path.abspath("d:\\__some_get_come__\\__test_Charm\\Game")
    # testTIF = f"d:\\_WfPC_rep\\wfpc_work\\master\\WFPC_Content_Pack_22\\22_8_Charms_BP_Real_Wars_x5\\Game\\Libs\\Icons\\charms\\charm_realwars01.tif"
    # # ==================TEST_PATH==================================

    # skin path
    it_acc_Skin = skin_repo + '\\Items\\Accessories'
    obj_att_Skin = skin_repo + '\\Objects\\Attachments\\Charms'
    libs_icons = skin_repo + '\\Libs\\Icons'

    main()