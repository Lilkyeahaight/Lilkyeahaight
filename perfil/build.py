#!/usr/bin/env python3
"""Arma README.md + metro.svg del perfil a partir de perfil.toml.

Tres estilos con la MISMA información (agent, terminal, postal) y tres temas de color.
Cada semana rota la combinación: 9 semanas sin repetir.

  python3 perfil/build.py                         # combinación de esta semana
  python3 perfil/build.py --layout terminal --tema cafe
"""
import argparse, datetime, json, pathlib, sys, tomllib
from urllib.parse import quote

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from metro import metro_svg  # noqa: E402

LAYOUTS = ["agent", "terminal", "postal"]


def load():
    data = tomllib.loads((HERE / "perfil.toml").read_text())
    temas = json.loads((HERE / "temas.json").read_text())
    return data, temas


def pick(week, temas):
    names = list(temas)
    return LAYOUTS[week % len(LAYOUTS)], names[(week // len(LAYOUTS)) % len(names)]


def q(s):
    return quote(s, safe="")


# ---------- piezas comunes ----------

def typing(lines, c, width=600, size=16):
    l = ";".join(q(x).replace("%20", "+") for x in lines)
    return (f'<p align="center">\n  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500'
            f'&size={size}&duration=2800&pause=1400&color={c["hot"]}&center=true&vCenter=true&width={width}&lines={l}" />\n</p>')


def flat_badges(d, c):
    a = d["agent"]
    items = [("model", a["model"]), ("status", a["status"]),
             ("role", f'CTO @ {a["organization"]}'), ("location", a["location"])]
    imgs = "\n".join(
        f'  <img src="https://img.shields.io/badge/{q(k)}-{q(v.replace("-", "--"))}-{c["mid"]}?style=flat-square&labelColor={c["deep"]}" />'
        for k, v in items)
    return f'<p align="center">\n{imgs}\n</p>'


def stack(d, c):
    imgs = "\n".join(
        f'  <img src="https://img.shields.io/badge/{q(n)}-{c["mid"]}?style=for-the-badge&logo={logo}&logoColor={c["accent"]}" />'
        for n, logo in d["stack"]["badges"])
    return f'<p align="center">\n{imgs}\n</p>'


def metro(alt_flow):
    return ('<sub>🚇 <b>agents/protocol.svg</b> · line map</sub>\n\n<p align="center">\n'
            f'  <img src="metro.svg" width="100%" alt="Protocol line map: {alt_flow}" />\n</p>')


def footer(d, c):
    return f'<p align="center"><code>{d["system_prompt"]["tagline"]}</code></p>\n\n{stack(d, c)}'


# ---------- el agent.md en crudo ----------

def agent_md(d):
    a, rt = d["agent"], d["runtime"]
    desc = "\n".join("  " + x for x in a["description"])
    out = [
        "---", f'name: {a["name"]}', f'model: {a["model"]}', f'role: {a["role"]}',
        f'organization: {a["organization"]}', "description: >", desc,
        f'tools: [{", ".join(a["tools"])}]', f'location: {a["location"]}', f'status: {a["status"]}', "---", "",
        "## Mission", "", *d["mission"]["lines"], "", d["mission"]["punchline"], "",
        "## Core capabilities", "", *[f"- {x}" for x in d["capabilities"]["items"]], "",
        "## Execution protocol", "", f'`{d["protocol"]["flow"]}`', "", *d["protocol"]["lines"], "",
        "## ERP mindset", "", *d["erp"]["lines"], "", *[f"- {x}" for x in d["erp"]["rules"]], "",
        "## Engineering doctrine", "", "```yaml", *[f"{k}: {v}" for k, v in d["doctrine"].items()], "```", "",
        "## Anti-friction", "", *d["anti_friction"]["lines"], "",
        "## Artificial intelligence", "", *d["ai"]["lines"], "",
        "## Boundaries", "", *[f"- {x}" for x in d["boundaries"]["items"]], "",
        "## Runtime", "", "```bash", "$ whoami", *[f"> {x}" for x in rt["whoami"]], "",
        "$ cat now.txt", *[f"> {x}" for x in rt["now"]], "", "$ uptime", f'> {rt["uptime"]}', "```", "",
        "## System prompt", "", *d["system_prompt"]["lines"], "", "---", "", f'`{d["system_prompt"]["tagline"]}`',
    ]
    return "\n".join(out)


# ---------- estilo 1: agent ----------

def layout_agent(d, c):
    a = d["agent"]
    body = agent_md(d)
    lines, kb = body.count("\n") + 1, len(body.encode()) / 1024
    banner = (f'<p align="center">\n  <img width="100%" src="https://capsule-render.vercel.app/api?type=rect&height=110'
              f'&color=0:{c["bg"]},100:{c["deep"]}&text={q(a["name"] + ".md")}&fontSize=40&fontColor={c["accent"]}'
              f'&fontAlign=50&fontAlignY=44&desc={q("agents/")}&descSize=15&descAlign=50&descAlignY=74" />\n</p>')
    t = typing([f'> loading agents/{a["name"]}.md ...', f'> role: {a["role"]} @ {a["organization"]}',
                *[f"> {x}" for x in d["system_prompt"]["tagline"].split(". ") if x]], c)
    return "\n\n".join([
        banner, flat_badges(d, c), t,
        f'<sub>📄 <b>agents/{a["name"]}.md</b> · {lines} lines · {kb:.1f} KB</sub>',
        f"````markdown\n{body}\n````", metro(d["protocol"]["flow"]),
        f'<div align="center">\n\n{stack(d, c)}\n\n</div>',
    ])


# ---------- estilo 2: terminal ----------

def layout_terminal(d, c):
    a, rt = d["agent"], d["runtime"]
    banner = (f'<p align="center">\n  <img width="100%" src="https://capsule-render.vercel.app/api?type=rect&height=90'
              f'&color=0:{c["deep"]},100:{c["bg"]}&text={q("~ $ " + a["name"].lower())}&fontSize=34'
              f'&fontColor={c["accent"]}&fontAlign=30&fontAlignY=55" />\n</p>')
    sh = [
        "$ whoami", f'{a["display_name"]} · {a["name"]}', *[f"> {x}" for x in rt["whoami"]], "",
        "$ cat mission.txt", *d["mission"]["lines"], d["mission"]["punchline"], "",
        "$ ls capabilities/", *[f"→ {x}" for x in d["capabilities"]["items"]], "",
        "$ cat protocol.txt", d["protocol"]["flow"], *d["protocol"]["lines"], "",
        "$ cat erp-mindset.md", *d["erp"]["lines"], *[f"  · {x}" for x in d["erp"]["rules"]], "",
        "$ cat doctrine.yml", *[f"{k}: {v}" for k, v in d["doctrine"].items()], "",
        "$ grep missing anti-friction.log", *d["anti_friction"]["lines"], "",
        "$ cat ai.txt", *d["ai"]["lines"], "",
        "$ cat boundaries.txt", *d["boundaries"]["items"], "",
        "$ cat now.txt", *[f"> {x}" for x in rt["now"]], "",
        "$ uptime", rt["uptime"], "",
        "$ cat system-prompt.txt", *d["system_prompt"]["lines"],
    ]
    t = typing([f'{a["role"]} @ {a["organization"]}', d["mission"]["punchline"], d["system_prompt"]["tagline"]], c)
    return "\n\n".join([banner, t, flat_badges(d, c), "```console\n" + "\n".join(sh) + "\n```",
                        metro(d["protocol"]["flow"]), footer(d, c)])


# ---------- estilo 3: postal ----------

def layout_postal(d, c):
    a, rt = d["agent"], d["runtime"]
    banner = (f'<p align="center">\n  <img width="100%" src="https://capsule-render.vercel.app/api?type=soft&height=220'
              f'&color=0:{c["deep"]},100:{c["mid"]}&text={q(a["display_name"])}&fontSize=54&fontColor={c["ink"]}'
              f'&fontAlignY=42&desc={q(a["role"] + " @ " + a["organization"] + " · " + a["location"])}'
              f'&descSize=18&descAlignY=64&descAlign=50&animation=fadeIn" />\n</p>')
    mission = (f'<h3 align="center">{"<br>".join(d["mission"]["lines"])}</h3>\n\n'
               f'<p align="center"><i>{d["mission"]["punchline"]}</i></p>')
    caps = "<br>".join(f"▸ {x}" for x in d["capabilities"]["items"])
    bounds = "<br>".join(f"✕ {x[3:] if x.startswith('No ') else x}" for x in d["boundaries"]["items"])
    two = (f'<table>\n<tr><th>🏗️ What I do</th><th>🚫 What I don\'t</th></tr>\n'
           f'<tr><td valign="top">{caps}</td><td valign="top">{bounds}</td></tr>\n</table>')
    doctrine = "| | |\n|---|---|\n" + "\n".join(f"| `{k}` | {v} |" for k, v in d["doctrine"].items())
    now = " · ".join(rt["now"])
    parts = [
        banner, mission, flat_badges(d, c),
        f'### 🧭 Protocol\n\n`{d["protocol"]["flow"]}`\n\n' + " ".join(d["protocol"]["lines"]),
        two,
        "### 🧩 ERP mindset\n\n> " + "<br>".join(d["erp"]["lines"]) + "\n\n" + "\n".join(f"- {x}" for x in d["erp"]["rules"]),
        "### 📐 Doctrine\n\n" + doctrine,
        "### 🔧 Anti-friction\n\n" + "\n".join(f"- {x}" for x in d["anti_friction"]["lines"]),
        "### 🤖 AI\n\n" + " ".join(d["ai"]["lines"]),
        metro(d["protocol"]["flow"]),
        f'<p align="center"><sub>{" · ".join(rt["whoami"])}<br><b>now:</b> {now}<br><b>uptime:</b> {rt["uptime"]}</sub></p>',
        "<p align=\"center\">" + "<br>".join(d["system_prompt"]["lines"]) + "</p>",
        footer(d, c),
    ]
    return "\n\n".join(parts)


RENDER = {"agent": layout_agent, "terminal": layout_terminal, "postal": layout_postal}


def build(layout, tema, d=None, temas=None):
    if d is None:
        d, temas = load()
    c = temas[tema]
    stamp = f"<!-- generado por perfil/build.py · estilo: {layout} · tema: {tema} · no edites a mano -->\n"
    return stamp + RENDER[layout](d, c) + "\n", metro_svg(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=LAYOUTS)
    ap.add_argument("--tema")
    ap.add_argument("--week", type=int, default=datetime.date.today().isocalendar().week)
    ap.add_argument("--out", default=str(ROOT))
    a = ap.parse_args()
    d, temas = load()
    layout, tema = pick(a.week, temas)
    layout, tema = a.layout or layout, a.tema or tema
    if tema not in temas:
        sys.exit(f"tema desconocido: {tema} (hay: {', '.join(temas)})")
    md, svg = build(layout, tema, d, temas)
    out = pathlib.Path(a.out)
    (out / "README.md").write_text(md)
    (out / "metro.svg").write_text(svg)
    print(f"README.md + metro.svg · estilo {layout} · tema {tema}")


if __name__ == "__main__":
    main()
