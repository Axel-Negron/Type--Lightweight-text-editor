from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as tk_font
from tkinter import ttk
from tkinter.colorchooser import askcolor
import configparser




############################Init####################################
window = Tk()
data = StringVar()
filepath = StringVar()
window.title("Just Type")

def load_config(config:configparser.ConfigParser):

    cur_font_name.set(config['Text']['font_name'])
    cur_font_size.set(config['Text']['font_size'])
    cur_font_color.set(config['Text']['font_color'])

    cur_bg1.set(config['Display']['bg_color1'])
    cur_bg2.set(config["Display"]['bg_color2'])
    cur_bg3.set(config["Display"]['bg_color3'])
    return

def ret_available_fonts():
    fonts = tk_font.families()

    return fonts

fonts = ret_available_fonts()
size_values = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18,
               20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]

#################Font variables#################

filepath.set('')
cur_tags = IntVar()

cur_tags.set(0)
cur_font_name = StringVar()
cur_font_size = IntVar()
cur_font_color = StringVar()

########################### Window colors

cur_bg1 = StringVar()
cur_bg2 = StringVar()
cur_bg3 = StringVar()

##############################################
cur_txt_addon = StringVar()
cur_txt_addon.set('normal')

boldvar = BooleanVar()
italicvar = BooleanVar()
underlinevar = BooleanVar()


is_bold = BooleanVar()
is_italic = BooleanVar()
is_underline = BooleanVar()


alive_btn = []
alive_widgets = []

rewrite_config = BooleanVar()
rewrite_config.set(0)
config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)
load_config(config)

i=IntVar()
combo_set = 0
for font in fonts:
    if font=='Arial':
        combo_set= i.get()
        break
    i.set(i.get()+1)
    
if i.get()>364:
    i.set(1)
    
    
#########################:##################################################


# MENU FUNCTIONS


def save_text_with_tags():

    try:
        path = filepath.get()
        print("Log-Filepath")

        if path=="":
            path = asksaveasfilename(defaultextension='.txt', filetypes=[
                                    ("Text Files", "*.txt")])
            filepath.set(path)
        
    except:
        print("Couldn't save, first time?")
        path = asksaveasfilename(defaultextension='.txt', filetypes=[
                                    ("Text Files", "*.txt")])
    
        if not filepath:
            return
        
    
    with open(path, "w") as file:
        # Dump the content and tags to the file

        for tag in txt.tag_names():
            if txt.tag_ranges(tag) == ():
                continue
            temp_text = txt.get(
                f"{txt.tag_ranges(tag)[0]}", f"{txt.tag_ranges(tag)[1]}")

            tag_config = txt.tag_configure(tag)
            font_from_tag = tag_config['font'][4]
            foreground_from_tag = tag_config['foreground'][4]
            tag_range = txt.tag_ranges(tag)
            file.write(
                f"{temp_text},{tag_range[0]},{tag_range[1]},{font_from_tag},{foreground_from_tag}\n")
            pass
    window.title(f'Just Type - {filepath}')


def load_text_with_tags():
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return

    # Clear the current content and tags in the Text widget
    txt.delete("1.0", END)
    data = []
    with open(filepath, "r") as file:
        for line in file:
            temp = line[:len(line)-1]
            temp = temp.split(",")
            data.append(temp)
            pass
    cur_tags.set(0)
    for entry in data:
        txt.insert(entry[1], entry[0])
        txt.tag_add(cur_tags.get(), entry[1], entry[2])
        txt.tag_config(cur_tags.get(), font=entry[3], foreground=entry[4])
        cur_tags.set(cur_tags.get()+1)

    return


def enter_update(event):
    w_size = window.winfo_geometry()
    insertpos = txt.index('insert')
    if insertpos[-1] == '0' or txt.get(insertpos+'-1c')==" ":
        i = 0
        newcursorpos = ''
        for char in insertpos:
            if insertpos[i+1]=='.':
                num = int(char)+1
                newcursorpos+=str(num)+'.0'
                break
            else:
                newcursorpos+=char
                i+=1
                
        txt.insert(insertpos,'\n')
        
        
    set_tag(cur_tags.get())
    window.geometry(w_size)
    txt.mark_set("insert", newcursorpos)
    return

