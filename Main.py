from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as tk_font
from tkinter import ttk
from tkinter.colorchooser import askcolor


window = Tk()
data = StringVar()
window.title("Just Type")


#Font variables#
cur_tags = IntVar()
cur_tags.set(0)
cur_font_name = StringVar()
cur_font_size = IntVar()
cur_font_name.set('Calibri')
cur_font_size.set(14)
cur_font_color = StringVar()
cur_font_color.set('#000000')
cur_bg = StringVar()
cur_bg.set("#edffd6")
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


def ret_available_fonts():
    fonts = tk_font.families()

    return fonts


fonts = ret_available_fonts()

cur_font_name.set(fonts[1])
size_values = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18,
               20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
cur_font_size.set(size_values[5])

# MENU FUNCTIONS


def save_text_with_tags():
    filepath = asksaveasfilename(defaultextension='.txt', filetypes=[
                                 ("Text Files", "*.txt")])
    if not filepath:
        return

    with open(filepath, "w") as file:
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
    update_txt(cur_font_name.get(), cur_font_size.get(), cur_tags.get())
    print(event)
    return


def open_settings():

    sidebar_wdth = '10'
    settings_wdw = Toplevel(window)
    settings_wdw.geometry("590x500")
    settings_wdw.title("Settings")
    sidebar = Frame(settings_wdw, width=sidebar_wdth)
    sidebar.pack(side=LEFT, fill='y',)
    txt_settings_btn = Button(sidebar, text="Text", width=sidebar_wdth,
                              command=lambda: disp_txt_settings(settings_wdw, alive_btn), pady=10)
    txt_settings_btn.pack()

    if txt_settings_btn["state"] == DISABLED:
        txt_settings_btn["state"] = NORMAL

    paper_settings_btn = Button(sidebar, text="Paper", width=sidebar_wdth,
                                command=lambda: disp_paper_settings(settings_wdw, alive_btn), pady=10)
    paper_settings_btn.pack()

    if paper_settings_btn["state"] == DISABLED:
        paper_settings_btn["state"] = NORMAL

    alive_btn.append(txt_settings_btn)
    alive_btn.append(paper_settings_btn)

    return

###############################


# Menu and Text Widget
txt_menu = Frame(window, background=cur_bg.get(), height=40)
txt_menu.pack(fill='x', pady=(0, 1))

txt = Text(window, background=cur_bg.get(), font=(cur_font_name.get(
), cur_font_size.get()*2), foreground=cur_font_color.get(), undo=True, maxundo=20)
txt.pack(expand=True, fill="both")


# TXT functions
##########################################################

def increase_font(event):
    if (cur_font_size.get()+2 <= 0):
        return
    cur_font_size.set(cur_font_size.get()+2)
    update_txt(cur_font_name.get(), cur_font_size.get(), cur_tags.get())
    return


def decrease_font(event):
    if (cur_font_size.get()-2 <= 0):
        return
    cur_font_size.set(cur_font_size.get()-2)
    update_txt(cur_font_name.get(), cur_font_size.get(), cur_tags.get())
    return


def txt_addons():

    size = window.winfo_geometry()
    addons = []
    font_txt = ""

    txt.mark_set('space', INSERT+'-1c')
    last_elm = txt.get('space')
    if last_elm == " ":
        update_txt(cur_font_name.get(), cur_font_size.get(), cur_tags.get())

    if boldvar.get() or is_bold.get() != FALSE:
        if is_bold.get() != 1:

            addons.append('bold')
            is_bold.set(1)
        else:
            is_bold.set(0)

    if italicvar.get() or is_italic.get() != FALSE:
        if is_italic.get() != 1:
            addons.append('italic')
            is_italic.set(1)

        else:
            is_italic.set(0)

    if underlinevar.get() or is_underline.get() != FALSE:
        if is_underline.get() != 1:
            addons.append('underline')
            is_underline.set(1)

        else:
            is_underline.set(0)

    for addon in addons:
        font_txt += addon+''

    cur_txt_addon.set(font_txt)

    if font_txt != "":
        txt.config(font=(cur_font_name.get(), cur_font_size.get()*2, font_txt))
    else:
        txt.config(font=(cur_font_name.get(), cur_font_size.get()*2))
        pass

    window.geometry(size)


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


