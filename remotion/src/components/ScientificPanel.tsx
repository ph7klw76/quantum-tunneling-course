import React from 'react';
import {interpolate,useCurrentFrame} from 'remotion';
import {Equation} from './Equation';
import {palette} from '../theme';
import data from '../generated/events.json';

const note:React.CSSProperties={fontSize:33,lineHeight:1.4,color:palette.muted,textAlign:'center'};
export const ScientificPanel:React.FC<{index:number}>=({index})=>{
 const frame=useCurrentFrame();
 const beat=(key:string,fallback:number)=>(data.highlight_beats.find(b=>b.scene===index&&b.key===key)?.frame??(data.scenes[index].start_frame+fallback))-data.scenes[index].start_frame;
 const reveal=(at:number)=>interpolate(frame,[at,at+18],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 if(index===8)return <div style={{padding:'32px 50px',height:'100%',background:palette.panel}}>
  <div style={{color:palette.teal,fontSize:27,letterSpacing:3}}>ONE EQUATION / ONE FIXED TOTAL ENERGY</div>
  <Equation tex={String.raw`-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2}+V(x)\psi=E\psi`} size={67}/>
  <div style={{display:'flex',gap:26,justifyContent:'center',marginTop:35}}>{[['Kinetic curvature','The spatial shape of ψ','curvature'],['Potential energy','A finite barrier V(x)','potential'],['Total energy','The same E throughout','total']].map(([title,body,key],i)=><div key={title} style={{opacity:reveal(beat(key,45+i*35)),width:480,padding:28,border:`1px solid ${palette.line}`,borderRadius:14}}><div style={{color:palette.amber,fontSize:34}}>{title}</div><div style={{fontSize:29,color:palette.muted,marginTop:12}}>{body}</div></div>)}</div>
  <Equation tex={String.raw`\kappa=\frac{\sqrt{2m(V_0-E)}}{\hbar}\quad [\mathrm{length}^{-1}]`} delay={beat('kappa',600)} size={48}/>
  <div style={{...note,opacity:reveal(beat('outside',420))}}>Oscillatory solutions outside; evanescent solutions inside.</div>
 </div>;
 if(index===11)return <div style={{padding:'35px 45px',height:'100%',background:palette.panel}}>
  <div style={{color:palette.teal,fontSize:27,letterSpacing:3}}>FINITE RECTANGULAR BARRIER / EXACT RESULT</div>
  <Equation tex={String.raw`T=\left[1+\frac{V_0^2\sinh^2(\kappa a)}{4E(V_0-E)}\right]^{-1}`} size={59}/>
  <div style={note}>E = 0.50 eV · V₀ = 1.00 eV · a = 0.45 nm · constant free-electron mass</div>
  <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1.6fr',gap:24,marginTop:30}}>
   {[['TRANSMISSION / T',data.physics.T,palette.teal],['REFLECTION / R',data.physics.R,palette.amber]].map(([label,value,color])=><div key={String(label)} style={{opacity:reveal(beat('result',60)),textAlign:'center',padding:'23px 12px',border:`1px solid ${palette.line}`,borderRadius:14}}><div style={{fontSize:23,color:palette.muted,letterSpacing:2}}>{label}</div><div style={{fontSize:69,color:String(color),fontVariantNumeric:'tabular-nums',fontWeight:600}}>{Number(value).toFixed(6)}</div></div>)}
   <div style={{textAlign:'left',padding:'5px 10px',fontSize:29,lineHeight:1.3}}><div style={{color:palette.teal,opacity:reveal(beat('conservation',540))}}>T + R = 1 · Equal leads: T = |t|²</div><div style={{color:palette.ink,marginTop:17,opacity:reveal(beat('ensemble',155))}}>About 1,424 of 10,000 electrons, with fluctuations.<br/><span style={{color:palette.muted}}>Probability is not energy lost.</span></div></div>
  </div>
 </div>;
 return null;
};
