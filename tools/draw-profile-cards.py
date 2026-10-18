# 24번 활동 프로필 카드: 인물 그림은 ElevenLabs Recraft v4.1 Flash(SODA 그림체), 글자는 Pillow
# 인물 원본: web/assets/img/k01/person-olena.webp, person-ahmet.webp
# 프로필 카드: 인물 그림(ElevenLabs Recraft) + 글자(Pillow)
from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
NAVY=(46,58,85); SLATE=(108,118,138); SAND=(222,205,176); IVORY=(251,248,241); OCHRE=(184,120,48)
F="/usr/share/fonts/opentype/inter/"
def f(w,s): return ImageFont.truetype(F+{"b":"Inter-Bold.otf","s":"Inter-SemiBold.otf","r":"Inter-Regular.otf"}[w], s)
def card(person, name, rows, out):
    W,H=1000,640
    im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
    d.rounded_rectangle((10,10,W-10,H-10),24,fill=IVORY,outline=SAND,width=3)
    d.rounded_rectangle((10,10,W-10,92),24,fill=NAVY); d.rectangle((10,60,W-10,92),fill=NAVY)
    d.text((48,51),"STECKBRIEF",font=f("b",30),fill=IVORY,anchor="lm")
    d.text((W-48,51),"Sprachschule Leipzig · Kurs A1",font=f("r",22),fill=SAND,anchor="rm")
    # 사진 칸
    px0,py0,pw,ph=44,124,300,476
    d.rounded_rectangle((px0,py0,px0+pw,py0+ph),16,fill="white",outline=SAND,width=2)
    p=person.copy(); p.thumbnail((pw-24,ph-24))
    im.paste(p,(px0+(pw-p.width)//2, py0+ph-12-p.height))
    x=392
    d.text((x,150),name,font=f("b",52),fill=NAVY)
    d.line((x,228,W-48,228),fill=SAND,width=3)
    y=262
    for k,v in rows:
        d.text((x,y),k,font=f("s",26),fill=SLATE)
        d.text((x+210,y),v,font=f("b",30),fill=NAVY)
        y+=78
    d.ellipse((W-80,H-80,W-56,H-56),fill=OCHRE)
    a=np.asarray(im).astype(np.int16); mask=a.sum(2)<750
    n=np.random.default_rng(5).normal(0,6,a.shape[:2]); a=a+(n[...,None]*mask[...,None])
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(out,quality=90)
