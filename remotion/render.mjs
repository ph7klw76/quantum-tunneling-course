import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';

const here=path.dirname(fileURLToPath(import.meta.url)),root=path.dirname(here),out=path.join(root,'outputs');
const mode=process.argv[2]||'sample';
if(mode==='full') {
 const eligibility=JSON.parse(await fs.readFile(path.join(here,'production-eligibility.json'),'utf8'));
 if(eligibility.eligible!==true) throw new Error('Confirm Remotion Free License eligibility or an existing appropriate license before production rendering. Evaluation samples/stills remain available; no subscription is purchased by this tool.');
}
const events=JSON.parse(await fs.readFile(path.join(root,'course/publication_events.json'),'utf8'));
await fs.mkdir(out,{recursive:true});
const media=path.join(here,'public/media');
await fs.access(path.join(media,'baseline.mp4'));await fs.access(path.join(media,'narration.wav'));
const browserExecutable=process.env.REMOTION_BROWSER_EXECUTABLE || (process.platform==='win32'?path.join(os.homedir(),'AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe'):null);
const concurrency=Number(process.env.REMOTION_CONCURRENCY||4);
console.log(JSON.stringify({mode,cpus:os.cpus().length,memoryGB:Math.round(os.totalmem()/1024**3),concurrency,durationFrames:events.duration_frames}));
const serveUrl=await bundle({entryPoint:path.join(here,'src/index.ts'),publicDir:path.join(here,'public'),outDir:path.join(here,'.bundle',mode),onProgress:p=>{if(p===100)console.log('Composition bundle ready');}});
const browser=await openBrowser('chrome',{browserExecutable,logLevel:'warn'});
try {
 const id=mode==='baseline'?'QuantumBaseline':'QuantumPolished';
 const inputProps={edition:mode==='baseline'?'baseline':'polished',showCaptions:false};
 const composition=await selectComposition({serveUrl,id,inputProps,puppeteerInstance:browser});
 const common={serveUrl,composition,inputProps,puppeteerInstance:browser,codec:'h264',crf:18,x264Preset:'veryfast',pixelFormat:'yuv420p',colorSpace:'bt709',imageFormat:'jpeg',jpegQuality:95,concurrency,logLevel:'warn',timeoutInMilliseconds:90000};
 const progress=label=>{let previous=0;return p=>{const now=Date.now();if(now-previous>10000||p.progress===1){previous=now;console.log(JSON.stringify({label,progress:Number(p.progress.toFixed(4)),renderedFrames:p.renderedFrames,encodedFrames:p.encodedFrames}));}};};
 if(mode==='stills') {
  const frames=[0,120,1500,5400,6100,8100,8650,11100,14430,18120,20700];
  for(const frame of frames){await renderStill({serveUrl,composition,inputProps,puppeteerInstance:browser,frame,output:path.join(out,`remotion-frame-${frame}.png`),imageFormat:'png',logLevel:'warn'});}
  await renderStill({serveUrl,composition,inputProps:{edition:'baseline',showCaptions:false},puppeteerInstance:browser,frame:120,output:path.join(out,'remotion-baseline-frame.png'),imageFormat:'png',logLevel:'warn'});
  await renderStill({serveUrl,composition,inputProps:{edition:'polished',showCaptions:true},puppeteerInstance:browser,frame:5400,output:path.join(out,'remotion-caption-proof.png'),imageFormat:'png',logLevel:'warn'});
  const thumbnail=await selectComposition({serveUrl,id:'QuantumThumbnail',puppeteerInstance:browser});
  await renderStill({serveUrl,composition:thumbnail,puppeteerInstance:browser,frame:0,output:path.join(out,'Quantum_Tunneling_Remotion_Thumbnail.png'),imageFormat:'png',logLevel:'warn'});
  console.log('Rendered visual proof frames');
 } else if(mode==='full') {
  // Cache video-only chapter renders; mux the original continuous WAV exactly once.
  const codeFiles=await fs.readdir(path.join(here,'src'),{recursive:true});
  const hash=crypto.createHash('sha256');
  for(const file of codeFiles.sort()){if(/\.(tsx?|json|css)$/.test(file))hash.update(await fs.readFile(path.join(here,'src',file)));}
  hash.update(await fs.readFile(path.join(root,'outputs/remotion-media-provenance.json')));
  hash.update(await fs.readFile(path.join(here,'pnpm-lock.yaml')));
  hash.update(await fs.readFile(fileURLToPath(import.meta.url)));
  const key=hash.digest('hex').slice(0,16),cache=path.join(out,'remotion-cache');await fs.mkdir(cache,{recursive:true});
  const chapters=[];
  for(let i=0;i<events.chapters.length;i++) {
   const from=events.chapters[i].start_frame,to=(events.chapters[i+1]?.start_frame??events.duration_frames)-1;
   const outputLocation=path.join(cache,`chapter-${i+1}-${key}.mp4`);
   if(!(await fs.stat(outputLocation).catch(()=>null))) {
    console.log(`Rendering chapter ${i+1}: frames ${from}–${to}`);
    await renderMedia({...common,outputLocation:outputLocation+'.partial.mp4',frameRange:[from,to],muted:true,onProgress:progress(`chapter-${i+1}`)});
    await fs.rename(outputLocation+'.partial.mp4',outputLocation);
   } else console.log(`Reusing completed render cache for chapter ${i+1}`);
   chapters.push({from,to,file:outputLocation});
   await fs.writeFile(path.join(out,'remotion-render-checkpoint.json'),JSON.stringify({key,chapters},null,2));
  }
  const concat=path.join(cache,'concat.txt');await fs.writeFile(concat,chapters.map(c=>`file '${c.file.replaceAll('\\','/').replaceAll("'","'\\''")}'`).join('\n'));
  const final=path.join(out,'Quantum_Tunneling_Lecture_Remotion.mp4');
  const ffmpeg=process.env.FFMPEG_BINARY || spawnSync(process.env.PYTHON||'python',['-c','import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],{encoding:'utf8'}).stdout.trim();
  const result=spawnSync(ffmpeg,['-hide_banner','-loglevel','warning','-y','-f','concat','-safe','0','-i',concat,'-i',path.join(media,'narration.wav'),'-i',path.join(root,'narration/lecture.srt'),'-f','ffmetadata','-i',path.join(out,'chapters.ffmetadata'),'-map','0:v:0','-map','1:a:0','-map','2:0','-map_metadata','3','-map_chapters','3','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata','title=Quantum Tunneling — Polished Applied Quantum Lab','-movflags','+faststart','-t',String(events.duration_seconds),final],{stdio:'inherit'});
  if(result.status!==0)throw new Error('Final video mux failed');
  console.log('FINAL RENDER: '+final);
 } else {
  const outputLocation=path.join(out,mode==='baseline'?'Quantum_Tunneling_Baseline_Sample.mp4':'Quantum_Tunneling_Remotion_Sample.mp4');
  const videoOnly=outputLocation+'.video.mp4';
  await renderMedia({...common,outputLocation:videoOnly,frameRange:[0,Math.min(1800,events.duration_frames)-1],muted:true,onProgress:progress(mode)});
  const ffmpeg=process.env.FFMPEG_BINARY || spawnSync(process.env.PYTHON||'python',['-c','import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],{encoding:'utf8'}).stdout.trim();
  const mux=spawnSync(ffmpeg,['-hide_banner','-loglevel','warning','-y','-i',videoOnly,'-i',path.join(media,'narration.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','60','-movflags','+faststart',outputLocation],{stdio:'inherit'});
  if(mux.status!==0)throw new Error('Sample audio mux failed');
  await fs.unlink(videoOnly);
  console.log('SAMPLE RENDER: '+outputLocation);
 }
} finally {await browser.close({silent:true});}
