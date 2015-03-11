import struct
import _winreg
import sys
def changeProxyer(proxy = "127.0.0.1:8118"):
    root = _winreg.HKEY_CURRENT_USER    
    proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    kv_Enable = [
      (proxy_path, "ProxyEnable", 1, _winreg.REG_DWORD),
      (proxy_path, "ProxyServer", proxy, _winreg.REG_SZ),
    ]    
            
    #set proxyer
    for keypath, value_name, value, value_type in kv_Enable:
        hKey = _winreg.CreateKey (root, keypath)
        _winreg.SetValueEx (hKey, value_name, 0, value_type, value)  

    # kv_Disable = [
          # (proxy_path, "ProxyEnable", 0, _winreg.REG_DWORD),
          # (proxy_path, "ProxyServer", proxy, _winreg.REG_SZ),
        # ]
        
        ##read proxy status
        #hKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, proxy_path)
        #value, type = _winreg.QueryValueEx(hKey, "ProxyEnable")
        #kv = kv_Enable
        #result = "Enabled"
        #if value:
            #result = "Disabled"
            #kv = kv_Disable
            
#read proxyer
proxyers = []
for line in open("proxy.txt"):
    print line
    ip,port = line.strip().split("\t")
    proxyers.append(ip+":"+port)   

#proxy = sys.argv[1]
for proxy in proxyers:
    changeProxyer(proxy)
print "Hello Kitty"