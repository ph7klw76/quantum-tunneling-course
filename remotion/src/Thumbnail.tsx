import React from 'react';
import {AbsoluteFill} from 'remotion';
import {palette,font} from './theme';
import events from './generated/events.json';
export const Thumbnail:React.FC=()=>{
 const xx=(x:number)=>30+(x+.8)/2.15*520,yy=(y:number)=>245-y*67;
 const curve=(density:boolean)=>events.physics.wave_samples.map((p,i)=>`${i?'L':'M'}${xx(p.x).toFixed(2)},${yy(density?p.density:p.real).toFixed(2)}`).join(' ');
 return <AbsoluteFill style={{background:palette.bg,color:palette.ink,fontFamily:font,padding:55}}>
  <div style={{color:palette.teal,fontSize:23,letterSpacing:4}}>APPLIED QUANTUM LAB</div>
  <div style={{position:'absolute',left:55,top:155,fontSize:105,fontWeight:700,lineHeight:.99,letterSpacing:-4}}>THROUGH<br/>THE <span style={{color:palette.amber}}>BARRIER</span></div>
  <div style={{position:'absolute',left:60,top:404,fontSize:35,lineHeight:1.2,maxWidth:570}}>Can an electron pass<br/>through a wall?</div>
  <div style={{position:'absolute',right:64,top:70,color:palette.teal,fontSize:57,fontWeight:600}}>T ≈ {(events.physics.T*100).toFixed(2)}%</div>
  <svg style={{position:'absolute',right:32,top:208,width:570,height:380}} viewBox="0 0 580 380"><rect x={xx(0)} y="70" width={xx(.45)-xx(0)} height="245" fill={palette.amber} opacity=".15"/><path d="M25 245H558" stroke={palette.muted} strokeWidth="1.5"/><path d={curve(false)} fill="none" stroke={palette.teal} strokeWidth="4"/><path d={curve(true)} fill="none" stroke={palette.amber} strokeWidth="4"/><g fill={palette.muted} fontSize="22" fontFamily={font}><text x={xx(0)-5} y="345">0</text><text x={xx(.45)-12} y="345">a</text><text x="30" y="42">Re(ψ)  /  |ψ|²</text><text x="435" y="345">x (nm)</text></g></svg>
  <div style={{position:'absolute',left:60,right:60,bottom:55,borderTop:`1px solid ${palette.line}`,paddingTop:23,color:palette.muted,fontSize:23,letterSpacing:1}}>FINITE BARRIER · PREDICT, CALCULATE, TEST · PROBABILITY, NOT A TRAJECTORY</div>
 </AbsoluteFill>;
};
