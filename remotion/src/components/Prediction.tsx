import React from 'react';
import {interpolate,useCurrentFrame} from 'remotion';
import {palette,font} from '../theme';
import type {Quiz,Scene} from '../types';

export const Prediction:React.FC<{quiz:Quiz;scene:Scene}> = ({quiz,scene})=>{
 const frame=useCurrentFrame(),global=frame+scene.start_frame;
 const holding=global>=quiz.hold_start_frame;
 const progress=interpolate(global,[quiz.hold_start_frame,quiz.hold_end_frame],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <div style={{position:'absolute',inset:0,padding:'35px 48px',background:palette.panel,fontFamily:font}}>
  <div style={{display:'flex',justifyContent:'space-between',fontSize:25,letterSpacing:3,color:palette.amber}}><span>{quiz.id} / PREDICT BEFORE THE ANSWER</span><span>{holding?'THINKING TIME':'FORM YOUR PREDICTION'}</span></div>
  <div style={{fontSize:48,lineHeight:1.16,fontWeight:600,maxWidth:1630,margin:'24px 0 26px',color:palette.ink}}>{quiz.question}</div>
  <div style={{display:'grid',gap:13}}>{quiz.options.map((option,i)=><div key={option} style={{display:'flex',gap:22,alignItems:'center',padding:'12px 20px',border:`1px solid ${palette.line}`,borderRadius:10,background:'#0B212D',color:palette.ink,fontSize:31,lineHeight:1.2}}><span style={{color:palette.teal,fontSize:25,flex:'0 0 34px'}}>{String.fromCharCode(65+i)}</span><span>{option}</span></div>)}</div>
  <div style={{position:'absolute',left:48,right:48,bottom:28,color:palette.muted,fontSize:27}}>Choose an answer. Give a reason. Revise after the explanation.<div style={{height:4,background:palette.line,marginTop:16}}><div style={{height:4,width:`${progress*100}%`,background:palette.amber}}/></div></div>
 </div>;
};