def space_update(event):
    w_size = window.winfo_geometry()
    set_tag(cur_tags.get())
    window.geometry(w_size)
    return


def open_settings():
    w_size = window.winfo_geometry()
    sidebar_wdth = '10'
    settings_wdw = Toplevel(window,background=cur_bg2.get())
    settings_wdw.geometry("590x500")
    settings_wdw.title("Settings")
    sidebar = Frame(settings_wdw,background=cur_bg2.get(), width=sidebar_wdth)
    sidebar.pack(side=LEFT, fill='y',)
    txt_settings_btn = Button(sidebar, text="Text",background=cur_bg3.get(),foreground=cur_font_color.get(), width=sidebar_wdth,
                              command=lambda: disp_txt_settings(settings_wdw, alive_btn), pady=10)
    txt_settings_btn.pack()

    if txt_settings_btn["state"] == DISABLED:
        txt_settings_btn["state"] = NORMAL

    paper_settings_btn = Button(sidebar, text="Paper",background=cur_bg3.get(),foreground=cur_font_color.get(), width=sidebar_wdth,
                                command=lambda: disp_paper_settings(settings_wdw, alive_btn), pady=10)
    paper_settings_btn.pack()

    if paper_settings_btn["state"] == DISABLED:
        paper_settings_btn["state"] = NORMAL

    alive_btn.append(txt_settings_btn)
    alive_btn.append(paper_settings_btn)

    window.geometry(w_size)

    return

def rewrite():
    if(rewrite_config.get()):
        with open (config_file,'w') as file:
            config.set("Display","bg_color1",cur_bg1.get())
            config.set("Display","bg_color2",cur_bg2.get())
            config.set("Display","bg_color3",cur_bg3.get())
            config.write(file)

#########################################################


# Menu and Text Widget
txt_menu = Frame(window, background=cur_bg1.get(), height=40)
txt_menu.pack(fill='x', pady=(0, 1))

txt = Text(window, background=cur_bg1.get(), font=(cur_font_name.get(
), cur_font_size.get()*2), foreground=cur_font_color.get(), undo=True, maxundo=20)
txt.pack(expand=True, fill="both")


# TXT functions
##########################################################
def save_shrt(event):
    save_text_with_tags()
    return 


def increase_font(event):
    
    w_size = window.winfo_geometry()
    set_tag(cur_tags.get())
    if (cur_font_size.get()+2 >= 100):
        return
    cur_font_size.set(cur_font_size.get()+2)
    update_text(cur_font_name.get(),cur_font_size.get())
    window.geometry(w_size)
    
    return


def decrease_font(event):
    
    w_size = window.winfo_geometry()
    set_tag(cur_tags.get())
    if (cur_font_size.get()-2 <= 0):
        return
    cur_font_size.set(cur_font_size.get()-2)
    update_text(cur_font_name.get(),cur_font_size.get())
    window.geometry(w_size)
    return


def txt_addons():
    addons = []
    font_txt = ""
        
    if is_bold.get():
        addons.append('bold')

    if is_italic.get():
        addons.append('italic')
        
    if is_underline.get():
        addons.append('underline')
        
    for addon in addons:
        font_txt += addon+' '

    cur_txt_addon.set(font_txt)
 
    return


def get_last_position_of_final_tag(tag_name):
    tag_ranges = txt.tag_ranges(tag_name)
    if tag_ranges:
        last_range_end = tag_ranges[-1]
        return last_range_end
    else:
        return None


def clean_tags():
    tags = txt.tag_names()
    for tag in tags:
        if txt.tag_ranges(tag) == ():
            txt.tag_delete(tag)
    return

def update_text(new_font,new_size,):
    txt_addon = cur_txt_addon.get()
    if txt_addon == '' or None:
        txt_addon = 'normal'
    cur_font_name.set(new_font)
    cur_font_size.set(new_size)
    txt.config(font=(cur_font_name.get(), cur_font_size.get()*2, txt_addon),
               foreground=cur_font_color.get())
    txt.pack(expand=True, fill="both")
    

