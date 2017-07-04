#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Urwid web site: http://excess.org/urwid/

"""
Urwid tour.  Shows many of the standard widget types and features.
"""
import os,ast
import urwid
import commands
import urwid.raw_display

####################
class PopUpDialog(urwid.WidgetWrap):
    """保存按钮的弹出框 """
    signals = ['close']
    def write_conf(self,content,object):     
        writeconf=commands.getoutput('sed -i "s/%s=.*/%s=%s/g" /ceph.conf  2>/dev/null' %(object,object,content))
    def __init__(self):

        close_button = urwid.Button("返回")
        urwid.connect_signal(close_button, 'click',
            lambda button:self._emit("close"))
        pile = urwid.Pile([urwid.Text(
            "保存成功"), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))
        try:
            if globals().has_key('myorinedit'):
                self.write_conf(myorinedit,'originmon')
            if globals().has_key('mydestedit'):
                self.write_conf(mydestedit,'destmon')
            if globals().has_key('mypool'):
                self.write_conf(mypool,'pool')
            if globals().has_key('myrbd'):
                self.write_conf(myrbd,'rbd')
            if globals().has_key('mymd5'):
                self.write_conf(mymd5,'md5')
            if globals().has_key('mythread'):
                self.write_conf(mythread,'thread')      
        except:
                pass        

class ThingWithAPopUp(urwid.PopUpLauncher):
    def __init__(self):
        self.__super.__init__(urwid.Button(u'保存配置'))
        urwid.connect_signal(self.original_widget, 'click',
            lambda button: self.open_pop_up())

    def create_pop_up(self):
        pop_up = PopUpDialog()
        urwid.connect_signal(pop_up, 'close',
            lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':5, 'top':5, 'overlay_width':20, 'overlay_height':4}

####################

def main():

    def read_conf(object,type):
        """
        读取目标配置文件传入的是要读取的配置文件
        """
        if type == "conf":
            getconf=commands.getoutput('ceph-conf --lookup -c /ceph.conf %s 2>/dev/null' %object)
            return getconf
        if type == "getlist":
            getcount=commands.getoutput('cat %s|wc -l 2>/dev/null' %object)
            return getcount
    def write_conf(content,object):
        """
        写入配置文件：
        content为写入的内容，object为写入的配置字段
        """       
        writeconf=commands.getoutput('sed -i "s/%s=.*/%s=%s/g" /ceph.conf  2>/dev/null' %(object,object,content))
    text_header = (u"欢迎使用fast copy  "
        u"可以使用 F8 exits.")
    text_footer = (u"Develop by 运维-武汉-磨渣 "
        u"UP / DOWN / PAGE UP / PAGE DOWN scroll.")
    text_intro = [
        u"本工具是用于快速的复制 "
        u"一个RBD到另外的一个集群的"]
    text_edit_origin_mon = ('editcp', u"输入原始ceph集群的monip: ")
    text_edit_dest_mon = ('editcp', u"输入目标ceph集群的monip: ")
    text_edit_dest_pool = ('editcp', u"输入存储池: ")
    text_edit_dest_rbd = ('editcp', u"输入RBD Image Name: ")

    text_edit_text1 = read_conf('originmon','conf')
    text_edit_text2 = read_conf('destmon','conf')
    text_edit_text3 = read_conf('pool','conf')
    text_edit_text4 = read_conf('rbd','conf')

    text_edit_thread = ('editcp', u"并发数: ")
    text_edit_text5 = read_conf('thread','conf')
    text_getcont = read_conf('/getlist','getlist')
    text_getcont = [('important', u"原始RBD对象数目： "),
        u"%s" %text_getcont]

    zp=urwid.Padding(ThingWithAPopUp(), 'center', 15)
    checkbox_md5_choose = ast.literal_eval(read_conf('md5','conf'))

    checkbox_md5="md5记录" 

    blank = urwid.Divider()
    editoriginmon=urwid.Edit(text_edit_origin_mon,text_edit_text1)
    editdestmon=urwid.Edit(text_edit_dest_mon,text_edit_text2)
    editdestpool=urwid.Edit(text_edit_dest_pool,text_edit_text3)
    editdestrbd=urwid.Edit(text_edit_dest_rbd,text_edit_text4)

    newsavebutton=urwid.AttrWrap(zp,'buttn')

    md5cb=urwid.CheckBox(checkbox_md5,checkbox_md5_choose)
    editthread=urwid.Edit(text_edit_thread,text_edit_text5)
    getobjectcount=urwid.Text(text_getcont)
    listbox_content = [
        urwid.Padding(urwid.Text(text_intro), left=2, right=2, min_width=40),
        urwid.Padding(urwid.AttrWrap(editoriginmon,
            'editbx', 'editfc'),left=2, width=50),
        blank,
        urwid.Padding(urwid.AttrWrap(editdestmon,
            'editbx', 'editfc'),left=2, width=50),
        blank,
        urwid.Padding(urwid.AttrWrap(editdestpool,
            'editbx', 'editfc'),left=2, width=50),
        blank,
        urwid.Padding(urwid.AttrWrap(editdestrbd,
            'editbx', 'editfc'),left=2, width=50),
        blank,
        urwid.Padding(newsavebutton,left=10,width=15),
        urwid.AttrWrap(urwid.Divider("-", 1), 'bright'),

        urwid.AttrWrap(urwid.Divider("-", 1), 'bright'),

#        urwid.GridFlow([urwid.Padding(urwid.AttrWrap(md5cb, 'buttn','buttnf'),left=4, right=3, width=12),
#        urwid.Padding(urwid.AttrWrap(md5cb, 'buttn','buttnf'),left=4, right=3, width=12)],13, 3, 1, 'left'),
#        urwid.Padding(urwid.AttrWrap(editthread,
#            'editbx', 'editfc'),left=2, width=20),
        urwid.Padding(getobjectcount,left=2, width=50),
        ]


    def on_save_change(edit, edit_addr,mysave):
        if mysave == 'origin':
            global myorinedit
            myorinedit = edit_addr
        elif mysave == 'dest':
            global mydestedit
            mydestedit = edit_addr
        elif mysave == 'pool':
            global mypool
            mypool = edit_addr
        elif mysave == 'rbd':
            global myrbd
            myrbd = edit_addr
        elif mysave == 'md5':
            global mymd5
            mymd5 = edit_addr
        elif mysave == 'thread':
            global mythread
            mythread = edit_addr

        
    urwid.connect_signal(editoriginmon, 'change', on_save_change,'origin')
    urwid.connect_signal(editdestmon, 'change', on_save_change,'dest')
    urwid.connect_signal(editdestpool, 'change', on_save_change,'pool')    
    urwid.connect_signal(editdestrbd, 'change', on_save_change,'rbd')
    urwid.connect_signal(md5cb, 'change', on_save_change,'md5')
    urwid.connect_signal(editthread, 'change', on_save_change,'thread')

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
        unhandled_input=unhandled,pop_ups=True).run()

def setup():

    main()

if '__main__'==__name__ :
    setup()
