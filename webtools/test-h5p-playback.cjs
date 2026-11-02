/* Exercise the real YouTube-backed H5P player, including video geometry and a timed pause. */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const {spawn} = require('node:child_process');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname,'..');

async function checkH5pPlayback(page,url,out,{startupOnly=false,embedded=false}={}) {
  const errors=[];
  const onError=e=>errors.push(e.message);
  page.on('pageerror',onError);
  try {
    await page.goto(url,{waitUntil:'domcontentloaded'});
    let player=page;
    if(embedded) {
      await page.locator('#lectureH5p').scrollIntoViewIfNeeded();
      player=await (await page.locator('#lectureH5p').elementHandle()).contentFrame();
      assert.ok(player,'The Watch & Question section must embed the H5P lesson');
    }
    const capture=name=>embedded?page.locator('#lecture').screenshot({path:path.join(out,name)}):page.screenshot({path:path.join(out,name),fullPage:true});
    // A lazy iframe can stop scheduling animation frames while its height settles.
    // Poll metadata by timer so readiness does not depend on iframe visibility.
    await player.waitForFunction(()=>window.H5P?.instances[0]?.video?.getDuration?.()>600,{},{timeout:60000,polling:250});
    const sourceVideoUrl=await player.evaluate(()=>H5P.instances[0].options.video.files[0].path);
    const publication=JSON.parse(await fs.readFile(path.join(root,'course/publication_config.json'),'utf8'));
    assert.equal(sourceVideoUrl,publication.active_youtube_url,'Player must load the confirmed active edition');
    const iframe=player.locator('.h5p-video-wrapper iframe');
    const geometry=await iframe.evaluate(el=>{
      const frame=el.getBoundingClientRect(),parent=el.parentElement.getBoundingClientRect();
      return {position:getComputedStyle(el).position,width:frame.width,height:frame.height,offsetTop:frame.top-parent.top,offsetLeft:frame.left-parent.left};
    });
    assert.equal(geometry.position,'absolute','YouTube iframe must overlay its aspect-ratio box');
    assert.ok(Math.abs(geometry.offsetTop)<2 && Math.abs(geometry.offsetLeft)<2,'Video iframe is clipped below its wrapper');
    assert.ok(geometry.width>200 && geometry.height>200);
    assert.deepEqual(errors,[],'Video startup raised a JavaScript error');
    if(startupOnly) {
      if(out) await capture('h5p-video-startup.png');
      return {mode:'startup-only',embedded,sourceVideoUrl,videoDuration:await player.evaluate(()=>H5P.instances[0].video.getDuration()),geometry,javaScriptErrors:errors,streaming:'Not tested on hosted CI; use the standalone playback test from a video-accessible network.'};
    }
    if(await player.locator('.h5p-splash').isVisible()) await player.locator('.h5p-splash').click();
    else await player.locator('.h5p-controls .h5p-pause').click();
    await player.waitForFunction(()=>H5P.instances[0].video.getCurrentTime()>1,{},{timeout:45000});
    const playingTime=await player.evaluate(()=>H5P.instances[0].video.getCurrentTime());
    if(out) await capture('h5p-video-playing.png');
    let chapterTime=null;
    if(embedded) {
      await page.locator('#chapters button').nth(1).click();
      await player.waitForFunction(()=>H5P.instances[0].video.getCurrentTime()>=75.5 && H5P.instances[0].video.getCurrentTime()<82,{},{timeout:30000});
      chapterTime=await player.evaluate(()=>H5P.instances[0].video.getCurrentTime());
    }
    // Seek just before the first real authored question and let playback cross it.
    await player.evaluate(()=>{H5P.instances[0].seek(49);H5P.instances[0].play();});
    const question=player.locator('.h5p-interaction .h5p-multichoice').first();
    await question.waitFor({state:'visible',timeout:30000});
    assert.ok((await question.innerText()).includes('Must transmission vanish'));
    const pausedAt=await player.evaluate(()=>H5P.instances[0].video.getCurrentTime());
    await page.waitForTimeout(1000);
    const pausedAfter=await player.evaluate(()=>H5P.instances[0].video.getCurrentTime());
    assert.ok(Math.abs(pausedAfter-pausedAt)<0.25,'H5P must pause the video for its question');
    assert.ok(pausedAt>=49.8 && pausedAt<56);
    assert.deepEqual(errors,[]);
    if(out) await capture('h5p-timed-question.png');
    return {mode:'streaming',embedded,sourceVideoUrl,videoDuration:await player.evaluate(()=>H5P.instances[0].video.getDuration()),playingTime,chapterTime,geometry,questionDisplayed:true,pausedAt,pausedAfter,javaScriptErrors:errors};
  } catch(error) {
    if(out) {
      const context=await page.evaluate(()=>({url:location.href,text:document.body.innerText.slice(0,3000)})).catch(()=>null);
      await fs.writeFile(path.join(out,'h5p-playback-failure.json'),JSON.stringify({message:error.message,javaScriptErrors:errors,context},null,2));
      await page.screenshot({path:path.join(out,'h5p-playback-failure.png'),fullPage:true}).catch(()=>{});
    }
    throw error;
  } finally {page.off('pageerror',onError);}
}

async function main() {
  const out=path.join(root,'outputs/browser');await fs.mkdir(out,{recursive:true});
  let server,browser;
  try {
    let url=process.env.H5P_TEST_URL;
    const embedded=process.env.H5P_EMBEDDED==='true';
    if(!url) {
      const python=process.env.PYTHON||(process.platform==='win32'?path.join(root,'.venv/Scripts/python.exe'):'python');
      server=spawn(python,['scripts/serve.py','--directory','outputs/pages','--base-path','/quantum-tunneling-course/','--port','8767'],{cwd:root,stdio:'ignore',windowsHide:true});
      url='http://127.0.0.1:8767/quantum-tunneling-course/'+(embedded?'':'h5p/quantum-tunneling.html');
      for(let i=0;i<40;i++) {
        try {if((await fetch(url)).ok)break;}catch{}
        await new Promise(r=>setTimeout(r,250));
      }
    }
    browser=await chromium.launch({headless:true});
    const page=await browser.newPage({viewport:{width:1280,height:900}});
    const result=await checkH5pPlayback(page,url,out,{embedded});
    await fs.writeFile(path.join(out,'h5p-playback.json'),JSON.stringify({url,...result},null,2));
    console.log(JSON.stringify(result));
  } finally {if(browser)await browser.close();if(server)server.kill();}
}
module.exports={checkH5pPlayback};
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