def update_txt(new_font, new_size, num: int):
    txt_addon = cur_txt_addon.get()
    if txt_addon == '' or None:
        txt_addon = 'normal'
    clean_tags()
    size = window.winfo_geometry()
    tags = txt.tag_names()
    if len(tags) == 1:

        txt.tag_add(num, '1.0', INSERT)
        txt.tag_config(num, font=(cur_font_name.get(),
                       cur_font_size.get()*2, txt_addon), foreground=cur_font_color.get())
        pass

    elif txt.index(INSERT) == txt.index('end-1c'):
        # check if tag was already made.
        last_tagpos = txt.tag_ranges(tags[-1])[1]
        txt.tag_add(num, last_tagpos, txt.index(INSERT))
        txt.tag_config(num, font=(cur_font_name.get(),
                       cur_font_size.get()*2, txt_addon), foreground=cur_font_color.get())
        pass

    else:
        txt.mark_set("insert", txt.index('end-1c'))
        pass

    cur_font_name.set(new_font)
    cur_font_size.set(new_size)
    txt.config(font=(cur_font_name.get(), cur_font_size.get()*2, txt_addon),
               foreground=cur_font_color.get())
    txt.pack(expand=True, fill="both")
    cur_tags.set(num+1)

    window.geometry(size)
    return


def get_combobox_selected(combobox_font: ttk.Combobox, combobox_size: ttk.Combobox, cmb_num):

    if (cmb_num == 1):
        update_txt(combobox_font.get(), combobox_size.get(), cur_tags.get())

    return


def change_font_color():
    try:
        color = askcolor()
        cur_font_color.set(color[1])
        txt.config(fg=cur_font_color.get())
        txt.pack(expand=True, fill="both")
    except:
        print("Log - Couldn't set color")
        
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

    r_view = Frame(wndw)
    r_view.pack(side=LEFT, fill='both', padx=5)

    rl_view = Frame(r_view)
    rl_view.pack(side=LEFT, fill='y', padx=15)

    rr_view = Frame(r_view)
    rr_view.pack(side=LEFT, fill='y', padx=5)

    font = Label(rl_view, text="Font: ", width=5, height=2)
    font.pack()
    font_boxes = Frame(rl_view)

    font_name_cmbx = ttk.Combobox(
        font_boxes, values=ret_available_fonts(), width=15)
    font_size_cmbx = ttk.Combobox(font_boxes, values=size_values, width=2)

    font_name_cmbx.pack(side=LEFT)
    font_size_cmbx.pack(side=RIGHT)

    font_boxes.pack()

    font_cmbx_apply = Button(rr_view, command=lambda: get_combobox_selected(
        font_name_cmbx, font_size_cmbx, cur_tags.get()), text="Apply", pady=15, width=5)
    font_cmbx_apply.pack()

    color_picker_lbl = Label(rl_view, text="Change font color: ", pady=15)
    color_picker = Button(rl_view, text="Pick",
                          command=change_font_color, pady=15, width=20)

    color_picker_lbl.pack()
    color_picker.pack()

    view_color = Label(rr_view, text="ABCDE", width=5,
                       fg=cur_font_color.get(), pady=25)
    view_color.pack()

    alive_widgets.append(r_view)
    alive_widgets.append(rl_view)
    alive_widgets.append(rr_view)

    return


def disp_paper_settings(wndw: Toplevel, alivebtn: list):

    for thing in alive_widgets:
        thing.destroy()

    if alivebtn[1]["state"] == NORMAL:
        alivebtn[1]["state"] = DISABLED

    if alivebtn[0]["state"] == DISABLED:
        alivebtn[0]["state"] = NORMAL

    return


# Buttons
font_cmb = ttk.Combobox(txt_menu, values=fonts, width=10)
font_cmb.current(1)
font_cmb.pack(side=LEFT)

size_cmb = ttk.Combobox(txt_menu, values=size_values, width=5)
size_cmb.current(5)
size_cmb.pack(side=LEFT)

bold_check = Checkbutton(txt_menu, text='Bold', font=(cur_font_name.get(
), 12, 'bold'), onvalue=True, offvalue=False, variable=boldvar, command=txt_addons)
italic_check = Checkbutton(txt_menu, text='Italic', font=(cur_font_name.get(
), 12, 'italic'), onvalue=True, offvalue=False, variable=italicvar, command=txt_addons)

underline_check = Checkbutton(txt_menu, text='Underline', font=(cur_font_name.get(
), 12, 'underline'), onvalue=True, offvalue=False, variable=underlinevar, command=txt_addons)


apply_btn = Button(txt_menu, text="Update", width=5, height=1, command=lambda: update_txt(
    font_cmb.get(), size_cmb.get(), cur_tags.get()))
apply_btn.pack(side=LEFT)
bold_check.pack(side=LEFT, padx=3)
italic_check.pack(side=LEFT, padx=3)
underline_check.pack(side=LEFT, padx=3)

menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)


photo = PhotoImage(file="imgs\icon.png")
window.wm_iconphoto(False, photo)

menu.add_cascade(label='File', menu=filemenu)
menu

filemenu.add_command(label='Open', command=load_text_with_tags)
filemenu.add_command(label='Save As...', command=save_text_with_tags)
filemenu.add_command(label='Settings', command=open_settings)


# Keybinds

txt.bind("<Return>", enter_update)
txt.bind("<space>", enter_update)
txt.bind("<less>", decrease_font)
txt.bind("<greater>", increase_font)

#################################


window.mainloop()
