"""Activate a real, separately uploaded polished YouTube video; never publish by itself."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlparse,parse_qs
import requests
ROOT=Path(__file__).resolve().parents[1]

def video_id(url):
    parsed=urlparse(url)
    if parsed.scheme!='https':raise ValueError('Use an HTTPS YouTube URL')
    if parsed.hostname=='youtu.be':identifier=parsed.path.strip('/')
    elif parsed.hostname in ['youtube.com','www.youtube.com']:identifier=parse_qs(parsed.query).get('v',[''])[0]
    else:raise ValueError('Use an actual YouTube watch/share URL')
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}',identifier):raise ValueError('Invalid YouTube video ID')
    return identifier

def main():
    p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--activate',action='store_true');p.add_argument('--rollback',action='store_true');a=p.parse_args()
    config_path=ROOT/'course/publication_config.json';cfg=json.loads(config_path.read_text(encoding='utf-8'))
    identifier=video_id(a.url)
    if a.rollback and identifier!=video_id(cfg['original_youtube_url']):raise ValueError('Rollback must use the original confirmed YouTube video')
    if not a.rollback and identifier==video_id(cfg['original_youtube_url']):raise ValueError('A polished upload requires a NEW video ID; the original ID cannot have its binary replaced')
    response=requests.get('https://www.youtube.com/oembed',params={'url':'https://www.youtube.com/watch?v='+identifier,'format':'json'},timeout=30);response.raise_for_status()
    info=response.json();assert identifier in info['html'],'Video is not embeddable through the public response'
    if a.activate:
        if not a.rollback:
            verification=json.loads((ROOT/'outputs/remotion-video-verification.json').read_text(encoding='utf-8'))
            assert verification['status']=='PASS' and verification['edition']=='full','Verify the full polished render before activation'
            cfg['polished_youtube_url']=a.url;cfg['active_edition']='polished'
        else:cfg['active_edition']='original'
        cfg['active_youtube_url']=a.url;config_path.write_text(json.dumps(cfg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(title=info['title'],video_id=identifier,activated=a.activate,playback_note='oEmbed validates public metadata, not actual playback. Run the H5P playback checks after regenerating exports.'),indent=2))

if __name__=='__main__':main()
