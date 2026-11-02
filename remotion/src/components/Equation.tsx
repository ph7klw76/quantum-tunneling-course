import React from 'react';
import katex from 'katex';
import {useCurrentFrame,interpolate} from 'remotion';
import {palette} from '../theme';
import 'katex/dist/katex.min.css';
import './equation.css';

export const Equation:React.FC<{tex:string;delay?:number;size?:number}> = ({tex,delay=0,size=52})=>{
 const f=useCurrentFrame();const opacity=interpolate(f,[delay,delay+18],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <div style={{fontSize:size,color:palette.ink,opacity,transform:`translateY(${(1-opacity)*12}px)`}} dangerouslySetInnerHTML={{__html:katex.renderToString(tex,{throwOnError:true,displayMode:true,output:'html'})}}/>;
};
