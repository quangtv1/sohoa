import win32com.shell.shell as shell
import win32gui
import win32con

def browse_directory():
    browse_info = shell.SHBrowseInfo()
    browse_info.HwndOwner = win32gui.GetActiveWindow()
    browse_info.ulFlags = win32con.BIF_NEWDIALOGSTYLE | win32con.BIF_EDITBOX
    browse_info.lpfn = browse_callback
    shell.SHBrowseForFolder(browse_info)

def browse_callback(hwnd, msg, lParam, lpData):
    if msg == win32con.BFFM_INITIALIZED:
        win32gui.SendMessage(hwnd, win32con.BFFM_SETSELECTION, 1, lpData)

    elif msg == win32con.BFFM_SELCHANGED:
        selected_path = win32gui.SendMessage(hwnd, win32con.BFFM_GETSELECTEDITEM, 0, None)
        selected_path = shell.SHGetPathFromIDList(selected_path)
        win32gui.SendMessage(hwnd, win32con.BFFM_SETSTATUSTEXT, 0, selected_path)

    return 0

def main():
    browse_directory()

if __name__ == "__main__":
    main()
