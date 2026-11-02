import json
from pathlib import Path
import unittest
from course.publication import make_events
from scripts.author import QUIZZES, MISCONCEPTION_FEEDBACK

ROOT=Path(__file__).resolve().parents[1]
class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events=make_events(json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8')),(ROOT/'narration/lecture.srt').read_text(encoding='utf-8'),QUIZZES,json.loads((ROOT/'course/narration_words.json').read_text(encoding='utf-8')))
        cls.baseline=json.loads((ROOT/'course/publication_baseline.json').read_text(encoding='utf-8'))
    def test_complete_contiguous_frame_schedule(self):
        scenes=self.events['scenes'];self.assertEqual(len(scenes),28)
        self.assertEqual(scenes[0]['start_frame'],0)
        self.assertTrue(all(a['end_frame']==b['start_frame'] for a,b in zip(scenes,scenes[1:])))
        self.assertEqual(sum(s['duration_frames'] for s in scenes),self.baseline['duration_frames'])
        self.assertEqual([s['start_frame'] for s in scenes],self.baseline['scene_start_frames'])
    def test_all_quizzes_keep_timing_and_precede_answer(self):
        for old,q in zip(self.baseline['quizzes'],self.events['quizzes']):
            self.assertEqual(old['time_seconds'],q['time_seconds'])
            self.assertLess(q['hold_start_frame'],q['frame'])
            self.assertGreaterEqual(q['reasoning_silence_seconds'],6)
            self.assertLessEqual(q['reasoning_silence_seconds'],10)
            self.assertGreater(q['answer_reveal_frame']-q['frame'],5*30)
            self.assertLess(q['remediation_frame'],q['frame'])
    def test_subtitles_have_exact_narrative_coverage_and_bounds(self):
        cues=self.events['captions'];self.assertEqual(len(cues),193)
        self.assertTrue(all(0<=c['start_seconds']<c['end_seconds']<=self.events['duration_seconds'] for c in cues))
        self.assertTrue(all(a['end_seconds']<=b['start_seconds'] for a,b in zip(cues,cues[1:])))
    def test_visual_highlights_are_inside_their_spoken_scenes(self):
        self.assertGreaterEqual(len(self.events['highlight_beats']),7)
        for beat in self.events['highlight_beats']:
            s=self.events['scenes'][beat['scene']]
            self.assertTrue(s['start_frame']<=beat['frame']<s['speech_end_frame'])
    def test_wrong_answers_have_specific_distinct_feedback(self):
        for i,(_,_,options,correct,_,_) in enumerate(QUIZZES):
            feedback=MISCONCEPTION_FEEDBACK[f'Q{i+1}']
            self.assertEqual(set(feedback),set(range(len(options)))-{correct})
            self.assertEqual(len(set(feedback.values())),len(feedback))
    def test_physics_values_and_independent_reflection(self):
        p=self.events['physics'];self.assertAlmostEqual(p['T'],.142361995467357,12)
        self.assertAlmostEqual(p['T']+p['R'],1,12)
        self.assertAlmostEqual(p['T_doubled'],.005873079,8)

if __name__=='__main__':unittest.main()
