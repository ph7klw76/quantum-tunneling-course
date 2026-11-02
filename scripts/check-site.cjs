const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),dist=path.resolve(process.argv[3]||path.join(root,'website/dist')),q=require(path.join(dist,'physics.js'));
let samples=0;for(const test of JSON.parse(fs.readFileSync(process.argv[2],'utf8'))){const s=q.state(test.E,test.V,test.a);assert.ok(Math.abs(q.transmission(test.E,test.V,test.a)-test.T)<1e-12);assert.ok(Math.abs(s.T+s.R-1)<1e-12);test.x.forEach((x,i)=>{const p=s.psi(x);p.forEach((v,j)=>assert.ok(Math.abs(v-test.p[i][j])<1e-11));samples++;});}
for(const file of ['app.js','interactive.js','physics.js','config.js','video-player.js']){require('node:child_process').execFileSync(process.execPath,['--check',path.join(dist,file)]);}
let links=0;for(const name of fs.readdirSync(dist).filter(f=>f.endsWith('.html'))){const html=fs.readFileSync(path.join(dist,name),'utf8');for(const match of html.matchAll(/(?:href|src)="([^"#]+)"/g)){let target=match[1].split(/[?#]/)[0];if(/^(https?:|data:|mailto:)/.test(target)||!target)continue;assert.ok(fs.existsSync(path.join(dist,target)),`${name}: missing ${target}`);links++;}}
for(const file of fs.readdirSync(dist)){assert.ok(!/\.(mp4|wav)$/i.test(file),'Video/audio masters must not enter Pages');}
const cfg=fs.readFileSync(path.join(dist,'config.js'),'utf8');assert.ok(cfg.includes('WCA_t3ttAAI'));
console.log(`JavaScript/Python agreement: ${samples} wave samples; 5 parameter cases; T+R. Syntax checks: 5 scripts. Local asset links: ${links}.`);