def set_tag(num: int):
    txt_addon = cur_txt_addon.get()
    clean_tags()
    size = window.winfo_geometry()
    tags = txt.tag_names()
    if len(tags) == 1:

        txt.tag_add(num, '1.0', INSERT)
        txt.tag_config(num, font=(cur_font_name.get(),
                       cur_font_size.get()*2, txt_addon), foreground=cur_font_color.get())
        pass

    elif txt.index(INSERT) == txt.index('end-1c'):

        last_tagpos = txt.tag_ranges(tags[-1])[1]
        txt.tag_add(num, last_tagpos, txt.index(INSERT))
        txt.tag_config(num, font=(cur_font_name.get(),
                       cur_font_size.get()*2, txt_addon), foreground=cur_font_color.get())
        pass

    else:
        txt.mark_set("insert", txt.index('end-1c'))
        pass


    cur_tags.set(num+1)
    window.geometry(size)
    return


def get_combobox_selected(combobox_font: ttk.Combobox, combobox_size: ttk.Combobox):

    set_tag(cur_tags.get())
    update_text(combobox_font, combobox_size)

    return


def color_updator():
    txt.config(background=cur_bg1.get())
    txt_menu.config(background=cur_bg2.get())
    italic_check.config(background=cur_bg3.get())
    underline_check.config(background=cur_bg3.get())
    bold_check.config(background=cur_bg3.get())
    apply_btn.config(background=cur_bg3.get())

    config.set('Display','bg_color1',cur_bg1.get())
    config.set('Display','bg_color2',cur_bg2.get())
    config.set('Display','bg_color3',cur_bg3.get())
    

def change_font_color():
    try:
        color = askcolor()
        cur_font_color.set(color[1])
        txt.config(fg=cur_font_color.get())
        txt.pack(expand=True, fill="both")
    except:
        print("Log - Couldn't set color")
        
    return


def underline_shrt(event):
    
    if is_underline.get()==1:
        set_tag(cur_tags.get())
        is_underline.set(0)
        underlinevar.set(0)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())
        

  
        return
    set_tag(cur_tags.get())
    is_underline.set(1)
    underlinevar.set(1)
    txt_addons()
    update_text(cur_font_name.get(),cur_font_size.get())

    
def bold_shrt(event):
    
    if is_bold.get()==1:
        set_tag(cur_tags.get())
        is_bold.set(0)
        boldvar.set(0)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())
        
  
     
        return
    
    
    set_tag(cur_tags.get())
    is_bold.set(1)
    boldvar.set(1)
    txt_addons()
    update_text(cur_font_name.get(),cur_font_size.get())


def italic_shrt(event):
    if is_italic.get()==1:
        set_tag(cur_tags.get())
        is_italic.set(0)
        italicvar.set(0)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())

       
        return
    set_tag(cur_tags.get())
    is_italic.set(1)
    italicvar.set(1)
    txt_addons()
    update_text(cur_font_name.get(),cur_font_size.get())
  
    
def bold_toggle():
    if boldvar.get():
        set_tag(cur_tags.get())
        is_bold.set(1)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())

        
    else:
        set_tag(cur_tags.get())
        is_bold.set(0)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())
        
        
def underline_toggle():
    if underlinevar.get():
        set_tag(cur_tags.get())
        is_underline.set(1)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())

        
    else:
        set_tag(cur_tags.get())
        is_underline.set(0)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())
        
        
def italic_toggle():
    if italicvar.get():
        set_tag(cur_tags.get())
        is_italic.set(1)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())

        
    else:
        set_tag(cur_tags.get())
        is_italic.set(0)
        txt_addons()
        update_text(cur_font_name.get(),cur_font_size.get())
    

