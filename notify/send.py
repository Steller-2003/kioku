"""Gửi 1 từ vựng lên kênh ntfy (chạy bởi GitHub Actions theo lịch)."""
import json, os, urllib.request
D = os.path.dirname(os.path.abspath(__file__))
words = json.load(open(os.path.join(D, "words.json"), encoding="utf-8"))
st = json.load(open(os.path.join(D, "state.json")))
w = words[st["i"] % len(words)]
kind = "Kanji" if w["k"] else "Từ vựng"
title = w["t"] + ("  ·  " + w["r"] if w["r"] and w["r"] != w["t"] else "")
msg = (w["hv"] + " — " if w["hv"] else "") + w["vn"] + f"\nN{w['lv']} · {kind} · từ {st['i'] % len(words) + 1}/{len(words)}"
body = json.dumps({"topic": os.environ.get("NTFY_TOPIC", "kioku-thang-db247664"), "title": title, "message": msg,
                   "tags": ["jp"], "click": os.environ.get("APP_URL", "")}).encode()
req = urllib.request.Request("https://ntfy.sh/", data=body, headers={"Content-Type": "application/json"})
print(urllib.request.urlopen(req, timeout=30).status, title)
st["i"] += 1
json.dump(st, open(os.path.join(D, "state.json"), "w"))
