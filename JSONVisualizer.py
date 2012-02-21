'''
    JSONVisualizer
    - A simple json tree visualizer
'''
__VERSION__ = '0.0.1'

import wx
import os.path, dircache

class JSONVisualizer(wx.Frame):
    def __init__(self, jsonObj, *args, **kwds):
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

        self.jsonObj = jsonObj
        self.rootID = self.tree.AddRoot('root')
        try:
            self.buildJSONTree(jsonObj, self.rootID)
        except:
            pass
    def buildJSONTree(self, jsonObj, parentID):
        if jsonObj == None:
            self.tree.AppendItem(parentID, 'None')
            return
        if isinstance(jsonObj, dict):
            for (k,v) in jsonObj.iteritems():
                childID = self.tree.AppendItem(parentID, k)
                self.buildJSONTree(v, childID)
        elif isinstance(jsonObj, list):
            for item in jsonObj:
                childID = self.tree.AppendItem(parentID, '[]')
                self.buildJSONTree(item, childID)
        else:
            self.tree.AppendItem(parentID, str(jsonObj))

if __name__ == "__main__":
    try:
        import sys
        from json import load
        f = open(sys.argv[1], 'r')
        jsonObj = load(f)
        f.close()
        app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        frame = JSONVisualizer(jsonObj,None, -1, "")
        app.SetTopWindow(frame)
        frame.Show()
        app.MainLoop()
    except Exception as ex:
        print ex
