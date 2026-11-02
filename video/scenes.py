"""28 native Manim CE animated teaching panels; composed by build.py.

Each seamless 4-second segment cycles stationary-state phase or a parameter
sweep. The composer repeats it during narration, preserving exact physics.
No LaTeX installation is needed: equations use Matplotlib's mathtext renderer.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from manim import *
from course.lesson import SEGMENTS,CHAPTERS
from course.physics import wavefunction,transmission,amplitudes,C

config.background_color = '#091522'
CYAN = '#63E4DB'; GOLD = '#F6C978'; GRAY = '#B6C8D6'

def label(text,size=27,color=WHITE,width=None):
    obj=Text(text,font='Sans',font_size=size,color=color)
    if width and obj.width>width: obj.scale_to_fit_width(width)
    return obj

def construct_panel(self,idx):
    s=SEGMENTS[idx]; kind=s['kind']; phase=ValueTracker(0)
    top=label(f"{idx//4+1:02d} / {CHAPTERS[idx//4].upper()}",19,CYAN).to_edge(UP,buff=.25).to_edge(LEFT,buff=.5)
    title=label(s['title'],38,width=13.2).move_to([0,2.94,0])
    focus=label(s['focus'],25,GRAY,width=13.1).move_to([0,2.28,0])
    footer=label('APPLIED QUANTUM LAB   /   FINITE, STATIC, LOSSLESS BARRIER',18,GRAY).to_edge(DOWN,buff=.23)
    self.add(top,title,focus,footer)
    if kind=='predict':
        panel=RoundedRectangle(width=11.5,height=3.6,corner_radius=.22,color=CYAN,fill_color='#102B3B',fill_opacity=1).move_to([0,-.25,0])
        self.add(panel,label('PAUSE & PREDICT',43,GOLD).move_to([0,.7,0]),
                 label('Commit to an answer.',31).move_to([0,-.1,0]),
                 label('Give a reason before continuing.',29,GRAY).move_to([0,-.8,0]))
        ring=Circle(radius=.16,color=CYAN).move_to([0,-1.5,0])
        self.add(ring); self.play(ring.animate.scale(1.5),rate_func=there_and_back,run_time=4)
        return
    if kind=='transmission':
        # Keep the exact expression visible while its result is narrated.
        equation=ImageMobject(str(Path(__file__).resolve().parents[1]/'outputs/equations/exact.png')).scale_to_fit_width(11.5).move_to([0,.95,0])
        r,A,B,t=amplitudes()
        self.add(equation,label('E = 0.50 eV     V0 = 1.00 eV     a = 0.45 nm',27,GRAY,width=12).move_to([0,-.35,0]),
                 label(f'T = {abs(t)**2:.6f}',39,CYAN).move_to([-3.1,-1.35,0]),
                 label(f'R = {abs(r)**2:.6f}',39,GOLD).move_to([3.1,-1.35,0]),
                 label('Equal leads: T = |t|²     R = |r|²',28,WHITE,width=12).move_to([0,-2.25,0]),
                 label('Transmission and reflection are probability-current ratios.',22,GRAY,width=12).move_to([0,-2.95,0]))
        self.wait(4);return
    if kind in ('sweep','energy_sweep','height','transmission'):
        is_energy=kind=='energy_sweep'; is_height=kind=='height'
        xmin,xmax=(.03,.97) if is_energy else ((.56,2.0) if is_height else (0,1.2))
        ax=Axes(x_range=[xmin,xmax,(xmax-xmin)/4],y_range=[0,1,.25],x_length=8.4,y_length=3.8,
                tips=False,axis_config={'color':GRAY,'include_numbers':False}).move_to([-1.65,-.25,0])
        f=lambda x:transmission(E=x) if is_energy else (transmission(V0=x) if is_height else transmission(a=x))
        self.add(ax,ax.plot(f,x_range=[xmin,xmax,(xmax-xmin)/180],color=CYAN),
                 label('T',28,GOLD).next_to(ax,UP,buff=.15).align_to(ax,LEFT),
                 label('E (eV)' if is_energy else ('V0 (eV)' if is_height else 'Barrier width a (nm)'),25,GRAY).next_to(ax,DOWN,buff=.35))
        for val in [0,.5,1]: self.add(label(str(val),20,GRAY).next_to(ax.c2p(xmin,val),LEFT,buff=.12))
        for val in np.linspace(xmin,xmax,4): self.add(label(f'{val:.2f}',19,GRAY).next_to(ax.c2p(val,0),DOWN,buff=.1))
        def xv():return xmin+(xmax-xmin)*(.5-.5*np.cos(phase.get_value()))
        dot=always_redraw(lambda:Dot(ax.c2p(xv(),f(xv())),color=GOLD,radius=.075))
        self.add(dot)
        self.add(label('EXACT MODEL',24,CYAN).move_to([4.9,1.,0]),
                 label('0 < E < V0',27).move_to([4.9,.3,0]),
                 label('a = 0.45 nm' if is_energy or is_height else 'E = 0.50 eV',24,GRAY).move_to([4.9,-.35,0]),
                 label('V0 = 1.00 eV' if not is_height else 'E = 0.50 eV',24,GRAY).move_to([4.9,-.95,0]),
                 label('T + R = 1',28,GOLD).move_to([4.9,-1.7,0]))
    elif kind in ('stm','device','evidence'):
        if kind=='stm':
            surface=VMobject(color=CYAN).set_points_smoothly([[-5,-1.2+.13*np.cos(x*5),0] for x in []]) if False else None
            atoms=VGroup(*[Circle(radius=.28,color=CYAN,fill_opacity=.4).move_to([x,-1.3,0]) for x in np.arange(-5,1,.6)])
            tip=Polygon([-2,1.4,0],[-.9,1.4,0],[-1.45,.15,0],color=GOLD,fill_opacity=.5)
            tip.add_updater(lambda m: m.move_to([-2+1.6*np.sin(phase.get_value()),.85+.12*np.cos(phase.get_value()*2),0]))
            gap=DoubleArrow([-4.7,-.9,0],[-4.7,.1,0],color=GRAY,buff=0)
            self.add(atoms,tip,gap,label('vacuum gap',24,GRAY).move_to([-4,0,0]),label('sample',24).move_to([-2,-2,0]))
            texts=['Bias selects an energy window.','Feedback holds current steady.','Electronic states affect contrast.']
        elif kind=='device':
            for x,w,col,txt in [(-4,2.4,CYAN,'electrode'),(-2,1.2,GOLD,'barrier'),(0,2.4,CYAN,'electrode')]:
                self.add(Rectangle(width=w,height=2.5,color=col,fill_opacity=.2).move_to([x,-.2,0]),label(txt,23,col).move_to([x,-1.9,0]))
            texts=['Band structure and effective mass','Defects, fields and disorder','Elastic versus inelastic transport']
        else:
            ax=Axes(x_range=[0,1,.25],y_range=[0,1,.25],x_length=6.4,y_length=3.2,tips=False).move_to([-2.7,-.3,0])
            self.add(ax,ax.plot(lambda x:.9*np.exp(-3*x),color=CYAN),label('thickness',24,GRAY).next_to(ax,DOWN),label('relative current',23,GOLD).next_to(ax,UP))
            dots=VGroup(*[Dot(ax.c2p(x,.9*np.exp(-3*x)*(1+.06*np.sin(x*40))),radius=.06,color=GOLD) for x in np.linspace(.05,.95,9)])
            self.add(dots);texts=['A trend can support a model.','Compare competing predictions.','Report uncertainty and controls.']
        for i,txt in enumerate(texts):self.add(label(txt,25,WHITE,width=5.0).move_to([3.9,1-i*1.1,0]))
        self.play(phase.animate.set_value(TAU),run_time=4,rate_func=linear);return
    elif kind=='energy':
        ax=Axes(x_range=[-.9,1.35,.5],y_range=[0,1.3,.5],x_length=8.2,y_length=3.7,tips=False).move_to([-1.7,-.2,0])
        self.add(ax,VMobject(color=GOLD,stroke_width=5).set_points_as_corners([ax.c2p(-.9,0),ax.c2p(0,0),ax.c2p(0,1),ax.c2p(.45,1),ax.c2p(.45,0),ax.c2p(1.35,0)]),
                 DashedLine(ax.c2p(-.9,.5),ax.c2p(1.35,.5),color=CYAN),
                 label('Energy (eV)',24,GRAY).next_to(ax,UP),label('x (nm)',24,GRAY).next_to(ax,DOWN))
        for y in [0,.5,1]:self.add(label(str(y),20,GRAY).next_to(ax.c2p(-.9,y),LEFT))
        self.add(label('V0 = 1.00 eV',26,GOLD).move_to([4.8,.9,0]),label('E = 0.50 eV',26,CYAN).move_to([4.8,.1,0]),label('a = 0.45 nm',26,GRAY).move_to([4.8,-.7,0]),label('Energy is conserved.',24,WHITE,width=4).move_to([4.8,-1.5,0]))
        self.wait(4);return
    elif kind=='equation':
        img=ImageMobject(str(Path(__file__).resolve().parents[1]/'outputs/equations/schrodinger.png')).scale_to_fit_width(11)
        img.move_to([0,.65,0]);self.add(img)
        img2=ImageMobject(str(Path(__file__).resolve().parents[1]/'outputs/equations/exact.png')).scale_to_fit_width(11)
        img2.move_to([0,-1.15,0]);self.add(img2)
        self.wait(4);return
    else:
        ax=Axes(x_range=[-.9,1.35,.5],y_range=[-1.8,4,1],x_length=8.1,y_length=4.25,tips=False,
                axis_config={'color':GRAY}).move_to([-1.7,-.35,0])
        self.add(ax,label('x (nm)',24,GRAY).next_to(ax,DOWN,buff=.25))
        for x in [0,.45,1.]:self.add(label(f'{x:g}',20,GRAY).next_to(ax.c2p(x,0),DOWN,buff=.12))
        def width(): return .45 if kind!='width' else .25+.4*(.5-.5*np.cos(phase.get_value()))
        barrier=always_redraw(lambda:Polygon(ax.c2p(0,0),ax.c2p(0,3.2),ax.c2p(width(),3.2),ax.c2p(width(),0),
                                            color=GOLD,fill_opacity=.13,stroke_width=2))
        self.add(barrier)
        x=np.linspace(-.9,1.35,300)
        def curve(density=False):
            p,_=wavefunction(x,a=width())
            y=abs(p)**2 if density else (p*np.exp(-1j*phase.get_value())).real
            return VMobject(color=GOLD if density else CYAN,stroke_width=3).set_points_as_corners([ax.c2p(float(xx),float(yy)) for xx,yy in zip(x,y)])
        self.add(always_redraw(lambda:curve(False)),always_redraw(lambda:curve(True)))
        if kind=='energy':
            # Energy reference is separate from the dimensionless wave ordinate.
            self.add(label('E = 0.50 eV < V0 = 1.00 eV',23,GOLD,width=7.4).move_to([-1.7,1.55,0]))
        panel=['Re(psi)', '|psi|²', 'Barrier: 0 to a', 'Relative amplitude', 'No particle path']
        for i,txt in enumerate(panel):self.add(label(txt,27,CYAN if i==0 else (GOLD if i==1 else GRAY),width=4).move_to([4.8,1.15-i*.65,0]))
    self.play(phase.animate.set_value(TAU),run_time=4,rate_func=linear)

for idx in range(len(SEGMENTS)):
    globals()[f'Segment{idx:02d}']=type(f'Segment{idx:02d}',(Scene,),{'__module__':__name__,'construct':lambda self,i=idx:construct_panel(self,i)})
