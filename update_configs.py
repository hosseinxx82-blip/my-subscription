import base64
import json
import urllib.request

SOURCE_URL = "https://nova-sunny-vault-702b.hossein-xx82.workers.dev/sub?sub=hossein-salamt&key=cb8aa2437a3c"
NEW_NAME_PREFIX = "freedom"

def b64decode(s):
    s = s.strip()
    pad = len(s) % 4
    if pad:
        s += "=" * (4 - pad)
    return base64.urlsafe_b64decode(s.encode()).decode(errors="ignore")

def fetch_source():
    with urllib.request.urlopen(SOURCE_URL) as resp:
        raw = resp.read().decode()
    try:
        decoded = b64decode(raw)
        if "://" in decoded:
            return decoded
    except Exception:
        pass
    return raw

def rename_vmess(link, idx):
    b64part = link[len("vmess://"):]
    try:
        data = json.loads(b64decode(b64part))
    except Exception:
        return link
    data["ps"] = f"{NEW_NAME_PREFIX}-{idx}"
    new_b64 = base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode()
    return "vmess://" + new_b64

def rename_generic(link, idx):
    base = link.split("#")[0]
    return f"{base}#{NEW_NAME_PREFIX}-{idx}"

def process(content):
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    out = []
    idx = 1
    for line in lines:
        if line.startswith("vmess://"):
            out.append(rename_vmess(line, idx))
        elif line.startswith(("vless://", "trojan://", "ss://", "ssr://", "hysteria://", "hy2://")):
            out.append(rename_generic(line, idx))
        else:
            out.append(line)
        idx += 1
    return "\n".join(out)

def main():
    content = fetch_source()
    new_content = process(content)
    encoded = base64.b64encode(new_content.encode()).decode()
    with open("sub.txt", "w") as f:
        f.write(encoded)

if __name__ == "__main__":
    main()