def appearance_colors(selector:int):
    match selector:

        case 1:

            color = askcolor()[1]
            if color !=None:
                cur_bg1.set(color)
            else:    
                cur_bg1.set(config['Display']['bg_color1'])
                print('error picking color')

        case 2:

            color = askcolor()[1]
            if color !=None:
                cur_bg2.set(color)
            else:    
                cur_bg2.set(config['Display']['bg_color2'])
                print('error picking color')

        case 3:
            color = askcolor()[1]
            if color !=None:
                cur_bg3.set(color)
            else:    
                cur_bg3.set(config['Display']['bg_color3'])
                print('error picking color')

    color_updator()

    return


def disp_txt_settings(wndw: Toplevel, alivebtn: list):
    for thing in alive_widgets:
        thing.destroy()
    try:

        if alivebtn[0]["state"] == NORMAL:
            alivebtn[0]["state"] = DISABLED

        if alivebtn[1]["state"] == DISABLED:
            alivebtn[1]["state"] = NORMAL

    except:
        print("paper settings not alive, ignoring state")

    r_view = Frame(wndw,background=cur_bg2.get())
    r_view.pack(side=LEFT, fill='both', padx=5)

    rl_view = Frame(r_view,background=cur_bg2.get())
    rl_view.pack(side=LEFT, fill='y', padx=15)

    rr_view = Frame(r_view,background=cur_bg2.get())
    rr_view.pack(side=LEFT, fill='y', padx=5)

    font = Label(rl_view, text="Font: ", width=5, height=2,background=cur_bg3.get(),foreground=cur_font_color.get())
    font.pack()
    font_boxes = Frame(rl_view,background=cur_bg2.get())

    font_name_cmbx = ttk.Combobox(
        font_boxes, values=ret_available_fonts(), width=15)
    font_size_cmbx = ttk.Combobox(font_boxes, values=size_values, width=2)

    font_name_cmbx.pack(side=LEFT)
    font_size_cmbx.pack(side=RIGHT)

    font_boxes.pack()

    font_cmbx_apply = Button(rr_view, command=lambda: get_combobox_selected(
        font_name_cmbx, font_size_cmbx), text="Apply",background=cur_bg3.get(),foreground=cur_font_color.get(), pady=15, width=5)
    
    font_cmbx_apply.pack()

    color_picker_lbl = Label(rl_view, text="Change font color: ",background=cur_bg3.get(),foreground=cur_font_color.get(), pady=15)
    color_picker = Button(rl_view, text="Pick",
                          command=change_font_color,background=cur_bg3.get(),foreground=cur_font_color.get(), pady=15, width=20)

    color_picker_lbl.pack()
    color_picker.pack()

    view_color = Label(rr_view, text="ABCDE", width=5,
                       fg=cur_font_color.get(),background=cur_bg3.get(),foreground=cur_font_color.get(), pady=25)
    view_color.pack()

    alive_widgets.append(r_view)
    alive_widgets.append(rl_view)
    alive_widgets.append(rr_view)

    return


