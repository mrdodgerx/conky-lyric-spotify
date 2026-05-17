#!/usr/bin/env python3
import json, os, subprocess, urllib.request, urllib.parse, re, hashlib, textwrap

MAX_CHARS = 40

CACHE_DIR = os.path.expanduser("~/.cache/spotify_lyrics")
os.makedirs(CACHE_DIR, exist_ok=True)

def pctl(args):
    try:
        return subprocess.check_output(["playerctl", "-p", "spotify"] + args, stderr=subprocess.DEVNULL).decode().strip()
    except:
        return None

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "conky/1.0"})
    with urllib.request.urlopen(req, timeout=8) as r:
        return r.read().decode()

def search_lyrics(artist, title):
    cache_key = hashlib.md5(f"{artist}|{title}".encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, cache_key + ".json")
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)
    q = urllib.parse.quote
    for query in [f"{artist} {title}", title]:
        url = f"https://lrclib.net/api/search?q={q(query)}"
        try:
            data = json.loads(fetch(url))
            if data:
                for d in data:
                    if not (d.get("syncedLyrics") or d.get("plainLyrics")):
                        continue
                    ra = d.get("artistName", "").lower().replace(" ", "")
                    sa = artist.lower().replace(" ", "")
                    if sa in ra or ra in sa:
                        with open(cache_file, "w") as f:
                            json.dump(d, f)
                        return d
        except:
            pass
    return None

def parse_lrc(text):
    lines = []
    for line in text.strip().split("\n"):
        m = re.match(r'\[(\d+):(\d+\.\d+)\]\s*(.*)', line)
        if m:
            ts = int(m.group(1)) * 60 + float(m.group(2))
            t = m.group(3).strip()
            if t:
                lines.append((ts, t))
    return lines

def get_current(lines, pos):
    best = 0
    for i in range(len(lines)):
        if lines[i][0] <= pos:
            best = i
    return best

def main():
    track_id = pctl(["metadata", "mpris:trackid"])
    if not track_id:
        print("${color2}No track playing${color}")
        return
    artist = pctl(["metadata", "xesam:artist"]) or ""
    title = pctl(["metadata", "xesam:title"]) or ""
    pos = float(pctl(["position"]) or 0)
    length = int(pctl(["metadata", "mpris:length"]) or 0) // 1000000
    if not artist or not title:
        print("${color2}Waiting for track info...${color}")
        return
    data = search_lyrics(artist, title)
    print(f"${{color0}}{textwrap.fill(title, MAX_CHARS)}${{color}}")
    print(f"${{color2}}{textwrap.fill(artist, MAX_CHARS)}${{color}}")
    if length > 0:
        prog = int((pos / length) * 40)
        bar = "${color0}" + "─" * prog + "${color2}" + "─" * (40 - prog) + "${color}"
        print(bar)
    else:
        print("")
    if not data:
        print("${color2}No lyrics found${color}")
        return
    synced = data.get("syncedLyrics")
    if synced:
        lines = parse_lrc(synced)
    else:
        plain = data.get("plainLyrics", "")
        plain_lines = [l for l in plain.strip().split("\n") if l.strip()]
        interval = length / len(plain_lines) if length > 0 and plain_lines else 5
        lines = [(i * interval, l) for i, l in enumerate(plain_lines)]
    if not lines:
        print("${color2}No lyrics available${color}")
        return
    current = get_current(lines, pos)
    start = max(0, current - 1)
    end = min(len(lines), current + 4)
    for i in range(start, end):
        _, text = lines[i]
        if i == current:
            wrapped = textwrap.fill(text, MAX_CHARS - 4).split("\n")
            for j, line in enumerate(wrapped):
                pfx = "  \u276f " if j == 0 else "     "
                print(f"${{color3}}{pfx}{line}${{color}}")
        elif i < current:
            wrapped = textwrap.fill(text, MAX_CHARS - 4).split("\n")
            for line in wrapped:
                print(f"${{color2}}    {line}${{color}}")
        else:
            wrapped = textwrap.fill(text, MAX_CHARS - 4).split("\n")
            for line in wrapped:
                print(f"${{color1}}    {line}${{color}}")

if __name__ == "__main__":
    main()
