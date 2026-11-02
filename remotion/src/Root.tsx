import React from 'react';
import {Composition} from 'remotion';
import {QuantumLecture} from './QuantumLecture';
import events from './generated/events.json';
import {Thumbnail} from './Thumbnail';
export const Root:React.FC=()=> <>
 <Composition id="QuantumPolished" component={QuantumLecture} width={1920} height={1080} fps={30} durationInFrames={events.duration_frames} defaultProps={{edition:'polished' as const,showCaptions:false}}/>
 <Composition id="QuantumBaseline" component={QuantumLecture} width={1920} height={1080} fps={30} durationInFrames={events.duration_frames} defaultProps={{edition:'baseline' as const,showCaptions:false}}/>
 <Composition id="QuantumThumbnail" component={Thumbnail} width={1280} height={720} fps={30} durationInFrames={1}/>
</>;
