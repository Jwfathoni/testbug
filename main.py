import socket
import ssl
import datetime

def scan_pro():
    print("="*40)
    print("   ADVANCED IP CLEAN SCANNER v2.0   ")
    print("="*40)
    
    # Fitur Ubah SNI
    bug_sni = input("[?] Masukkan SNI/Bug (contoh: support.zoom.us.nautica.dedefathu.my.id): ")
    if not bug_sni:
        print("[!] SNI tidak boleh kosong!")
        return

    # Daftar range IP Cloudflare yang populer
    ranges = ["172.64.0.", "172.67.73.", "162.159.135.", "104.21.10.", "104.22.5."]
    
    file_name = "hasil_scan.txt"
    
    print(f"\n[*] Memulai Scan...")
    print(f"[*] Target SNI : {bug_sni}")
    print(f"[*] Output File: {file_name}\n")
    print("-" * 40)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    found_count = 0

    with open(file_name, "a") as f:
        # Menulis header di file txt
        f.write(f"\n--- Hasil Scan: {datetime.datetime.now()} ---\n")
        f.write(f"SNI: {bug_sni}\n")
        
        for r in ranges:
            for i in range(1, 100): # Scan range .1 sampai .99
                ip = f"{r}{i}" 
                try:
                    # Timeout singkat agar proses cepat
                    sock = socket.create_connection((ip, 443), timeout=1.0)
                    with context.wrap_socket(sock, server_hostname=bug_sni) as ssock:
                        # Kirim dummy request untuk memastikan jalur benar-benar terbuka
                        request = f"GET / HTTP/1.1\r\nHost: {bug_sni}\r\n\r\n"
                        ssock.send(request.encode())
                        
                        result = f"[+] {ip:15} --> [ AMAN ]"
                        print(result)
                        
                        # Simpan ke file txt
                        f.write(f"{ip}\n")
                        found_count += 1
                    sock.close()
                except ConnectionResetError:
                    print(f"[-] {ip:15} --> [ RESET ]")
                except Exception:
                    # Lewati IP yang tidak aktif (Timeout/Offline)
                    pass

    print("-" * 40)
    print(f"[*] Selesai! Menemukan {found_count} IP Aman.")
    print(f"[*] Hasil tersimpan di: {file_name}")
    print("="*40)

if __name__ == "__main__":
    scan_pro()
