"""Mapa de metro del protocolo, en SVG. Se ve igual en claro y oscuro: todo letrero lleva fondo propio."""
def chip_w(t, fs=13.5): return int(len(t) * fs * 0.56 + 34)

def metro_svg(c):
    L1, L2, ST, RING = "#" + c["l1"], "#" + c["l2"], "#FFFFFF", "#8B949E"
    W, H, y1, y2 = 1000, 300, 100, 190
    s1 = [("🔍", "Understand", 190, "st", 0), ("📐", "Architect", 330, "x", 0),
          ("🚀", "Ship", 830, "x", 0), ("🌱", "Evolve", 935, "st", 0)]
    s2 = [("⚙️", "Implement", 440, "st", 0), ("🚧", "Verify", 545, "closed", 1),
          ("🔧", "Fix", 640, "st", 0), ("✅", "Verify", 735, "st", 1)]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">']
    o.append(f'<path d="M150 {y1} H960" stroke="{L1}" stroke-width="12" stroke-linecap="round" fill="none"/>')
    o.append(f'<path d="M960 {y1} H995" stroke="{L1}" stroke-width="12" stroke-dasharray="1 10" stroke-linecap="round"/>')
    o.append(f'<path d="M330 {y1} C330 {y2} 330 {y2} 385 {y2} H775 C830 {y2} 830 {y2} 830 {y1}" stroke="{L2}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    for y, col, n, name in ((y1, L1, "L1", "Business"), (y2, L2, "L2", "Engineering")):
        w = chip_w(name.upper(), 10.5) - 10
        o.append(f'<circle cx="62" cy="{y}" r="21" fill="{col}" stroke="{ST}" stroke-width="3"/><text x="62" y="{y+5}" text-anchor="middle" font-size="14" font-weight="800" fill="{ST}">{n}</text>')
        o.append(f'<rect x="{62-w/2}" y="{y+28}" width="{w}" height="18" rx="9" fill="{col}"/><text x="62" y="{y+41}" text-anchor="middle" font-size="10" font-weight="700" letter-spacing=".8" fill="{ST}">{name.upper()}</text>')
    def chip(x, y, icon, name, col):
        t = f"{icon} {name}"; w = chip_w(t)
        o.append(f'<rect x="{x-w/2}" y="{y-15}" width="{w}" height="29" rx="14.5" fill="{col}"/>')
        o.append(f'<text x="{x}" y="{y+4.5}" text-anchor="middle" font-size="13.5" font-weight="600" fill="{ST}">{t}</text>')
    for icon, name, x, k, row in s1:
        o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y1-46}" stroke="{L1}" stroke-width="2.5"/>')
        chip(x, y1 - 50, icon, name, L1)
    for icon, name, x, k, row in s2:
        yc = y2 + 50 + row * 40
        o.append(f'<line x1="{x}" y1="{y2}" x2="{x}" y2="{yc}" stroke="{L2}" stroke-width="2.5"/>')
        chip(x, yc, icon, name, L2)
    def station(x, y, kind, col):
        if kind == "x":
            o.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{ST}" stroke="{RING}" stroke-width="4"/><circle cx="{x}" cy="{y}" r="6" fill="{col}"/>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{ST}" stroke="{col}" stroke-width="5"/>')
            if kind == "closed":
                o.append(f'<path d="M{x-4} {y-4} L{x+4} {y+4} M{x+4} {y-4} L{x-4} {y+4}" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>')
    for _, _, x, k, _ in s1: station(x, y1, k, L1)
    for _, _, x, k, _ in s2: station(x, y2, k, L2)
    return "\n".join(o + ["</svg>"])
