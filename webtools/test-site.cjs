/* Real-browser regression checks against this project's isolated test server. */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const {spawn} = require('node:child_process');
const assert = require('node:assert/strict');
const {checkH5pPlayback} = require('./test-h5p-playback.cjs');
const root = path.resolve(__dirname,'..');
const base = 'http://127.0.0.1:8766/quantum-tunneling-course/';
const sleep = ms => new Promise(r=>setTimeout(r,ms));
async function main() {
 const out=path.join(root,'outputs/browser');await fs.mkdir(out,{recursive:true});
 const python=process.env.PYTHON || (process.platform==='win32'?path.join(root,'.venv/Scripts/python.exe'):'python');
 const server=spawn(python,['scripts/serve.py','--directory','outputs/pages','--base-path','/quantum-tunneling-course/','--port','8766'],{cwd:root,stdio:'ignore',windowsHide:true});
 let browser;const report={layouts:[],h5p_questions:[],notebook:null};
 try {
  for(let i=0;i<60;i++){try{if((await fetch(base)).ok)break;}catch{}await sleep(500);if(i===59)throw new Error('Preview server did not start');}
  browser=await chromium.launch({headless:true});
  for(const [name,width,height] of [['desktop',1440,960],['tablet',820,1180],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
   await page.goto(base,{waitUntil:'domcontentloaded'});
   await page.locator('#transmission').filter({hasText:'14.24%'}).waitFor();
   assert.ok((await page.locator('#lectureH5p').getAttribute('src')).startsWith('h5p/quantum-tunneling.html'));
   assert.equal(await page.locator('#h5pLink').count(),0,'Separate interactive-video card must be merged into Watch & Question');
   await page.locator('#lectureH5p').scrollIntoViewIfNeeded();
   await page.waitForFunction(()=>{
     const frame=document.querySelector('#lectureH5p'),content=frame.contentDocument?.querySelector('.h5p-content');
     return content && content.getBoundingClientRect().height>100 && Math.abs(frame.clientHeight-content.getBoundingClientRect().height)<5;
   },{},{timeout:60000});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),name+' horizontal overflow');
   await page.locator('#width').evaluate(el=>{el.value='0.9';el.dispatchEvent(new Event('input'));});
   assert.ok(parseFloat(await page.locator('#transmission').innerText())<1);
   await page.locator('#reset').click();
   assert.equal(await page.locator('#transmission').innerText(),'14.24%');
   assert.equal(await page.locator('#chapters button').count(),7);
   await page.screenshot({path:path.join(out,name+'.png'),fullPage:true});
   report.layouts.push({name,width,height,noOverflow:true,sliders:true,chapters:7});await page.close();
  }
  const page=await browser.newPage();
  const quizzes=JSON.parse(await fs.readFile(path.join(root,'quizzes/quizzes.json'),'utf8'));
  await page.goto(base,{waitUntil:'domcontentloaded'});
  for(let i=0;i<quizzes.length;i++){
   await page.locator('#quiz input').nth(quizzes[i].correct_index).check();
   await page.locator('#quiz button[type=submit]').click();
   assert.ok((await page.locator('#quiz .feedback').innerText()).startsWith('Correct.'));
   await page.locator('#quiz .secondary').click();
  }
  for(let i=0;i<quizzes.length;i++){
   const errors=[];const handler=e=>errors.push(e.message);page.on('pageerror',handler);
   await page.goto(base+`h5p/question-${i+1}.html`,{waitUntil:'domcontentloaded'});
   await page.locator('.h5p-multichoice').waitFor();
   const choices=page.locator('.h5p-alternative-container');
   await choices.nth((quizzes[i].correct_index+1)%quizzes[i].options.length).click();
   await page.locator('.h5p-question-check-answer').click();
   await page.locator('.h5p-question-try-again').waitFor();
   assert.equal(await page.evaluate(()=>H5P.instances[0].getScore()),0);
   assert.ok((await page.locator('.h5p-question-feedback').innerText()).trim().length>0);
   await page.locator('.h5p-question-try-again').click();
   await choices.nth(quizzes[i].correct_index).click();
   await page.locator('.h5p-question-check-answer').click();
   assert.equal(await page.evaluate(()=>H5P.instances[0].getScore()),1);
   assert.deepEqual(errors,[]);page.off('pageerror',handler);
   report.h5p_questions.push({id:i+1,incorrectFeedback:true,retry:true,correctScore:1});
  }
  // Hosted runners can initialize YouTube but may not stream the media.
  // Keep the exact black-frame regression mandatory; run full playback separately.
  report.h5p_playback=await checkH5pPlayback(page,base,out,{startupOnly:process.env.GITHUB_ACTIONS==='true',embedded:true});
  report.h5p_interactive_video=await page.frame({name:'lectureH5pFrame'}).evaluate(()=>({library:H5PIntegration.contents['cid-1'].library,interactions:JSON.parse(H5PIntegration.contents['cid-1'].jsonContent).interactiveVideo.assets.interactions.length}));
  assert.equal(report.h5p_interactive_video.interactions,7);
  await page.setViewportSize({width:390,height:844});
  await page.goto(base+'h5p/question-1.html',{waitUntil:'domcontentloaded'});
  await page.locator('.h5p-multichoice').waitFor();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'H5P phone horizontal overflow');
  await page.screenshot({path:path.join(out,'h5p-phone.png'),fullPage:true});
  report.h5p_phone={width:390,noOverflow:true};
  await page.setViewportSize({width:1440,height:960});
  // Launch the actual indexed notebook and run its cells in Pyodide.
  await page.goto(base+'lab/lab/index.html?path=Quantum_Tunneling_Lab.ipynb',{waitUntil:'domcontentloaded'});
  await page.waitForSelector('.jp-Notebook',{timeout:120000});
  await page.getByRole('menuitem',{name:'Run',exact:true}).click();
  await page.getByText('Run All Cells',{exact:true}).click();
  await page.waitForFunction(()=>Array.from(document.querySelectorAll('.jp-OutputArea-output')).some(e=>e.textContent.includes('log-slope=')),{},{timeout:300000});
  await page.waitForFunction(()=>document.querySelectorAll('.jp-OutputArea-output img,.jp-OutputArea-output canvas,.jp-OutputArea-output svg').length>=3,{},{timeout:30000});
  const notebook=await page.evaluate(()=>({errors:document.querySelectorAll('.jp-OutputArea-error').length,outputs:Array.from(document.querySelectorAll('.jp-OutputArea-output')).map(e=>e.textContent),plots:document.querySelectorAll('.jp-OutputArea-output img,.jp-OutputArea-output canvas,.jp-OutputArea-output svg').length,outputTypes:Array.from(document.querySelectorAll('.jp-OutputArea-output')).map(e=>e.getAttribute('data-mime-type'))}));
  report.notebook=notebook;
  await page.screenshot({path:path.join(out,'jupyterlite.png'),fullPage:true});
  await fs.writeFile(path.join(out,'results.json'),JSON.stringify(report,null,2));
  assert.equal(notebook.errors,0);assert.ok(notebook.outputs.some(s=>s.includes('emscripten')));assert.ok(notebook.outputs.some(s=>s.includes('T+R=1.000000000000')));assert.ok(notebook.plots>=3);
  console.log(JSON.stringify(report));
 } finally {if(browser)await browser.close();server.kill();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
