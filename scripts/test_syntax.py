import urllib.request
import base64

test_cases = [
    ('text with quotes', 'flowchart TD\n A["Mulai: Inisialisasi"] --> B["Selesai"]'),
    ('text with lte', 'flowchart TD\n A["Uji: VRAM <= 7.5 GB"] --> B["Selesai"]'),
    ('text with br', 'flowchart TD\n A["Baris 1<br/>Baris 2"] --> B["Selesai"]'),
    ('classDef', 'flowchart TD\n classDef gpu fill:#DCFCE7,stroke:#16A34A\n A["GPU"]:::gpu --> B["Selesai"]'),
]

for name, code in test_cases:
    b64 = base64.urlsafe_b64encode(code.encode('utf-8')).decode('ascii')
    url = f'https://mermaid.ink/img/{b64}?bgColor=!white'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print(f'{name}: SUCCESS ({len(resp.read())} bytes)')
    except Exception as e:
        print(f'{name}: FAILED ({e})')