def disp_paper_settings(wndw: Toplevel, alivebtn: list):

    for thing in alive_widgets:
        thing.destroy()
    try:
        if alivebtn[1]["state"] == NORMAL:
            alivebtn[1]["state"] = DISABLED

        if alivebtn[0]["state"] == DISABLED:
            alivebtn[0]["state"] = NORMAL
    except:
        print("Font settings not alive")

    r_view = Frame(wndw,background=cur_bg2.get())
    r_view.pack(side=LEFT, fill='both', padx=5)

    rl_view = Frame(r_view,background=cur_bg2.get())
    rl_view.pack(side=LEFT, padx=5,fill='y')

    appearance_lbl = Label(rl_view,text='Appearance: ',background=cur_bg3.get(),foreground=cur_font_color.get())
    appearance_lbl.pack()

    colors_frame = Frame(rl_view,background=cur_bg2.get())
    colors_frame.pack()

    appearance_color1 = Label(colors_frame,text='Color 1',background=cur_bg3.get(),foreground=cur_font_color.get(),width=9)
    appearance_color1.pack(side=LEFT)
    appearance_color2 = Label(colors_frame,text='Color 2',background=cur_bg3.get(),foreground=cur_font_color.get(),width=9)
    appearance_color2.pack(side=LEFT)
    appearance_color3 = Label(colors_frame,text='Color 3',background=cur_bg3.get(),foreground=cur_font_color.get(),width=9)    
    appearance_color3.pack(side=LEFT)

    color_btn_frm = Frame(rl_view,background=cur_bg2.get())
    color_btn_frm.pack()
    
    color_picker1 = Button(color_btn_frm,text="Pick",command=lambda: appearance_colors(1),background=cur_bg3.get(),foreground=cur_font_color.get(),width=9)
    color_picker2 = Button(color_btn_frm,text="Pick",command=lambda: appearance_colors(2),background=cur_bg3.get(),foreground=cur_font_color.get(),width=9)
    color_picker3 = Button(color_btn_frm,text="Pick",command=lambda: appearance_colors(3),background=cur_bg3.get(),foreground=cur_font_color.get(),width=9)

    color_picker1.pack(side=LEFT)
    color_picker2.pack(side=LEFT)
    color_picker3.pack(side=LEFT)

    rewrite_system = Frame(rl_view,background=cur_bg2.get())
    rewrite_system.pack()
    store_system_settings = Checkbutton(rewrite_system,text='Save to system',background=cur_bg3.get(),foreground=cur_font_color.get(),onvalue=True,offvalue=False,variable=rewrite_config)
    store_btn = Button(rewrite_system,text='Apply',background=cur_bg3.get(),foreground=cur_font_color.get(),width=5,command=rewrite)
    store_system_settings.pack(side=LEFT)
    store_btn.pack(side=LEFT)

    rr_view = Frame(wndw,background=cur_bg2.get())
    rr_view.pack(side=RIGHT)


    
    alive_widgets.append(r_view)
    alive_widgets.append(rr_view)
    alive_widgets.append(rl_view)

    return


######################################################## Buttons
font_cmb = ttk.Combobox(txt_menu, values=fonts, width=30)
font_cmb.current(i.get())
font_cmb.pack(side=LEFT)

size_cmb = ttk.Combobox(txt_menu, values=size_values, width=5)
size_cmb.current(4)
size_cmb.pack(side=LEFT)

bold_check = Checkbutton(txt_menu, text='Bold', font=(cur_font_name.get(
), 12, 'bold'), foreground=cur_font_color.get(),background=cur_bg3.get(),onvalue=True, offvalue=False, variable=boldvar, command=bold_toggle)
italic_check = Checkbutton(txt_menu, text='Italic', font=(cur_font_name.get(
), 12, 'italic'),foreground=cur_font_color.get(),background=cur_bg3.get() ,onvalue=True, offvalue=False, variable=italicvar, command=italic_toggle)

underline_check = Checkbutton(txt_menu, text='Underline', font=(cur_font_name.get(
), 12, 'underline'),foreground=cur_font_color.get() ,background=cur_bg3.get(),onvalue=True, offvalue=False, variable=underlinevar, command=underline_toggle)

apply_btn = Button(txt_menu, foreground=cur_font_color.get(),background=cur_bg3.get(),text="Update", width=5, height=1, command=lambda: get_combobox_selected(
    font_cmb.get(), size_cmb.get()))
apply_btn.pack(side=LEFT)
bold_check.pack(side=LEFT, padx=3)
italic_check.pack(side=LEFT, padx=3)
underline_check.pack(side=LEFT, padx=3)

menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)


photo = PhotoImage(file="imgs/icon.png")
window.wm_iconphoto(False, photo)

menu.add_cascade(label='File', menu=filemenu)
menu

filemenu.add_command(label='Open', command=load_text_with_tags)
filemenu.add_command(label='Save As...', command=save_text_with_tags)
filemenu.add_command(label='Settings', command=open_settings)


##################################################### Keybinds

txt.bind("<Return>", enter_update)
txt.bind("<space>", space_update)
txt.bind("<less>", decrease_font)
txt.bind("<greater>", increase_font)
txt.bind("<Control-s>",save_shrt)
txt.bind("<Control-u>",underline_shrt)
txt.bind("<Control-b>",bold_shrt)
txt.bind("<Control-i>",italic_shrt)

#####################################################


window.mainloop()
