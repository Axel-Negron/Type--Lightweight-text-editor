from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as tk_font
from tkinter import ttk 



#Font variables#
cur_font_name = 'Calibri '
cur_font_size = '14'
#




window = Tk()
window.title("Text Editor")


txt = Text(window, fg='purple', bg='light yellow', font= cur_font_name+cur_font_size)
txt.pack(expand=True,fill="both")






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
    
def get_combobox_selected(combobox: ttk.Combobox,cmb_num):
    
    match cmb_num:
        
        case '1':
            
            cur_font_name = str(combobox.get())+" "
            
    
    return 
    
    
    
def disp_txt_settings(wndw: Toplevel):
    r_view = Frame(wndw)
    r_view.pack(side=LEFT,fill='both',padx=5)
    
    
    rl_view = Frame(r_view)
    rl_view.pack(side=LEFT,fill='y',padx=15)
    
    rr_view = Frame(r_view)
    rr_view.pack(side=LEFT,fill='y',padx=5)
    
    
    font = Label(rl_view,text="Font: ",width=5,height=2  )
    font.pack()
    
    
    font_cmbx =ttk.Combobox(rl_view,values=ret_available_fonts())
    font_cmbx.pack()
    
    font_cmbx_apply = Button(rr_view,command=lambda: get_combobox_selected(font_cmbx,1),text="Apply",pady=15,width=5)
    font_cmbx_apply.pack()
    
    font_name = cur_font_name
    font_size = cur_font_size
    
    print(type(wndw))
    return

def disp_paper_settings(wndw: Toplevel):
    
    return
    

def open_settings():
    sidebar_wdth = '10'
    settings_wdw = Toplevel(window)
    settings_wdw.geometry("590x500")
    settings_wdw.title("Settings")
    sidebar = Frame(settings_wdw,width=sidebar_wdth)
    sidebar.pack(side=LEFT,fill='y',)
    txt_settings_btn= Button(sidebar,text="Text",width=sidebar_wdth,command=lambda: disp_txt_settings(settings_wdw))
    txt_settings_btn.pack()
    paper_settings_btn = Button(sidebar,text="Paper",width=sidebar_wdth, command=lambda: disp_paper_settings(settings_wdw))
    paper_settings_btn.pack()
    
    
    return



menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)


menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save As...', command=save_file)
filemenu.add_command(label='Settings',command=open_settings)


window.mainloop()