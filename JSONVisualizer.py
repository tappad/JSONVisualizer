#!/usr/bin/python2.6
'''
    JSONVisualizer
    - A simple json tree visualizer
'''
__VERSION__ = '0.0.1'

import wx
import os.path, dircache

class JSONVisualizer(wx.Frame):
    def __init__(self, jsonObj, windowTitle, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.tree = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)
        self.Layout()
        self.SetTitle(windowTitle)
        self.jsonObj = jsonObj
        self.rootID = self.tree.AddRoot('root')
#        try:
        self.buildJSONTree(jsonObj, self.rootID)
#        except:
#            pass
        self.tree.Expand(self.rootID)
        self.SetSize((500,500))
    def buildJSONTree(self, jsonObj, parentID):
        if jsonObj == None:
            self.tree.AppendItem(parentID, 'None')
            return
        if isinstance(jsonObj, dict):
            for (k,v) in jsonObj.iteritems():
                childID = self.tree.AppendItem(parentID, k.encode('utf8'))
                self.buildJSONTree(v, childID)
                self.tree.Expand(childID)
        elif isinstance(jsonObj, list):
            for item in jsonObj:
                childID = self.tree.AppendItem(parentID, '[]')
                self.buildJSONTree(item, childID)
                self.tree.Expand(childID)
        else:
            if isinstance(jsonObj, basestring):
                jsonObj = jsonObj.encode('utf8')
            self.tree.AppendItem(parentID, str(jsonObj))

if __name__ == "__main__":
    try:
        import sys
        from json import load
        title = "JSONVisualizer - %s"
        if len(sys.argv) > 1:
            f = open(sys.argv[1], 'r')
            title = title % sys.argv[1]
        else:
            f = sys.stdin
            title = title % "stdin"
        jsonObj = load(f)
        f.close()
        app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        frame = JSONVisualizer(jsonObj, title, None, -1, "")
        app.SetTopWindow(frame)
        frame.Show()
        app.MainLoop()
    except Exception as ex:
        print ex
        raise
