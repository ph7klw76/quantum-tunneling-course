const fs = require('node:fs/promises');
const fss = require('node:fs');
const path = require('node:path');
const {once} = require('node:events');
const H5P = require('@lumieducation/h5p-server');
const HtmlExporter = require('@lumieducation/h5p-html-exporter').default;
const root = path.resolve(__dirname, '..');
const work = path.join(root, 'tools/h5p');
const user = {id:'author',name:'Applied Quantum Lab',email:'',type:'local'};
const viewport = html => html.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">');
async function main() {
  const {FileLibraryStorage,FileContentStorage,DirectoryTemporaryFileStorage,InMemoryStorage} = H5P.fsImplementations;
  for (const dir of ['libraries','content','temp']) await fs.mkdir(path.join(work,dir),{recursive:true});
  const libraries = new FileLibraryStorage(path.join(work,'libraries'));
  const content = new FileContentStorage(path.join(work,'content'));
  const config = new H5P.H5PConfig(new InMemoryStorage(), {coreApiVersion:{major:1,minor:28},h5pVersion:'1.28.0',maxTotalSize:128*1024*1024,maxFileSize:64*1024*1024});
  const editor = new H5P.H5PEditor(new InMemoryStorage(),config,libraries,content,new DirectoryTemporaryFileStorage(path.join(work,'temp')),undefined,undefined,{permissionSystem:new H5P.LaissezFairePermissionSystem()});
  for (const name of ['H5P.InteractiveVideo','H5P.MultiChoice','H5P.Summary']) {
    const result = await editor.uploadPackage(path.join(work,name+'.h5p'),user,{onlyInstallLibraries:true});
    console.log(name, result.installedLibraries.length, 'libraries installed');
  }
  // The Hub bundle still contains Video 1.6.66, whose YouTube handler reads
  // private YT.Player internals. Install the pinned official upstream fix.
  const videoDirectory = path.join(work,'video-upstream');
  const videoMetadata = JSON.parse(await fs.readFile(path.join(videoDirectory,'library.json'),'utf8'));
  if (videoMetadata.machineName!=='H5P.Video' || videoMetadata.majorVersion!==1 || videoMetadata.minorVersion!==6 || videoMetadata.patchVersion!==81) throw new Error('Expected pinned official H5P.Video 1.6.81');
  for (const file of [...videoMetadata.preloadedJs,...videoMetadata.preloadedCss]) {
    const full = path.resolve(videoDirectory,file.path);
    if (!full.startsWith(videoDirectory+path.sep)) throw new Error('Invalid library file path');
    await fs.access(full);
  }
  console.log('Official H5P.Video update:',await editor.libraryManager.installFromDirectory(videoDirectory));
  if (process.argv.includes('--libraries-only')) return;
  // Parameters are generated below from the original licensed course activities.
  const params = JSON.parse(await fs.readFile(path.join(root,'h5p/content.json'),'utf8'));
  const metadata = JSON.parse(await fs.readFile(path.join(root,'h5p/h5p.json'),'utf8'));
  const id = await content.addContent(metadata,params,user,'1');
  await content.addFile(id,'subtitles/lecture.vtt',fss.createReadStream(path.join(root,'website/dist/lecture.vtt')),user);
  const exporter = new HtmlExporter(libraries,content,config,path.join(work,'core'),path.join(work,'editor'));
  const html = viewport(await exporter.createSingleBundle(id,user,{showLicenseButton:true,showFrame:true}));
  await fs.mkdir(path.join(root,'website/dist/h5p'),{recursive:true});
  await fs.writeFile(path.join(root,'website/dist/h5p/quantum-tunneling.html'),html);
  const packager = new H5P.PackageExporter(editor.libraryManager,content,{exportMaxContentPathLength:255,permissionSystem:new H5P.LaissezFairePermissionSystem()});
  const stream = fss.createWriteStream(path.join(root,'h5p/Quantum_Tunneling_Interactive.h5p'));
  const finished = once(stream,'finish');
  await packager.createPackage(id,stream,user); await finished;
  const questions = JSON.parse(await fs.readFile(path.join(root,'h5p/questions.json'),'utf8'));
  for (let i=0;i<questions.length;i++) {
    const qid = String(i+2);
    await content.addContent({...metadata,mainLibrary:'H5P.MultiChoice',title:'Practice question '+(i+1),preloadedDependencies:[{machineName:'H5P.MultiChoice',majorVersion:1,minorVersion:16}]},questions[i],user,qid);
    await fs.writeFile(path.join(root,`website/dist/h5p/question-${i+1}.html`),viewport(await exporter.createSingleBundle(qid,user,{showLicenseButton:true,showFrame:true})));
  }
  console.log('Exported native .h5p and Lumi HTML',html.length);
}
main().catch(e=>{console.error(e);process.exitCode=1;});
