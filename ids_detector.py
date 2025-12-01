import socket
import time
import select
from datetime import datetime
import platform
from dashboard import push_attack_event  #


# Signatures and mappings


ALERT_SIGNATURES = {
    b"SELECT * FROM users": "SQL injection detected",
    b"admin'--": "SQL injection attempt",
    b"<script>": "XSS attack detected",
    b"../": "Directory traversal detected"
}

ATTACK_KEY_MAP = {
    "SQL injection detected": "sql",
    "SQL injection attempt": "sql_injection",
    "XSS attack detected": "xss",
    "Directory traversal detected": "dir_traversal",
}

LOG_FILE = "ids_alerts.log"


# Setup and entry point

def test_setup():
    print("🎉 IDS setup test - all systems ready!")
    print(f"Alert signatures loaded: {len(ALERT_SIGNATURES)} patterns")
    print(f"Log file: {LOG_FILE}")
    print("✅ Pure Python loopback IDS ready! (No sudo needed)")


def packet_sniffer():
    system = platform.system()
    print(f"🖥️ OS Detected: {system}")
    
    if system == "Linux":
        print("🐧 Using Linux Pure Python sniffer...")
        linux_packet_sniffer()
    elif system == "Windows":
        print("🪟 Using Windows sniffer...")
        windows_packet_sniffer()
    else:
        print("❌ Unsupported OS!")

# Linux loopback IDS

def linux_packet_sniffer():
    """Pure Python TCP/UDP loopback IDS - NO sudo needed."""
    print("✅ Pure Python loopback IDS ready!")
    
    # TCP socket (port 8080) for HTTP-style traffic
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind(("127.0.0.1", 8080))
    tcp_sock.listen(5)
    
    # UDP socket (port 8080) for other traffic
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("127.0.0.1", 8080))
    
    print("🔍 Monitoring TCP+UDP loopback on port 8080... Ctrl+C to stop")
    
    packet_count = 0
    while True:
        try:
            ready_read, _, _ = select.select([tcp_sock, udp_sock], [], [], 0.1)
            
            for sock in ready_read:
                packet_count += 1
                
                if sock == tcp_sock:
                    conn, addr = tcp_sock.accept()
                    data = conn.recv(1024)
                    conn.close()
                    print(f"📦 TCP Packet #{packet_count} | From: {addr}")
                else:
                    data, addr = udp_sock.recvfrom(1024)
                    print(f"📦 UDP Packet #{packet_count} | From: {addr}")
                
                print(f"   Data (hex): {data[:100].hex()}")
                
                # Attack detection
                for signature, alert_msg in ALERT_SIGNATURES.items():
                    if signature in data:
                        print(f"🚨 ATTACK DETECTED: {alert_msg}")
                        log_alert(addr, signature, alert_msg)
                
                print("-" * 60)
        
        except KeyboardInterrupt:
            print("\n[*] Loopback IDS stopped.")
            break
        except Exception as e:
            print(f"⚠️  Sniffer error: {e}")

# Logging + dashboard push

def log_alert(addr, signature, alert_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = f"[{timestamp}] {alert_msg} from {addr[0]} | Signature: {signature.decode()}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(alert)
    print(f"📝 Logged to {LOG_FILE}")

    key = ATTACK_KEY_MAP.get(alert_msg)
    if key:
        try:
            push_attack_event(key, alert_msg, addr[0])
        except Exception as e:
            print("ERROR in push_attack_event:", e)


# Windows placeholder

def windows_packet_sniffer():
    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sniffer.bind(("0.0.0.0", 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        print("✅ Windows sniffer ready! (admin mode required)")
        # You can add Windows detection logic here similar to Linux if needed.
    except Exception as e:
        print(f"❌ Windows error: {e}")

# Main

if __name__ == "__main__":
    test_setup()
    packet_sniffer()
