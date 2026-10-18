# 1과 명함·이름표 그림 (글자가 들어가므로 Pillow로 직접 그림)
# 사용: python3 tools/draw-cards.py → cards/*.webp 를 web/assets/img/k01/ 로 복사
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os
NAVY=(46,58,85); SLATE=(108,118,138); SAND=(222,205,176); IVORY=(251,248,241); OCHRE=(184,120,48); RED=(196,64,58)
F="/usr/share/fonts/opentype/inter/"
def f(w,s): return ImageFont.truetype(F+{"b":"Inter-Bold.otf","s":"Inter-SemiBold.otf","r":"Inter-Regular.otf","l":"Inter-Light.otf","i":"Inter-Italic.otf"}[w], s)
W,H=900,600; CW,CH=760,470
def base():
    im=Image.new("RGB",(W,H),(255,255,255))
    sh=Image.new("L",(W,H),0); d=ImageDraw.Draw(sh)
    x0,y0=(W-CW)//2,(H-CH)//2
    d.rounded_rectangle((x0+10,y0+16,x0+CW+10,y0+CH+16),18,fill=70); sh=sh.filter(ImageFilter.GaussianBlur(14))
    im.paste((205,198,185),(0,0),sh)
    return im,x0,y0
def grain(im):
    a=np.asarray(im).astype(np.int16); mask=(a.sum(2)<750)
    n=np.random.default_rng(3).normal(0,7,a.shape[:2])
    a=a+(n[...,None]*mask[...,None]); return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def save(im,name):
    g=grain(im).crop((40,35,W-25,H-15)); g.save(f"cards/{name}.webp",quality=90); g.save(f"cards/{name}.png")

# 1) 선생님 명함
im,x,y=base(); d=ImageDraw.Draw(im)
d.rounded_rectangle((x,y,x+CW,y+CH),18,fill=NAVY)
d.rounded_rectangle((x+22,y,x+CW,y+CH),18,fill=IVORY); d.rectangle((x+22,y,x+48,y+CH),fill=IVORY)
d.rounded_rectangle((x+70,y+60,x+122,y+112),10,fill=OCHRE); d.text((x+96,y+86),"SL",font=f("b",24),fill=IVORY,anchor="mm")
d.text((x+140,y+66),"Sprachschule Leipzig",font=f("s",26),fill=NAVY); d.text((x+140,y+98),"Deutsch als Fremdsprache",font=f("r",18),fill=SLATE)
d.text((x+70,y+215),"Petra Wagner",font=f("b",56),fill=NAVY)
d.text((x+72,y+290),"Lehrerin · Deutsch",font=f("r",26),fill=SLATE)
d.line((x+70,y+350,x+CW-60,y+350),fill=SAND,width=3)
d.text((x+70,y+372),"Tel. 0341 / 12 15 19",font=f("r",22),fill=NAVY); d.text((x+70,y+404),"Raum 3 · Kurs A1",font=f("r",22),fill=NAVY)
save(im,"karte-wagner")

# 2) Jonas 명함 (학생)
im,x,y=base(); d=ImageDraw.Draw(im)
d.rounded_rectangle((x,y,x+CW,y+CH),18,fill=SAND)
d.rounded_rectangle((x+24,y+24,x+CW-24,y+CH-24),12,outline=NAVY,width=3)
d.text((x+CW//2,y+120),"JONAS BECKER",font=f("b",54),fill=NAVY,anchor="mm")
d.text((x+CW//2,y+178),"Student · Informatik",font=f("r",26),fill=NAVY,anchor="mm")
d.ellipse((x+CW//2-6,y+228,x+CW//2+6,y+240),fill=OCHRE)
d.text((x+CW//2,y+295),"Kochstraße 12 · 04275 Leipzig",font=f("r",22),fill=NAVY,anchor="mm")
d.text((x+CW//2,y+332),"Mobil 0170 / 12 8 15",font=f("r",22),fill=NAVY,anchor="mm")
d.text((x+CW//2,y+392),"„Das ist ein Fall für uns!“",font=f("i",20),fill=SLATE,anchor="mm")
save(im,"karte-becker")

# 3) 민준 이름표 (Hallo, ich bin …)
im,x,y=base(); d=ImageDraw.Draw(im)
d.rounded_rectangle((x,y,x+CW,y+CH),26,fill=RED)
d.text((x+CW//2,y+62),"HALLO",font=f("b",62),fill=IVORY,anchor="mm")
d.text((x+CW//2,y+118),"ich bin",font=f("r",30),fill=IVORY,anchor="mm")
d.rounded_rectangle((x+28,y+160,x+CW-28,y+CH-60),10,fill=IVORY)
d.text((x+CW//2,y+250),"Minjun Park",font=f("i",64),fill=NAVY,anchor="mm")
d.text((x+CW//2,y+330),"Südkorea · Kurs A1",font=f("r",24),fill=SLATE,anchor="mm")
d.text((x+CW//2,y+CH-30),"Sprachschule Leipzig",font=f("s",20),fill=IVORY,anchor="mm")
save(im,"karte-park")
