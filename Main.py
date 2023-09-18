from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as tk_font
from tkinter import ttk 
from tkinter.colorchooser import askcolor






window = Tk()
data  = StringVar()
window.title("Text Editor")


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





alive_btn = []
alive_widgets = []

#

txt = Text(window,background=cur_bg.get(),font=(cur_font_name.get(),cur_font_size.get()),foreground=cur_font_color.get(),undo=True,maxundo=20)
txt.pack(expand=True,fill="both")



def get_last_position_of_final_tag(tag_name):
    tag_ranges = txt.tag_ranges(tag_name)
    if tag_ranges:
        last_range_end = tag_ranges[-1]
        return last_range_end
    else:
        return None

def update_txt(new_font,new_size,num:int):
    tags = txt.tag_names()
    if len(tags)==1:

        txt.tag_add(num,'1.0',INSERT)
        txt.tag_config(num,font=(cur_font_name.get(),cur_font_size.get()),foreground=cur_font_color.get())

    else:
        cur_font_name.set(new_font)
        cur_font_size.set(new_size)
        print("Debug "+ tags[-1])
        if txt.tag_ranges(tags[-1])==() and len(tags)==1:
            txt.tag_add(num,'1.0',INSERT)
            txt.tag_config(num,font=(cur_font_name.get(),cur_font_size.get()),foreground=cur_font_color.get())

        elif txt.tag_ranges(tags[-1])==():
            for tag in tags:
                if tag == ():
                    txt.tag_delete(tag)
            
            txt.tag_add(num,'1.0',INSERT)
            txt.tag_config(num,font=(cur_font_name.get(),cur_font_size.get()),foreground=cur_font_color.get())
            
        else:

            txt.tag_add(num,txt.tag_ranges(tags[-1])[1],INSERT)
            txt.tag_config(num,font=(cur_font_name.get(),cur_font_size.get()),foreground=cur_font_color.get())

       

    #txt.tag_config(new_font,font=(new_font,new_size))


    txt.config(font= (new_font,new_size),foreground=cur_font_color.get())
    txt.pack(expand=True,fill="both")
    cur_tags.set(num+1)
    #txt.insert("1.0",data.get())


    #data = txt.get("1.0","end")
    #txt.delete("1.0","end")

    return




def open_file():
    filepath = askopenfilename(filetypes=[("Text file", "*.txt"),("All Files","*.*")])
    if not filepath:
        return
    txt.delete("1.0",END)
    with open(filepath, mode='r', encoding='utf-8') as input_file:
        text = input_file.read()
        txt.insert(END, text)
        window.title(f'Simple Text Editor - {filepath}')

def save_file():
    filepath = asksaveasfilename(defaultextension='.txt', filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not filepath:
        return
    with open(filepath, mode='w', encoding='utf-8') as output_file:
        text = txt.get('1.0', END)
        output_file.write(text)
        window.title(f'Simple Text Editor - {filepath}')
        


def ret_available_fonts():
    fonts = tk_font.families()
    
    return fonts
    
def get_combobox_selected(combobox_font: ttk.Combobox,combobox_size: ttk.Combobox,cmb_num):
    
    if(cmb_num == 1):
        update_txt(combobox_font.get(),combobox_size.get(),cur_tags.get())

    return 


def change_font_color():
    color = askcolor()
    if(color):
        cur_font_color.set(color[1]) 

        txt.config(fg=cur_font_color.get())
        txt.pack(expand=True,fill="both")
    else:
        pass

    return
    
    
def disp_txt_settings(wndw: Toplevel,alivebtn: list):
    for thing in alive_widgets:
        thing.destroy()
    try:

        if alivebtn[0]["state"] == NORMAL:
            alivebtn[0]["state"] = DISABLED

        if alivebtn[1]["state"] == DISABLED:
            alivebtn[1]["state"] = NORMAL

    except:
        print("paper settings not alive, ignoring state")

    size_values = [1,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40]
    
    r_view = Frame(wndw)
    r_view.pack(side=LEFT,fill='both',padx=5)
    
    
    rl_view = Frame(r_view)
    rl_view.pack(side=LEFT,fill='y',padx=15)
    
    rr_view = Frame(r_view)
    rr_view.pack(side=LEFT,fill='y',padx=5)
    
    
    font = Label(rl_view,text="Font: ",width=5,height=2)
    font.pack()
    font_boxes = Frame(rl_view)

    font_name_cmbx =ttk.Combobox(font_boxes,values=ret_available_fonts(), width=15)
    font_size_cmbx = ttk.Combobox(font_boxes,values=size_values, width=2)

    font_name_cmbx.pack(side=LEFT)
    font_size_cmbx.pack(side=RIGHT)

    font_boxes.pack()
    
    font_cmbx_apply = Button(rr_view,command=lambda: get_combobox_selected(font_name_cmbx,font_size_cmbx,1),text="Apply",pady=15,width=5)
    font_cmbx_apply.pack()

    color_picker_lbl = Label(rl_view,text="Change font color: ",pady=15)
    color_picker = Button(rl_view,text="Pick",command=change_font_color,pady=15,width=20)

    color_picker_lbl.pack()
    color_picker.pack()

    view_color = Label(rr_view, text="ABCDE",width=5,fg=cur_font_color.get(),pady=25)
    view_color.pack()

    alive_widgets.append(r_view);alive_widgets.append(rl_view); alive_widgets.append(rr_view)


    

    return

def disp_paper_settings(wndw: Toplevel, alivebtn: list):

    for thing in alive_widgets:
        thing.destroy()
    
    if alivebtn[1]["state"] == NORMAL:
        alivebtn[1]["state"] = DISABLED

    if alivebtn[0]["state"] == DISABLED:
        alivebtn[0]["state"] = NORMAL

    return
    

def open_settings():

    sidebar_wdth = '10'
    settings_wdw = Toplevel(window)
    settings_wdw.geometry("590x500")
    settings_wdw.title("Settings")
    sidebar = Frame(settings_wdw,width=sidebar_wdth)
    sidebar.pack(side=LEFT,fill='y',)
    txt_settings_btn= Button(sidebar,text="Text",width=sidebar_wdth,command=lambda: disp_txt_settings(settings_wdw,alive_btn),pady=10)
    txt_settings_btn.pack()

    if txt_settings_btn["state"] == DISABLED:
        txt_settings_btn["state"] = NORMAL

    paper_settings_btn = Button(sidebar,text="Paper",width=sidebar_wdth, command=lambda: disp_paper_settings(settings_wdw,alive_btn),pady=10)
    paper_settings_btn.pack()

    if paper_settings_btn["state"] == DISABLED:
        paper_settings_btn["state"] = NORMAL

    alive_btn.append(txt_settings_btn)
    alive_btn.append(paper_settings_btn)
    
    
    return


menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)


menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save As...', command=save_file)
filemenu.add_command(label='Settings',command=open_settings)


window.mainloop()