# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  6 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import wx
import wx.xrc
import wx.grid
from threading import Thread
from main_handler import get_track, create_query, file_handler, exists_query

###########################################################################
## Class MainFrame
###########################################################################

EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):

    def __init__(self, data, btn_on=False):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        self.btn_on = btn_on


class WikiaWorker(Thread):

    end = abort = False

    def __init__(self, wxObject):
        Thread.__init__(self)
        self.wxObject = wxObject
        self.counter = 0
        self.file_path = get_track(self.wxObject.query_file)
        self.start()

    def run(self):
        """ get lyrics for ich file """
        files = iter(self.file_path)
        while not (self.abort or self.end):
            try:
                file_ = next(files)
                result = file_handler(file_, self.wxObject.ch_box_rewrite.Value)
                self.counter += 1
                wx.PostEvent(self.wxObject, ResultEvent('%s -- %s' % (file_, result)))
            except StopIteration:
                self.end = True
        else:
            wx.PostEvent(self.wxObject, ResultEvent('Stopped' if self.abort else 'All done.', True))
        del files

    def stop(self):
        self.abort = True


class MainFrame(wx.Frame):

    vk_api = None
    worker = None
    query_file = exists_query()

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Lyrics importer", pos = wx.DefaultPosition, size = wx.Size( 600,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

        self.b_get_music = wx.Button( self.m_panel2, wx.ID_ANY, u"Music Path", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer16.Add( self.b_get_music, 0, wx.ALL, 5 )

        self.l_music_path = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_music_path.Wrap( -1 )
        self.l_music_path.SetMinSize( wx.Size( 350,-1 ) )

        bSizer16.Add( self.l_music_path, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.l_music_count = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_music_count.Wrap( -1 )
        bSizer16.Add( self.l_music_count, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer14.Add( bSizer16, 0, wx.EXPAND, 5 )

        self.m_staticline5 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer14.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

        sizer_new = wx.BoxSizer(wx.HORIZONTAL)
        self.b_something_fresh = wx.Button(self.m_panel2, wx.ID_ANY, u"Get Lyrics", wx.DefaultPosition, wx.DefaultSize, 0)
        self.b_stop_process = wx.Button(self.m_panel2, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0)
        self.ch_box_rewrite = wx.CheckBox(self.m_panel2, -1, u'Rewrite lyrics', wx.DefaultPosition, wx.DefaultSize, 0)
        self.ch_box_rewrite.SetValue(True)
        self.b_stop_process.Disable()
        self.b_something_fresh.Enable() if self.query_file else self.b_something_fresh.Disable()
        sizer_new.Add(self.b_something_fresh, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_new.Add(self.b_stop_process, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_new.Add(self.ch_box_rewrite, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        bSizer14.Add(sizer_new, 0, wx.EXPAND, 5)

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        self.listbox = wx.ListBox( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0 )
        bSizer18.Add( self.listbox, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer14.Add( bSizer18, 1, wx.EXPAND, 5 )

        self.m_panel2.SetSizer( bSizer14 )
        self.m_panel2.Layout()
        bSizer14.Fit( self.m_panel2 )
        bSizer1.Add( self.m_panel2, 1, wx.EXPAND, 5 )

        self.SetSizer( bSizer1 )
        self.Layout()
        self.status_bar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

        self.b_get_music.Bind( wx.EVT_BUTTON, self.create_music_query )
        self.b_something_fresh.Bind(wx.EVT_BUTTON, self.get_wikia_lyrics)
        self.b_stop_process.Bind(wx.EVT_BUTTON, self.stop_wikia)

        self.Show(True)

        EVT_RESULT(self, self.update_display)

    # @property
    # def params(self):
    #     num = lambda x: bool(x).numerator
    #     return [
    #         ('search_own', num(self.ch_own.GetValue())),
    #         ('performer_only', num(self.ch_artist.GetValue())),
    #         ('auto_complete', num(self.ch_auto.GetValue())),
    #         ('sort', self.b_choices.GetCurrentSelection())
    #     ]

    # def get_vk_token(self, event):
    #     self.vk_api = CallApi()
    #     if self.vk_api.token:
    #         self.l_vk_status.SetLabelText("Token gets successful")

    def create_music_query(self, event):
        """ Create query of all mp3 files in chosen dir """
        dlg = wx.DirDialog(self, "Choose input directory", "", wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            result, count = create_query(path.encode('utf-8'))
            self.query_file = result
            self.status_bar.SetStatusText("Query was created on %s" % result)
            self.l_music_path.SetLabelText("Query was created on %s" % result)
            self.l_music_count.SetLabelText("%s files exists" % count)
            self.listbox.Clear()
            for line in get_track(self.query_file):
                self.listbox.Append(line)
            self.b_something_fresh.Enable()
        dlg.Destroy()

    def get_wikia_lyrics(self, e):
        """ if query exists runs thread """
        if self.query_file:
            self.status_bar.SetStatusText("WAITING!!!!")
            self.listbox.Clear()
            self.worker = WikiaWorker(self)
            self.b_something_fresh.Disable()
            self.b_stop_process.Enable()
        else:
            self.status_bar.SetStatusText("Where query man?")

    def stop_wikia(self, e):
        self.b_stop_process.Disable()
        self.b_something_fresh.Enable()
        self.worker.stop()

    def update_display(self, msg):
        self.status_bar.SetStatusText(msg.data)
        self.listbox.Append(msg.data)
        if msg.btn_on:
            self.b_stop_process.Disable()
            self.b_something_fresh.Enable()

app = wx.App()
frame = MainFrame(None)
app.MainLoop()