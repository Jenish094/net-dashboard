import socket
import requests
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

def parseportrange(ports_range):
    ports = set()
    parts = str(ports_range).split(',')
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if '-' in p:
            try:
                a, b = p.split('-', 1)
                a = int(a); b = int(b)
                if a < 1: a = 1
                if b > 65535: b = 65535
                ports.update(range(a, b + 1))
            except Exception:
                continue
        else:
            try:
                v = int(p)
                if 1 <= v <= 65535:
                    ports.add(v)
            except Exception:
                continue
    return sorted(ports)


def probeport(target_ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        res = s.connect_ex((target_ip, port))
        print(f"[port_scanner] connect_ex result for {port}: {res}")
        if res == 0:
            print(f"[port_scanner] Open port: {port}")
            entry = {"port": port}
            try:
                url = f"http://{target_ip}:{port}"
                resp = requests.get(url, timeout=2)
                entry.update({"url": url, "status": resp.status_code})
                print(f"[port_scanner] Web server detected: {url} (status {resp.status_code})")
            except Exception:
                try:
                    warnings.filterwarnings('ignore')
                    url = f"https://{target_ip}:{port}"
                    resp = requests.get(url, timeout=2, verify=False)
                    entry.update({"url": url, "status": resp.status_code})
                    print(f"[port_scanner] Web server detected: {url} (status {resp.status_code})")
                except Exception:
                    pass
            s.close()
            return entry
    except Exception as e:
        print(f"[port_scanner] Error probing port {port}: {e}")
    try:
        s.close()
    except Exception:
        pass
    return None


def scanports(target_ip, ports_range="1-65535", timeout=1.0, max_workers=200):
    print(f"[port_scanner] TCP connect scanning {target_ip} ports {ports_range}")
    ports = parseportrange(ports_range)
    if not ports:
        print("[port_scanner] No valid ports parsed")
        return []

    results = []
    with ThreadPoolExecutor(max_workers=min(max_workers, len(ports))) as ex:
        futures = {ex.submit(probeport, target_ip, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    results.append(res)
            except Exception as e:
                print(f"[port_scanner] probe exception: {e}")

    print(f"[port_scanner] Scan complete: {len(results)} open port entries (may include non-web ports)")
    return sorted(results, key=lambda x: x['port'])