import socket

domain = "zaakqeqkedwupfzytxlh.supabase.co"
print(f"Testing connection to {domain}...")

try:
    ip = socket.gethostbyname(domain)
    print(f"✅ Success! Supabase IP found: {ip}")
except Exception as e:
    print(f"❌ DNS Error: {e}")
    print("Iska matlab aapka Wi-Fi, ISP, ya Antivirus is URL ko block kar raha hai.")