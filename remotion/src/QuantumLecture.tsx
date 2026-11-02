import React from 'react';
import {AbsoluteFill,Sequence,interpolate,useCurrentFrame,staticFile} from 'remotion';
import {Audio,Video} from '@remotion/media';
import events from './generated/events.json';
import {palette,font,phases,phaseFor} from './theme';
import {Prediction} from './components/Prediction';
import {ScientificPanel} from './components/ScientificPanel';
import type {LectureProps,Scene} from './types';

const ScenePresentation:React.FC<{scene:Scene}> = ({scene})=>{
 const f=useCurrentFrame(),enter=interpolate(f,[0,15],[0,1],{extrapolateRight:'clamp'});
 const quiz=events.quizzes.find(q=>q.scene===scene.index);
 const phase=phaseFor(scene.index,scene.kind);
 return <AbsoluteFill style={{fontFamily:font,color:palette.ink}}>
  <div style={{position:'absolute',left:70,right:70,top:37,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
   <div style={{letterSpacing:3,fontSize:24,color:palette.teal}}>ψ / APPLIED QUANTUM LAB</div>
   <div style={{display:'flex',gap:23,fontSize:20,letterSpacing:2}}>{phases.map((p,i)=><span key={p} style={{color:i===phase?palette.amber:palette.muted,borderBottom:i===phase?`3px solid ${palette.amber}`:'3px solid transparent',paddingBottom:8}}>{p}</span>)}</div>
  </div>
  <div style={{position:'absolute',left:70,right:70,top:103,opacity:enter,transform:`translateY(${(1-enter)*12}px)`}}>
   <div style={{fontSize:21,letterSpacing:3,color:palette.muted,marginBottom:11}}>CHAPTER {String(scene.chapter+1).padStart(2,'0')} / {events.chapters[scene.chapter].title.toUpperCase()}</div>
   <div style={{fontSize:53,fontWeight:600,lineHeight:1.1,letterSpacing:-1}}>{scene.title}</div>
   <div style={{fontSize:30,color:palette.muted,marginTop:10}}>{scene.focus}</div>
  </div>
  {(quiz || scene.index===8 || scene.index===11 || scene.index===27) && <div style={{position:'absolute',left:64,top:268,width:1792,height:674,borderRadius:17,overflow:'hidden',border:`1px solid ${palette.line}`}}>
   {quiz?<Prediction quiz={quiz} scene={scene}/>:scene.index===27?<div style={{height:'100%',background:palette.panel,padding:'46px 55px'}}>
    <div style={{color:palette.teal,fontSize:27,letterSpacing:3}}>YOUR NEXT EXPERIMENT</div><div style={{fontSize:65,lineHeight:1.12,fontWeight:600,marginTop:24}}>Predict. Compute. Test.<br/>Explain what would change your mind.</div>
    <div style={{display:'flex',gap:30,marginTop:42}}>{['Vary the barrier','Compare independent solvers','Critique the evidence'].map((x,i)=><div key={x} style={{flex:1,padding:25,border:`1px solid ${palette.line}`,borderRadius:12,fontSize:31,color:palette.muted}}><span style={{color:palette.amber}}>0{i+1} / </span>{x}</div>)}</div>
    <div style={{fontSize:30,color:palette.teal,marginTop:36}}>ph7klw76.github.io/quantum-tunneling-course/</div><div style={{fontSize:27,color:palette.muted,marginTop:15}}>Open the computational lab and the unfamiliar-interface investigation.</div>
   </div>:<ScientificPanel index={scene.index}/>}</div>}
  <div style={{position:'absolute',left:70,right:70,top:975,display:'flex',justifyContent:'space-between',alignItems:'center',borderTop:`1px solid ${palette.line}`,paddingTop:22,fontSize:26,color:palette.muted}}>
   <span>{scene.index===15?`EXACT WIDTH COMPARISON:  T(0.45 nm) = ${events.physics.T.toFixed(6)}  →  T(0.90 nm) = ${events.physics.T_doubled.toFixed(6)}`:scene.kind==='predict'?'PREDICTION FIRST / EXPLANATION NEXT':scene.index===19?'STATIC + ELASTIC: TOTAL ENERGY IS CONSERVED':scene.index>=24?'A FITTED MODEL NEEDS ASSUMPTIONS, CONTROLS AND UNCERTAINTY':scene.index>=20?'INTERPRETATION NEEDS BIAS, ELECTRONIC STATES AND CONTROLS':'STATIONARY 1D MODEL / IDENTICAL LEADS / NO PARTICLE TRAJECTORY'}</span>
   <span style={{color:palette.teal,fontSize:22}}>SCENE {String(scene.index+1).padStart(2,'0')} / 28</span>
  </div>
 </AbsoluteFill>;
};

export const QuantumLecture:React.FC<LectureProps>=({edition,showCaptions})=>{
 const frame=useCurrentFrame();
 const scene=events.scenes.find(s=>frame>=s.start_frame && frame<s.end_frame)||events.scenes[events.scenes.length-1];
 const hideManim=scene.kind==='predict'||[8,11,27].includes(scene.index);
 const cue=showCaptions?events.captions.find(c=>frame>=c.start_frame&&frame<c.end_frame):null;
 return <AbsoluteFill style={{background:palette.bg}}>
  {edition==='baseline'?<Video src={staticFile('media/baseline.mp4')} muted style={{width:1920,height:1080}}/>:<>
   {!hideManim&&<div style={{opacity:interpolate(frame-scene.start_frame,[0,10],[0,1],{extrapolateRight:'clamp'}),position:'absolute',left:64,top:268,width:1792,height:674,overflow:'hidden',borderRadius:17,border:`1px solid ${palette.line}`}}><Video src={staticFile('media/baseline.mp4')} muted objectFit="fill" style={{position:'absolute',width:1792,height:1008,top:-250,left:0}}/></div>}
   <Sequence from={scene.start_frame} durationInFrames={scene.duration_frames} name={scene.title}><ScenePresentation scene={scene}/></Sequence>
   <div style={{position:'absolute',bottom:0,left:0,height:5,width:`${frame/(events.duration_frames-1)*100}%`,background:palette.teal}}/>
  </>}
  <Audio src={staticFile('media/narration.wav')}/>
  {cue&&<div style={{position:'absolute',left:150,right:150,bottom:126,textAlign:'center',fontFamily:font,fontSize:35,lineHeight:1.25,color:'white',background:'#081821ee',padding:'16px 24px',borderRadius:10}}>{cue.text}</div>}
 </AbsoluteFill>;
};
