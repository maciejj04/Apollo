import unittest
import numpy as np
from src.Engine.StaticAudio import StaticAudio
from unittest.mock import patch
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

class StaticAudioTest(unittest.TestCase):
    
#    @patch("src.Commons.CommonAudioInfo.CommonAudioInfo.getChunkSize", return_value=1)
    def testshouldSplitToChunksProperly(self):
        statAudio = StaticAudio(np.ones(2, dtype=np.int16))
        
        self.assertEqual(len(statAudio.chunks), 4)


if __name__ == '__main__':
    unittest.main()
