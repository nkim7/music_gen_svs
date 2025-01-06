import uiautomation as auto
import time
import os

def main():
    # Step 1: Start the OpenUtau application and wait for it to load.
    openutau_path = r"C:\Users\nagyu\Downloads\OpenUtau-win-x86\OpenUtau.exe"
    os.startfile(openutau_path)
    print("OpenUtau application has been started, waiting for it to load...")

  
    time.sleep(2)

    # Step 2: Locate the OpenUtau window
    openutau_window = auto.WindowControl(searchDepth=1, Name="OpenUtau v0.1.529.0")
    if not openutau_window.Exists(5):
        raise Exception("Failed to find the OpenUtau window.")
    print("OpenUtau window found.")

    # Step 3: Find and click the 'File' menu
    file_menu = openutau_window.MenuItemControl(searchDepth=11, Name="File")
    if not file_menu.Exists(5):
        raise Exception("Failed to find the 'File' menu item.")
    file_menu.Click()
    print("'File' menu has been clicked.")

    # Step 4: Find and double-click the 'Open...' menu item
    open_menu_item = openutau_window.MenuItemControl(searchDepth=13, Name="Open...")
    if not open_menu_item.Exists(5):
        raise Exception("Failed to find the 'Open...' menu item.")
    

    open_menu_item.DoubleClick()
    print("'Open...' menu item has been double-clicked successfully.")

    # Step 5: Locate the 'Open' file dialog
    file_dialog = auto.WindowControl(searchDepth=8, ControlType=auto.ControlType.WindowControl)
    if not file_dialog.Exists(5):
        raise Exception("Failed to find the 'Open' file dialog.")
    print("File dialog found.")

    # Step 6: Find the 'output.ustx' file 
    output_ustx_file = file_dialog.ListItemControl(searchDepth=19, Name="output.ustx")
    if not output_ustx_file.Exists(5):
        raise Exception("Failed to find the 'output.ustx' file.")
    

    output_ustx_file.DoubleClick()
    print("'output.ustx' file has been double-clicked successfully.")

    # Step 7: Wait for the file to fully load
    time.sleep(10) 

    # Step 8: Find and click the 'File' menu 
    file_menu = openutau_window.MenuItemControl(searchDepth=11, Name="File")
    if not file_menu.Exists(5):
        raise Exception("Failed to find the 'File' menu item.")
    file_menu.Click()
    print("'File' menu has been clicked again.")

    # Step 9: Find the 'Export Audio'
    export_audio_menu_item = openutau_window.MenuItemControl(searchDepth=26, Name="Export Audio")
    if not export_audio_menu_item.Exists(5):
        raise Exception("Failed to find the 'Export Audio' menu item.")
    
  
    export_audio_menu_item.Click()
    print("'Export Audio' menu item has been clicked.")

    # Step 10: Find the 'Export Wav Files To...' menu item 
    export_wav_menu_item = openutau_window.MenuItemControl(searchDepth=27, Name="Export Wav Files To...")
    if not export_wav_menu_item.Exists(5):
        raise Exception("Failed to find the 'Export Wav Files To...' menu item.")
    
 
    export_wav_menu_item.Click()
    print("'Export Wav Files To...' menu item has been clicked successfully.")

    # Step 11: Locate the 'File name:' edit box and enter "music"
    file_name_edit = auto.EditControl(searchDepth=8, Name="File name:")
    if not file_name_edit.Exists(5):
        raise Exception("Failed to find the 'File name:' edit box.")
    

    file_name_edit.SendKeys("music")
    print("File name has been set to 'music'.")

    # Step 12: Find the 'Save' button and click it
    save_button = auto.ButtonControl(searchDepth=3, Name="Save")
    if not save_button.Exists(5):
        raise Exception("Failed to find the 'Save' button.")
    

    save_button.Click()
    print("Save button has been clicked successfully.")

  
    # Step 14: Find the 'Close' button in depth 2 and click it
    close_button = openutau_window.ButtonControl(searchDepth=2, Name="Close")
    if not close_button.Exists(5):
        raise Exception("Failed to find the 'Close' button.")
    

    close_button.Click()
    print("Close button has been clicked, closing the window.")

if __name__ == '__main__':
    main()
