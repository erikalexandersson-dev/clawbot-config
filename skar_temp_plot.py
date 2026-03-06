import json, math, urllib.request, datetime

STATION='SKAR'
# Same dates as above + today (UTC date aligns with local window since we use fixed Z times)
DAYS=[
  '2026-01-31','2026-02-01','2026-02-02','2026-02-03','2026-02-04','2026-02-05','2026-02-06','2026-02-07'
]
UTC_OFFSET_HOURS=-5  # America/Bogota
LOCAL_START=6
LOCAL_END=12
Z_START=LOCAL_START-UTC_OFFSET_HOURS  # 11
Z_END=LOCAL_END-UTC_OFFSET_HOURS      # 17
MAX_HOURS=24*10

url=f"https://aviationweather.gov/api/data/metar?ids={STATION}&format=json&hours={MAX_HOURS}"
with urllib.request.urlopen(url, timeout=30) as r:
    data=json.loads(r.read().decode('utf-8'))

# Collect points per day within Z window
points={d:[] for d in DAYS}
for o in data:
    rt=datetime.datetime.fromisoformat(o['reportTime'].replace('Z','+00:00'))
    day=rt.date().isoformat()
    if day not in points:
        continue
    if not (Z_START <= rt.hour <= Z_END):
        continue
    temp=o.get('temp')
    if temp is None:
        continue
    # convert to local time
    local=rt + datetime.timedelta(hours=UTC_OFFSET_HOURS)
    x=local.hour + local.minute/60.0
    if x < LOCAL_START-0.01 or x > LOCAL_END+0.01:
        continue
    points[day].append((x, float(temp), rt.strftime('%H%MZ')))

for d in DAYS:
    points[d].sort(key=lambda t: t[0])

# write CSV for inspection
csv_path='/root/.openclaw/workspace/skar_temp_6-12.csv'
with open(csv_path,'w',encoding='utf-8') as f:
    f.write('date,local_time,temp_c,report_z\n')
    for d in DAYS:
        for x,t,z in points[d]:
            hh=int(x)
            mm=int(round((x-hh)*60))
            f.write(f"{d},{hh:02d}:{mm:02d},{t:.1f},{z}\n")

# Determine y range
all_t=[t for d in DAYS for _,t,_ in points[d]]
if all_t:
    y_min=math.floor(min(all_t)-1)
    y_max=math.ceil(max(all_t)+1)
else:
    y_min,y_max=0,1

# SVG layout
W,H=1200,700
M_L,M_R,M_T,M_B=80,40,40,80
plot_w=W-M_L-M_R
plot_h=H-M_T-M_B


def x_to_px(x):
    return M_L + (x-LOCAL_START)/(LOCAL_END-LOCAL_START)*plot_w

def y_to_px(y):
    return M_T + (y_max-y)/(y_max-y_min)*plot_h

# Flyable map from JP Clawbot summary (forwarded by Erik)
# True = flyable, False = not flyable/cancelled
flyable={
    '2026-01-31': True,
    '2026-02-01': True,
    '2026-02-02': False,
    '2026-02-03': True,
    '2026-02-04': True,
    '2026-02-05': True,
    '2026-02-06': False,
    # 2026-02-07 not decided yet; leave unset for neutral color
}

def color_for(day):
    if day in flyable:
        return '#16a34a' if flyable[day] else '#dc2626'
    return '#334155'

svg=[]
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')
svg.append(f'<text x="{M_L}" y="28" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" font-size="18" fill="#0f172a">SKAR temperatur 06–12 lokal tid (Bogotá) — varje dag en linje</text>')
svg.append(f'<text x="{M_L}" y="50" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" font-size="12" fill="#475569">Färger: grön=flygbar, röd=ej flygbar (saknas tills vi får listan). Källa: aviationweather.gov METAR</text>')

# Axes
svg.append(f'<rect x="{M_L}" y="{M_T}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#cbd5e1"/>')

# X ticks each hour
for h in range(LOCAL_START, LOCAL_END+1):
    x=x_to_px(h)
    svg.append(f'<line x1="{x}" y1="{M_T+plot_h}" x2="{x}" y2="{M_T+plot_h+6}" stroke="#94a3b8"/>')
    svg.append(f'<text x="{x}" y="{M_T+plot_h+24}" text-anchor="middle" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#334155">{h:02d}</text>')

svg.append(f'<text x="{M_L+plot_w/2}" y="{H-20}" text-anchor="middle" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#334155">Klockslag (lokal tid)</text>')

# Y ticks
step=1 if (y_max-y_min)<=12 else 2
for y in range(int(y_min), int(y_max)+1, step):
    py=y_to_px(y)
    svg.append(f'<line x1="{M_L-6}" y1="{py}" x2="{M_L}" y2="{py}" stroke="#94a3b8"/>')
    svg.append(f'<text x="{M_L-10}" y="{py+4}" text-anchor="end" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#334155">{y}</text>')
    svg.append(f'<line x1="{M_L}" y1="{py}" x2="{M_L+plot_w}" y2="{py}" stroke="#e2e8f0"/>')

svg.append(f'<text x="22" y="{M_T+plot_h/2}" transform="rotate(-90 22 {M_T+plot_h/2})" text-anchor="middle" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#334155">Temperatur (°C)</text>')

# Lines per day
legend_x=M_L+plot_w+10
legend_y=M_T+10
svg.append(f'<text x="{legend_x}" y="{legend_y}" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#0f172a">Dagar</text>')

for idx,day in enumerate(DAYS):
    pts=points.get(day, [])
    if len(pts)<2:
        # still show legend
        cy=legend_y+18+idx*16
        svg.append(f'<line x1="{legend_x}" y1="{cy-4}" x2="{legend_x+18}" y2="{cy-4}" stroke="{color_for(day)}" stroke-width="3"/>')
        svg.append(f'<text x="{legend_x+24}" y="{cy}" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#334155">{day} (få/inga punkter)</text>')
        continue

    d_attr=' '.join([f"L {x_to_px(x):.1f} {y_to_px(t):.1f}" if i else f"M {x_to_px(x):.1f} {y_to_px(t):.1f}" for i,(x,t,_) in enumerate(pts)])
    svg.append(f'<path d="{d_attr}" fill="none" stroke="{color_for(day)}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.9"/>')

    # legend line
    cy=legend_y+18+idx*16
    svg.append(f'<line x1="{legend_x}" y1="{cy-4}" x2="{legend_x+18}" y2="{cy-4}" stroke="{color_for(day)}" stroke-width="3"/>')
    svg.append(f'<text x="{legend_x+24}" y="{cy}" font-size="12" font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial" fill="#334155">{day}</text>')

svg.append('</svg>')

svg_path='/root/.openclaw/workspace/skar_temp_6-12.svg'
with open(svg_path,'w',encoding='utf-8') as f:
    f.write('\n'.join(svg))

print(svg_path)
print(csv_path)
for d in DAYS:
    print(d, len(points.get(d,[])))
