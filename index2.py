import win32clipboard

CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")

rtf = 'test'

win32clipboard.OpenClipboard(0)
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, rtf)
win32clipboard.CloseClipboard()