"""Read first 256 KB of a deposited Thermo .raw over HTTPS; print instrument model/method strings."""
import json, re, sys, urllib.request
API = "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/"
for acc in sys.argv[1:]:
    files = json.load(urllib.request.urlopen(API + acc + "/files/all", timeout=60))
    raws = [f for f in files if f["fileName"].lower().endswith(".raw")]
    if not raws:
        print(acc, "no .raw"); continue
    f = sorted(raws, key=lambda f: f["fileName"])[0]
    ftp = [l["value"] for l in f["publicFileLocations"] if l["value"].startswith("ftp://")][0]
    url = ftp.replace("ftp://", "https://")
    req = urllib.request.Request(url, headers={"Range": "bytes=0-262143"})
    try:
        data = urllib.request.urlopen(req, timeout=90).read()
    except Exception as e:
        print(acc, "fetch failed", e); continue
    txt = data.decode("utf-16-le", errors="ignore")
    hits = sorted(set(re.findall(r"(Q Exactive[\w \-]*|Orbitrap[\w \-]*|LTQ[\w \-]*|Exploris[\w \-]*|TMT[\w\-]*|SILAC[\w\-]*)", txt)))
    print(acc, f["fileName"], "|", [h.strip()[:60] for h in hits][:8])
