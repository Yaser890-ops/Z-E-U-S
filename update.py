import os
import re
import requests

# پوشه یا فایل خروجی در ساختار پنل (مثلاً پوشه proxies)
output_dir = "proxies"
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

manual_file = "manual_configs.txt"
sources_file = "sources.txt"
configs = []

# ۱. خواندن کانفیگ‌های دستی و VIP
if os.path.exists(manual_file):
    with open(manual_file, "r", encoding="utf-8") as f:
        for line in f.read().splitlines():
            if line.strip() and not line.startswith("#"):
                configs.append(line.strip())

# ۲. خواندن منابع از sources.txt
if os.path.exists(sources_file):
    with open(sources_file, "r", encoding="utf-8") as f:
        for url in f.read().splitlines():
            url = url.strip()
            if not url or url.startswith("#"):
                continue
            try:
                res = requests.get(url, timeout=15)
                if res.status_code == 200:
                    found = re.findall(r'((?:vless|vmess|trojan|ss)://[^\s<>"]+)', res.text)
                    for conf in found:
                        configs.append(conf.strip())
            except Exception as e:
                print(f"Error: {e}")

# ۳. حذف موارد تکراری برای خروجی تمیز
unique_configs = list(dict.fromkeys(configs))

# ۴. ذخیره خروجی نهایی
output_file = os.path.join(output_dir, "vip.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

print(f"Updated! Total active configs: {len(unique_configs)}")
