Gravatar.py
===========

A simple Python library for accessing and cacheing Gravatar images.

wxPython Example
----------------

    import wx, Gravatar, StringIO
    
    cache = Gravatar.AvatarCache("cache")
    def wxGravatarImage(User, **kwargs):
        return wx.BitmapFromImage(
    	    wx.ImageFromStream(
                StringIO.StringIO(
                    cache.Image(User, **kwargs)
                )
            )
        )
    
    class ImageForm(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, -1, "wxGravatar Test", size=(400,400))
            Bitmap = wxGravatarImage("example@mydomain.com", Size=128,
                DefaultImage=Gravatar.DefaultImage.IdentIcon)
            wx.StaticBitmap(self, -1, Bitmap, (5,5))
    
    class MyApp(wx.App):
        def OnInit(self):
            MainPanel = ImageForm()
            MainPanel.Show()
            return True
    
    App = MyApp(redirect=False).MainLoop()

