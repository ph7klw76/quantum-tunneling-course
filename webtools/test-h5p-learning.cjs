/* Real H5P/YouTube learning paths, using the active URL and the authoritative quiz times. */
const {chromium}=require('playwright');
const fs=require('node:fs/promises');
const path=require('node:path');
const {spawn}=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
async function main(){
 const out=path.join(root,'outputs/browser');await fs.mkdir(out,{recursive:true});
 const quizzes=JSON.parse(await fs.readFile(path.join(root,'quizzes/quizzes.json'),'utf8'));
 const python=process.env.PYTHON||(process.platform==='win32'?path.join(root,'.venv/Scripts/python.exe'):'python');
 const directory=process.env.H5P_QA_DIRECTORY||'outputs/pages';
 const phone=process.env.H5P_QA_PHONE==='true';
 const prefix=process.env.H5P_QA_DIRECTORY?'h5p-polished':'h5p-learning';
 const suffix=phone?'-phone':'';
 const server=process.env.H5P_QA_URL?null:spawn(python,['scripts/serve.py','--directory',directory,'--base-path','/quantum-tunneling-course/','--port','8768'],{cwd:root,stdio:'ignore',windowsHide:true});
 let browser,page;const report=[];const errors=[];const mediaInterruptions=[];let phase='startup';
 try{
  const url=process.env.H5P_QA_URL||'http://127.0.0.1:8768/quantum-tunneling-course/h5p/quantum-tunneling.html';
  for(let i=0;i<50;i++){try{if((await fetch(url)).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
  browser=await chromium.launch({headless:true});page=await browser.newPage({viewport:phone?{width:390,height:844}:{width:1280,height:900}});page.on('pageerror',e=>{
   // H5P's native MP4 review jump cancels an in-flight HTMLMediaElement.play().
   // Record this specific upstream rejection; every playback/seek/score check still runs.
   if(process.env.H5P_QA_DIRECTORY&&e.message==='The play() request was interrupted by a call to pause(). https://goo.gl/LdLk22')mediaInterruptions.push({name:e.name,message:e.message,phase});
   else errors.push(e.message);
  });
  await page.goto(url,{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.H5P?.instances[0]?.video?.getDuration?.()>600,{},{timeout:60000});
  await page.locator('.h5p-controls .h5p-pause').click();
  await page.waitForFunction(()=>H5P.instances[0].video.getCurrentTime()>0.3,{},{timeout:30000});
  const seekAndPlay=async seconds=>{
   await page.evaluate(()=>H5P.instances[0].pause());await page.waitForTimeout(200);
   await page.evaluate(t=>H5P.instances[0].seek(t),seconds);
   await page.waitForFunction(t=>Math.abs(H5P.instances[0].video.getCurrentTime()-t)<.25,seconds,{timeout:10000});
   // Native HTML5 seeking and H5P pause events settle before requesting play.
   await page.waitForTimeout(200);await page.evaluate(()=>H5P.instances[0].play());
  };
  for(let i=0;i<quizzes.length;i++){
   const q=quizzes[i];
   phase=q.id;
   await seekAndPlay(q.time_seconds-.65);
   const question=page.locator('.h5p-multichoice:visible').filter({hasText:q.question});
   const openQuestion=async()=>{if(phone){const launcher=page.locator('.h5p-interaction[role="button"]:visible').filter({hasText:q.id});await launcher.waitFor({state:'visible',timeout:20000});await launcher.click();}await question.waitFor({state:'visible',timeout:20000});};
   await openQuestion();
   const before=await page.evaluate(()=>H5P.instances[0].video.getCurrentTime());await page.waitForTimeout(700);
   const after=await page.evaluate(()=>H5P.instances[0].video.getCurrentTime());assert.ok(Math.abs(after-before)<.25);
   const wrong=(q.correct_index+1)%q.options.length;
   await question.locator('.h5p-alternative-container').nth(wrong).click();await question.locator('.h5p-question-check-answer').click();
   await page.waitForTimeout(300);
   assert.ok((await question.locator('.h5p-question-feedback').innerText()).includes(q.explanation));
   const review=question.locator('.h5p-question-iv-adaptivity-wrong');await review.waitFor({state:'visible',timeout:5000});
   await review.click();
   await page.waitForFunction(t=>Math.abs(H5P.instances[0].video.getCurrentTime()-t)<2,q.remediation_seconds,{timeout:10000});
   const reviewTime=await page.evaluate(()=>H5P.instances[0].video.getCurrentTime());
   await seekAndPlay(q.time_seconds-.65);
   await openQuestion();
   // Native IV adaptivity resets the question when taking its review jump.
   assert.equal(await question.locator('[aria-checked=true]').count(),0);
   await question.locator('.h5p-alternative-container').nth(q.correct_index).click();await question.locator('.h5p-question-check-answer').click();
   const score=await page.evaluate(index=>H5P.instances[0].interactions[index].getInstance().getScore(),i);assert.equal(score,1);
   assert.ok((await question.locator('.h5p-question-feedback').innerText()).includes(q.explanation));
   report.push({id:q.id,pauseTime:before,wrongAnswer:true,reviewTime,targetReview:q.remediation_seconds,retry:true,correctScore:score,feedback:true});
   await page.screenshot({path:path.join(out,`${prefix}-${q.id}${suffix}.png`),fullPage:true});
   await question.locator('.h5p-question-iv-continue').click();
   await page.waitForTimeout(300);
  }
  phase='summary';const mastery=JSON.parse(await fs.readFile(path.join(root,'h5p/authoring.json'),'utf8')).mastery;
  await seekAndPlay(await page.evaluate(()=>H5P.instances[0].video.getDuration()-2.5));
  await page.waitForFunction(()=>{const lesson=H5P.instances[0];return lesson.video.getCurrentTime()>lesson.video.getDuration()-3;},{},{timeout:15000});
  // The seekbar dot has the same summary class; click the actual in-video task.
  const summaryButton=page.locator('.h5p-interaction.h5p-end-summary:visible');await summaryButton.waitFor({state:'visible',timeout:15000});await summaryButton.click();
  for(const statements of mastery.statements)await page.getByRole('radio',{name:statements[0],exact:true}).click();
  const summary=await page.evaluate(()=>{const lesson=H5P.instances[0],task=lesson.interactions[lesson.interactions.length-1].getInstance();return{score:task.getScore(),maxScore:task.getMaxScore()};});
  assert.equal(summary.score,5);assert.equal(summary.maxScore,5);
  await page.screenshot({path:path.join(out,`${prefix}-summary${suffix}.png`),fullPage:true});
  assert.deepEqual(errors,[]);
  assert.ok(mediaInterruptions.length<=quizzes.length+1,'Unexpected repeated media rejection');
  const config=JSON.parse(await fs.readFile(path.join(root,'course/publication_config.json'),'utf8'));
  await fs.writeFile(path.join(out,`${process.env.H5P_QA_DIRECTORY?'h5p-polished-learning-paths':'h5p-learning-paths'}${suffix}.json`),JSON.stringify({testedUrl:url,source:process.env.H5P_QA_DIRECTORY?'local verified polished MP4':config.active_youtube_url,activeEdition:process.env.H5P_QA_DIRECTORY?'polished local QA':config.active_edition,viewport:page.viewportSize(),paths:report,summary,errors,mediaInterruptions},null,2));
  for(const name of ['h5p-learning-failure.json','h5p-learning-failure.png'])await fs.rm(path.join(out,name),{force:true});
  console.log(JSON.stringify(report));
 }catch(error){
  if(page){const player=await page.evaluate(()=>({time:H5P.instances[0].video.getCurrentTime(),duration:H5P.instances[0].video.getDuration(),summaryButtons:[...document.querySelectorAll('.h5p-end-summary')].map(e=>({class:e.className,text:e.textContent}))}));await fs.writeFile(path.join(out,'h5p-learning-failure.json'),JSON.stringify({message:error.message,completed:report,errors,player,text:await page.locator('body').innerText()},null,2));await page.screenshot({path:path.join(out,'h5p-learning-failure.png'),fullPage:true});}throw error;
 }finally{if(browser)await browser.close();server?.kill();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
