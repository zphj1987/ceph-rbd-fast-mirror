#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Urwid web site: http://excess.org/urwid/

"""
Urwid tour.  Shows many of the standard widget types and features.
"""
import os
import urwid
import commands
import urwid.raw_display


####################
class PopUpDialog(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__(self):
        close_button = urwid.Button("that's pretty cool")
        urwid.connect_signal(close_button, 'click',
            lambda button:self._emit("close"))
        pile = urwid.Pile([urwid.Text(
            "^^  I'm attached to the widget that opened me. "
            "Try resizing the window!\n"), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))

class ThingWithAPopUp(urwid.PopUpLauncher):
    def __init__(self):
        self.__super.__init__(urwid.Button("click-me"))
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = PopUpDialog()
        urwid.connect_signal(pop_up, 'close',
            lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':32, 'overlay_height':7}

####################

def main():

    def read_conf(object):
        """
        读取目标配置文件传入的是要读取的配置文件
        """
        getconf=commands.getoutput('ceph-conf --lookup -c /ceph.conf %s 2>/dev/null' %object)
        return getconf
    
    
    def write_conf(content,object):
        """
        写入配置文件：
        content为写入的内容，object为写入的配置字段
        """       
        writeconf=commands.getoutput('sed -i "s/%s=.*/%s=%s/g" /ceph.conf  2>/dev/null' %(object,object,content))
    text_header = (u"欢迎使用fast copy  "
        u"可以使用 F8 exits.")
    text_footer = (u"Welcome to the urwid tour!  "
        u"UP / DOWN / PAGE UP / PAGE DOWN scroll.  jiao.")
    text_intro = [('important', u"Text"),
        u"本工具是用于快速的复制 "
        u"一个RBD到另外的一个集群的"]
    text_edit_origin_mon = ('editcp', u"输入原始ceph集群的monip: ")
    text_edit_dest_mon = ('editcp', u"输入目标ceph集群的monip: ")
    text_edit_text1 = read_conf('originmon')
    text_edit_text2 = read_conf('destmon')
    
    button = urwid.Button(u'保存配置')
    blank = urwid.Divider()
    editoriginmon=urwid.Edit(text_edit_origin_mon,text_edit_text1)
    editdestmon=urwid.Edit(text_edit_dest_mon,text_edit_text2)
    savebutton=urwid.AttrWrap(button,'buttn')
    listbox_content = [
        urwid.Padding(urwid.Text(text_intro), left=2, right=2, min_width=40),
        urwid.Padding(urwid.AttrWrap(editoriginmon,
            'editbx', 'editfc'),left=2, width=50),
        blank,
        urwid.Padding(urwid.AttrWrap(editdestmon,
            'editbx', 'editfc'),left=2, width=50),
        blank,
        urwid.Padding(savebutton,left=2,width=12),
        ]



    def on_exit_clicked(button):
#        raise urwid.ExitMainLoop()
        try:
            if globals().has_key('myorinedit'):
                write_conf(myorinedit,'originmon')
            if globals().has_key('mydestedit'):
                write_conf(mydestedit,'destmon')  
            ThingWithAPopUp()         
        except:
            pass

    def on_save_change(edit, edit_addr,mysave):
        if mysave == 'origin':
            global myorinedit
            myorinedit = edit_addr
        elif mysave == 'dest':
            global mydestedit
            mydestedit = edit_addr

        

    
    urwid.connect_signal(button, 'click', on_exit_clicked)
    urwid.connect_signal(editoriginmon, 'change', on_save_change,'origin')
    urwid.connect_signal(editdestmon, 'change', on_save_change,'dest')


    #AttrWrap是用来给文本设置颜色，属性
    header = urwid.AttrWrap(urwid.Text(text_header), 'header')
    footer = urwid.AttrWrap(urwid.Text(text_footer), 'header')
    

    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
#    listbox = urwid.Filler(urwid.Padding(ThingWithAPopUp(), 'center', 15))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header,footer=footer)

    palette = [
        ('body','black','light gray', 'standout'),
        ('reverse','light gray','black'),
        ('header','white','dark red', 'bold'),
        ('important','dark blue','light gray',('standout','underline')),
        ('editfc','white', 'dark blue', 'bold'),
        ('editbx','light gray', 'dark blue'),
        ('editcp','black','light gray', 'standout'),
        ('bright','dark gray','light gray', ('bold','standout')),
        ('buttn','black','dark cyan'),
        ('buttnf','white','dark blue','bold'),
        ]

    # use appropriate Screen class

    screen = urwid.raw_display.Screen()

    def unhandled(key):
        if key == 'f8':
            raise urwid.ExitMainLoop()

    urwid.MainLoop(frame, palette, screen,
        unhandled_input=unhandled,pop_ups=True).run()

def setup():

    main()

if '__main__'==__name__ :
    setup()
