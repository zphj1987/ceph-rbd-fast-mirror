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

def main():

    def read_conf(object):
        getconf=commands.getoutput('ceph-conf --lookup -c /ceph.conf %s 2>/dev/null' %object)
        return getconf
    def write_conf(content,object):
        writeconf=commands.getoutput('sed -i "s/%s=.*/%s=%s/g" /ceph.conf  2>/dev/null' %(object,object,content))
        #writeconf=commands.getoutput('echo %s %s %s' %(object,object,content))
        return writeconf

    text_header = (u"欢迎使用fast copy  "
        u"可以使用 F8 exits.")
    text_footer = (u"Welcome to the urwid tour!  "
        u"UP / DOWN / PAGE UP / PAGE DOWN scroll.  jiao.")
    text_intro = [('important', u"Text"),
        u" widgets are the most common in "
        u"any urwid program.  This Text widget was created "
        u"without setting the wrap or align mode, so it "
        u"defaults to left alignment with wrapping on space "
        u"characters.  ",
        ('important', u"Change the window width"),
        u" to see how the widgets on this page react.  "
        u"This Text widget is wrapped with a ",
        ('important', u"Padding"),
        u" widget to keep it indented on the left and right."]
    text_edit_origin_mon = ('editcp', u"输入原ceph集群的monip: ")
    text_edit_dest_mon = ('editcp', u"输入目标ceph集群的monip: ")
    text_edit_text1 = read_conf('originmon')
    text_edit_text2 = u"A"
    reply = urwid.Text(u"")
    button = urwid.Button(u'保存配置')
    blank = urwid.Divider()
    editoriginmon=urwid.Edit(text_edit_origin_mon,text_edit_text1)
    savebutton=urwid.AttrWrap(urwid.Button(u'保存配置'),'buttn')
    listbox_content = [
        urwid.Padding(urwid.Text(text_intro), left=2, right=2, min_width=40),
        urwid.AttrWrap(editoriginmon,
            'editbx', 'editfc'),
        blank,
        urwid.AttrWrap(urwid.Edit(text_edit_dest_mon,text_edit_text2),
            'editbx', 'editfc'),
        urwid.Padding(savebutton,'center',20),
        reply,
        ]

    def on_exit_clicked(button):
#        raise urwid.ExitMainLoop()
        try:
            write_conf(myedit,'originmon')
            print  write_conf(myedit,'originmon')
        except:
            pass


    def on_save_change(edit, edit_addr):
        global myedit
        myedit= edit_addr
    urwid.connect_signal(button, 'click', on_exit_clicked)
    urwid.connect_signal(editoriginmon, 'change', on_save_change)


    #AttrWrap是用来给文本设置颜色，属性
    header = urwid.AttrWrap(urwid.Text(text_header), 'header')
    footer = urwid.AttrWrap(urwid.Text(text_footer), 'header')
    

    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
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
        unhandled_input=unhandled).run()

def setup():

    main()

if '__main__'==__name__ :
    setup()
