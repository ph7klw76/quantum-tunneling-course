import json,unittest
from pathlib import Path
from course.narration_utils import chunks,speech_text,word_error_rate,frame_duration

ROOT=Path(__file__).resolve().parents[1]
class NarrationTests(unittest.TestCase):
    def test_sentence_chunks_preserve_exact_canonical_text(self):
        text='Can an electron pass through a wall? The wavefunction describes a state. Energy is conserved.'
        result=chunks(text,limit=60)
        self.assertEqual(' '.join(result),text)
        self.assertTrue(all(x.endswith(('.', '?')) for x in result))
    def test_engine_specific_pronunciation_does_not_change_captions(self):
        lex=json.loads((ROOT/'narration/voice-config.json').read_text(encoding='utf-8'))['pronunciation']
        text="Schrödinger relates a wavefunction to kappa and Planck's constant."
        self.assertIn('Shroh-ding-er',speech_text(text,'chatterbox',lex))
        self.assertIn('[kappa](/kˈæpə/)',speech_text(text,'kokoro',lex))
        self.assertIn('Schrödinger',text)
    def test_wer_aliases_and_missing_content(self):
        self.assertEqual(word_error_rate('wavefunction','wave function'),0)
        self.assertEqual(word_error_rate("Planck's constant","Plank's constant"),0)
        self.assertEqual(word_error_rate('zero point four five nanometers','0.45 nanometers'),0)
        self.assertEqual(word_error_rate('ten thousand electrons','10,000 electrons'),0)
        self.assertEqual(word_error_rate('fourteen hundred electrons','1,400 electrons'),0)
        self.assertGreater(word_error_rate('energy is conserved','energy is lost'),0)
    def test_frame_quantization_never_truncates(self):
        for duration in [.1,18,23.654,47.777]:
            result=frame_duration(duration)
            self.assertGreaterEqual(result,duration-1e-10)
            self.assertLess(result-duration,1/30+1e-10)
            self.assertAlmostEqual(round(result*30),result*30)
    def test_asr_split_compound_keeps_canonical_caption_and_bounds(self):
        from scripts.neural_narration import align_expected
        words=['The','wave','function','is','not','a','path.']
        decoded={'words':[{'word':w,'start':i*.2,'end':i*.2+.18} for i,w in enumerate(words)]}
        cues,matched,total=align_expected('The wavefunction is not a path.',decoded,1.6)
        self.assertEqual(' '.join(t for _,_,t in cues),'The wavefunction is not a path.')
        self.assertGreater(matched/total,.6)
        self.assertTrue(all(0<=a<b<=1.6 for a,b,_ in cues))

if __name__=='__main__':unittest.main()
