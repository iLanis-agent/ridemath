import json, math

def pos(x): return isinstance(x,(int,float)) and math.isfinite(x) and x>0
def jround(x): return math.floor(x+0.5)
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def r1(x): return jround(x*10)/10

TERRAIN={"flat":1,"rolling":0.85,"hilly":0.65}
WH_PER_MI={"eco":8,"tour":12,"sport":18,"turbo":25}

def range_plan(sticker,lb,terrain):
    if not pos(sticker): return {"error":"the sticker miles must be above zero"}
    if not pos(lb): return {"error":"the rider weight must be above zero"}
    if terrain not in TERRAIN: return {"error":"pick a terrain"}
    w=max(0.7,1-max(0,lb-170)*0.004)
    return {"miles":r1(sticker*w*TERRAIN[terrain])}

def render_range(r,sticker,lb,terrain):
    return ("Your "+jsnum(sticker)+"-mile sticker with a "+jsnum(lb)+" lb rider on "+terrain
            +" roads figures about "+jsnum(r["miles"])
            +" miles - the sticker rider weighed 150 and the wind was at his back.")

def watt_plan(wh,assist):
    if not pos(wh): return {"error":"the battery watt-hours must be above zero"}
    if assist not in WH_PER_MI: return {"error":"pick an assist level"}
    return {"miles":r1(wh/WH_PER_MI[assist]),"rate":WH_PER_MI[assist]}

def render_watt(r,wh,assist):
    return ("Your "+jsnum(wh)+" Wh battery in "+assist+" figures about "+jsnum(r["miles"])
            +" miles at "+jsnum(r["rate"])+" Wh a mile - the eco number on the box belongs to a different ride.")

def charge_plan(wh,w):
    if not pos(wh): return {"error":"the battery watt-hours must be above zero"}
    if not pos(w): return {"error":"the charger watts must be above zero"}
    return {"hours":r1(wh/w*1.15)}

def render_charge(r,wh,w):
    return ("Your "+jsnum(wh)+" Wh battery on the "+jsnum(w)+" W charger figures about "+jsnum(r["hours"])
            +" hours empty to full - the last 15% is the slow part.")

cases=[]
def add(tool,args):
    if tool=="range": r=range_plan(*args); fn=render_range
    elif tool=="watt": r=watt_plan(*args); fn=render_watt
    else: r=charge_plan(*args); fn=render_charge
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(60,210,"rolling"),(60,150,"flat"),(45,190,"hilly"),(80,170,"flat"),(50,250,"rolling"),(70,180,"hilly"),(40,140,"flat"),(55,300,"rolling")]:
    add("range",a)
for a in [(500,"sport"),(500,"eco"),(625,"tour"),(400,"turbo"),(750,"tour"),(360,"sport"),(500,"turbo")]:
    add("watt",a)
for a in [(500,100),(500,200),(625,150),(400,100),(750,200),(360,90)]:
    add("charge",a)
add("range",[0,180,"flat"]); add("range",[60,180,"swamp"]); add("watt",[0,"eco"]); add("watt",[500,"ludicrous"]); add("charge",[500,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
