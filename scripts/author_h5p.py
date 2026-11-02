"""Create real H5P parameters from the original course activities."""
import copy
import json
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

ROOT = Path(__file__).resolve().parents[1]
LIBS = ROOT / 'tools/h5p/libraries'
SPEC = json.loads((ROOT / 'h5p/authoring.json').read_text(encoding='utf-8'))

def defaults(fields):
    result = {}
    for field in fields:
        if 'default' in field:
            result[field['name']] = copy.deepcopy(field['default'])
        elif field['type'] == 'group':
            result[field['name']] = defaults(field['fields'])
        elif field['type'] == 'list':
            result[field['name']] = []
    return result

def params(library):
    return defaults(json.loads((LIBS/library/'semantics.json').read_text(encoding='utf-8')))

def action(library, parameters, title):
    name, version = library.rsplit('-', 1)
    return dict(library=f'{name} {version}', params=parameters,
                subContentId=str(uuid5(NAMESPACE_URL, 'quantum-tunneling/'+title)),
                metadata=dict(title=title, contentType=name, license='CC BY', licenseVersion='4.0',
                              authors=[dict(name='Applied Quantum Lab', role='Author')]))

def multichoice(q):
    p = params('H5P.MultiChoice-1.16')
    p['question'] = '<p>'+q['question']+'</p>'
    p['answers'] = [dict(text='<p>'+text+'</p>', correct=i == q['correct_index'],
                         tipsAndFeedback=dict(tip='', chosenFeedback=q['explanation'] if i == q['correct_index'] else q['incorrect_feedback'][i], notChosenFeedback=''))
                    for i, text in enumerate(q['options'])]
    p['behaviour'].update(type='single', randomAnswers=False, enableRetry=True, enableSolutionsButton=True, enableCheckButton=True, showScorePoints=True, passPercentage=100)
    p['overallFeedback'] = [dict(from_=0)] if False else [dict(**{'from':0,'to':100,'feedback':q['explanation']})]
    return p

p = params('H5P.InteractiveVideo-1.27')
iv = p['interactiveVideo']
iv['video']['files'] = [dict(path='https://www.youtube.com/watch?v=WCA_t3ttAAI', mime='video/YouTube', copyright=dict(license='CC BY',licenseVersion='4.0'))]
iv['video']['startScreenOptions'].update(title='Quantum Tunneling — Can an Electron Pass Through a Wall?', shortStartDescription='Predict, calculate, and explain. Seven questions pause the lecture; review jumps help you revise your reasoning.')
iv['video']['textTracks'] = dict(videoTrack=[dict(label='English',kind='subtitles',srcLang='en',track=dict(path='subtitles/lecture.vtt',mime='text/vtt'))],defaultTrackLabel='English')
iv['assets']['interactions'] = []
for q in SPEC['interactions']:
    a = action('H5P.MultiChoice-1.16',multichoice(q),q['id']+' — '+q['question'])
    iv['assets']['interactions'].append(dict(duration=dict(**{'from':q['time_seconds'],'to':q['time_seconds']+6}),pause=True,displayType='poster',buttonOnMobile=True,label=q['id'],x=5,y=8,width=90,height=80,libraryTitle='Multiple Choice',action=a,adaptivity=dict(wrong=dict(seekTo=q['remediation_seconds'],allowOptOut=True,message='Review the explanation, then return to this question.',seekLabel='Review explanation'),requireCompletion=False),visuals=dict(backgroundColor='rgb(255, 255, 255)',boxShadow=True)))
iv['assets']['bookmarks'] = [dict(time=c['start'],label=c['title']) for c in json.loads((ROOT/'website/dist/chapters.json').read_text(encoding='utf-8'))]
iv['assets']['endscreens'] = [dict(time=713.5,label='Review and submit practice answers')]
summary = params('H5P.Summary-1.10')
summary['intro'] = '<p>Choose the statement you can defend for each concept. Then complete the independent investigation.</p>'
summary['summaries'] = [dict(summary=['<p>'+s+'</p>' for s in statements],tip=dict(tip='Return to the lecture or computational lab to test your reasoning.')) for statements in SPEC['mastery']['statements']]
iv['summary'] = dict(task=action('H5P.Summary-1.10',summary,'Five concept mastery check'),displayAt=3)
p['override'].update(autoplay=False,loop=False,showRewind10=True,preventSkippingMode='none')
metadata = dict(title=SPEC['title'],language='en',mainLibrary='H5P.InteractiveVideo',embedTypes=['div'],license='CC BY',licenseVersion='4.0',authors=[dict(name='Applied Quantum Lab',role='Author')],preloadedDependencies=[dict(machineName=name,majorVersion=major,minorVersion=minor) for name,major,minor in [('H5P.InteractiveVideo',1,27),('H5P.MultiChoice',1,16),('H5P.Summary',1,10)]])
for name, data in [('content.json',p),('h5p.json',metadata)]:
    (ROOT/'h5p'/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
# Standalone activities provide an accessible alternative when YouTube is blocked.
(ROOT/'h5p/questions.json').write_text(json.dumps([multichoice(q) for q in SPEC['interactions']],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Authored 7 native H5P questions, review jumps, bookmarks and 5-concept Summary.')
