"""The page CSS (the colours come from config.THEME)."""
from .config import THEME


CSS = ":root{" + ";".join(f"--{k.replace('_', '-')}:{v}" for k, v in THEME.items()) + "}" + """
*{box-sizing:border-box}
body{margin:0;display:flex;min-height:100vh;background:var(--bg);color:var(--text);
     font-family:"Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;font-size:15px}
nav{width:230px;flex-shrink:0;background:var(--sidebar);display:flex;flex-direction:column;
    position:sticky;top:0;height:100vh}
nav .head{padding:26px 18px 14px;text-align:center}
nav .logo{width:150px;height:150px;object-fit:cover;border-radius:14px;border:2px solid var(--brand);display:block;margin:0 auto 14px}
nav .brand{color:var(--brand);font-weight:700;font-size:1.15rem;letter-spacing:.5px}
nav a{color:#fff;text-decoration:none;padding:14px 24px;font-size:1.05rem;display:block}
nav a:hover{background:var(--hover)}
nav a.active{background:var(--active);font-weight:600}
nav .spacer{flex:1}
nav form{margin:0}
nav button{width:100%;text-align:left;background:none;border:0;color:#c9b8ad;padding:16px 24px;
           font:inherit;cursor:pointer}
nav button:hover{background:var(--hover);color:#fff}
main{flex:1;padding:26px 34px;min-width:0;max-width:1060px}
h1{margin:0;font-size:1.9rem}
.sub{color:var(--muted);margin:4px 0 20px}
h2{margin:0 0 12px;font-size:1.1rem}
.card{background:var(--card);border-radius:10px;padding:18px 20px;margin-bottom:16px;
      box-shadow:0 1px 3px rgba(0,0,0,.09)}
label{display:flex;flex-direction:column;gap:4px;font-size:.85rem;color:var(--muted)}
input,select{font:inherit;padding:8px 10px;border:1px solid #d9cdc3;border-radius:6px;
             background:#fff;color:var(--text)}
input:focus,select:focus{outline:2px solid var(--accent);border-color:var(--accent)}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end}
.score input{width:80px}
.dash{padding-bottom:9px;font-size:1.2rem;color:var(--muted)}
.btn{font:inherit;font-weight:600;background:var(--accent);color:#fff;border:0;border-radius:6px;
     padding:9px 18px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:var(--accent-h)}
.btn.danger{background:var(--danger);padding:5px 12px;font-size:.85rem}
.btn.danger:hover{background:var(--danger-h)}
.hint{color:var(--muted);font-size:.85rem;margin:10px 0 0}
.flash{padding:11px 16px;border-radius:8px;margin-bottom:16px;font-weight:600}
.flash.ok{background:#dcfce7;color:#166534}
.flash.err{background:#fee2e2;color:#991b1b}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chip{padding:6px 14px;border-radius:999px;background:#eadfd6;color:var(--text);
      text-decoration:none;font-size:.9rem}
.chip:hover{background:#ddcdbf}
.chip.on{background:var(--accent);color:#fff;font-weight:600}
table{width:100%;border-collapse:collapse}
th{background:var(--sidebar);color:#fff;text-align:left;padding:10px 12px;font-weight:600}
td{padding:9px 12px;border-bottom:1px solid #efe6de}
tbody tr:nth-child(even){background:var(--alt)}
td.c,th.c{text-align:center}
tr.gold,tr.gold:nth-child(even){background:var(--gold);font-weight:700}
tr.silver,tr.silver:nth-child(even){background:var(--silver);font-weight:700}
tr.bronze,tr.bronze:nth-child(even){background:var(--bronze);font-weight:700}
.pos{color:var(--good);font-weight:600}.neg{color:var(--danger);font-weight:600}
.empty{color:var(--muted);padding:6px 0}
.wrap{overflow-x:auto}
mark.egg{background:#ffeb3b;color:#000;padding:0 4px;border-radius:3px}
.btn.alt{background:#6b7280;padding:5px 12px;font-size:.85rem}
.btn.alt:hover{background:#4b5563}
.badge{background:#e5e7eb;color:#4b5563;border-radius:999px;padding:2px 10px;font-size:.75rem;font-weight:600;vertical-align:middle}
.actions{display:flex;gap:8px;justify-content:center}
.trophy{width:20px;height:auto;padding 0; border radius 0;}
form.inline{margin:0}
@media (max-width:760px){
  body{flex-direction:column}
  nav{width:100%;height:auto;position:static;flex-direction:row;flex-wrap:wrap}
  nav .head{width:100%;display:flex;align-items:center;gap:12px;padding:10px 16px;text-align:left}
  nav .logo{width:44px;height:44px;margin:0;border-radius:8px}
  nav a,nav button{padding:10px 14px}nav .spacer{display:none}
  main{padding:18px}
  th,td{padding:8px 5px}
}
"""
