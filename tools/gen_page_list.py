# -*- coding: utf-8 -*-
"""从 index.html 导航结构生成在线页面清单（pages.html）与 Markdown 版（页面清单.md）。

用法：在仓库根目录执行  python3 tools/gen_page_list.py
输出：pages.html、页面清单.md（均为确定性输出，不含时间戳）
"""
import re
import html
import os

SITE_URL = "https://ifashion2016.github.io/water-prototype/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_nav():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    parts = re.split(r'<div class="module-title">', src)[1:]
    rows = []
    for p in parts:
        module = html.unescape(re.match(r"([^<]+)<", p).group(1)).strip()
        section = p[:p.find("<!--", 10) if "<!--" in p[10:] else len(p)]
        for href, name in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)<span', section):
            href = href.strip()
            if not href.endswith(".html") or href == "pages.html":
                continue
            rows.append((module, html.unescape(name).strip(), href))
    return rows


def render_html(rows):
    total = len(rows)
    body = []
    prev = None
    for module, name, href in rows:
        if module != prev:
            body.append(
                '<tr class="module-row"><td colspan="3">%s</td></tr>' % html.escape(module)
            )
            prev = module
        body.append(
            '<tr><td class="mod">%s</td><td class="name">%s</td>'
            '<td class="url"><a href="%s" target="_blank">%s%s</a></td></tr>'
            % (html.escape(module), html.escape(name), html.escape(href),
               SITE_URL, html.escape(href))
        )
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>页面清单 · 智慧水务高保真原型</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "PingFang SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, sans-serif;
    background: #f0f4f9; min-height: 100vh; padding: 32px 20px; color: #333;
  }}
  .wrap {{ max-width: 1000px; margin: 0 auto; }}
  .head {{
    background: linear-gradient(135deg, #0f4aa2 0%, #1686d9 100%);
    border-radius: 14px; padding: 26px 30px; color: #fff; margin-bottom: 20px;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;
  }}
  .head h1 {{ font-size: 22px; font-weight: 600; letter-spacing: 1px; }}
  .head p {{ font-size: 13px; opacity: .85; margin-top: 6px; }}
  .head a.home {{
    background: rgba(255,255,255,.18); color: #fff; text-decoration: none;
    padding: 9px 18px; border-radius: 22px; font-size: 13px; backdrop-filter: blur(8px);
  }}
  .head a.home:hover {{ background: rgba(255,255,255,.3); }}
  .search {{
    width: 100%; padding: 12px 18px 12px 42px; border: 1px solid #dbe3ee; border-radius: 10px;
    font-size: 14px; margin-bottom: 16px; outline: none; background: #fff url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23999" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>') no-repeat 14px center;
  }}
  .search:focus {{ border-color: #1686d9; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(15,60,120,.08); }}
  th {{
    background: #0f4aa2; color: #fff; font-size: 13px; font-weight: 600;
    padding: 12px 16px; text-align: left;
  }}
  td {{ padding: 10px 16px; font-size: 13px; border-top: 1px solid #eef2f8; vertical-align: middle; }}
  tr:hover td {{ background: #f5f9ff; }}
  tr.module-row td {{
    background: #eaf2fc; color: #0f4aa2; font-weight: 600; font-size: 13px;
    padding: 8px 16px; letter-spacing: 1px;
  }}
  td.mod {{ color: #888; white-space: nowrap; }}
  td.name {{ font-weight: 500; white-space: nowrap; }}
  td.url a {{ color: #0563c1; text-decoration: none; word-break: break-all; }}
  td.url a:hover {{ text-decoration: underline; }}
  .foot {{ text-align: center; color: #99a6b8; font-size: 12px; margin-top: 20px; line-height: 1.8; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="head">
    <div>
      <h1>📋 原型页面清单（{total} 页）</h1>
      <p>智慧水务高保真原型 · 与站点导航实时一致 · 每次发布自动生成</p>
    </div>
    <a class="home" href="./index.html">🏠 返回原型导航</a>
  </div>
  <input class="search" id="q" placeholder="搜索页面名称或路径…" oninput="filter()">
  <table id="tbl">
    <thead><tr><th style="width:130px">模块</th><th style="width:180px">页面名称</th><th>链接</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
  <div class="foot">
    本清单由发布流程自动生成；已下线页面不在清单中。<br>
    站点入口：{site}
  </div>
</div>
<script>
  function filter() {{
    var k = document.getElementById('q').value.toLowerCase();
    var trs = document.querySelectorAll('#tbl tbody tr');
    var show = {{}};
    for (var i = trs.length - 1; i >= 0; i--) {{
      var tr = trs[i];
      if (tr.className === 'module-row') {{
        tr.style.display = show[i] ? '' : 'none';
        continue;
      }}
      var hit = tr.textContent.toLowerCase().indexOf(k) >= 0;
      tr.style.display = hit ? '' : 'none';
      if (hit) {{
        for (var j = i - 1; j >= 0; j--) {{
          if (trs[j].className === 'module-row') {{ show[j] = true; break; }}
        }}
      }}
    }}
  }}
</script>
</body>
</html>
""".format(total=total, rows="\n".join(body), site=SITE_URL)


def render_md(rows):
    lines = [
        "# 智慧水务高保真原型 · 页面清单",
        "",
        "站点入口：%s" % SITE_URL,
        "",
        "> 本清单由发布流程自动生成，与站点导航保持一致；已下线页面不在清单中。",
        "",
    ]
    prev = None
    for module, name, href in rows:
        if module != prev:
            lines.append("## %s" % module)
            lines.append("")
            prev = module
        lines.append("- %s：%s%s" % (name, SITE_URL, href))
    lines.append("")
    return "\n".join(lines)


def main():
    rows = parse_nav()
    if not rows:
        raise SystemExit("未从 index.html 解析到任何页面链接")
    with open(os.path.join(ROOT, "pages.html"), "w", encoding="utf-8") as f:
        f.write(render_html(rows))
    with open(os.path.join(ROOT, "页面清单.md"), "w", encoding="utf-8") as f:
        f.write(render_md(rows))
    print("已生成 pages.html 与 页面清单.md，共 %d 页" % len(rows))


if __name__ == "__main__":
    main()
