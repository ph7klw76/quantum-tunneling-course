import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const events=JSON.parse(fs.readFileSync(new URL('../../course/publication_events.json',import.meta.url),'utf8'));
test('render contains the complete original frame schedule',()=>{
 assert.equal(events.duration_frames,21421);assert.equal(events.fps,30);
 assert.equal(events.scenes.reduce((n,s)=>n+s.duration_frames,0),21421);
});
test('no answer-reveal boundary occurs inside a prediction hold',()=>{
 for(const q of events.quizzes){assert.ok(q.answer_reveal_frame>=q.hold_end_frame);assert.ok(q.frame<q.hold_end_frame);}
});
test('rendered numerical values are the exact physics export',()=>{
 assert.ok(Math.abs(events.physics.T+events.physics.R-1)<1e-12);
 assert.ok(events.physics.T_doubled<events.physics.T/20);
});
