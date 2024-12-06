import unittest
from crdclib import readYAML
from pathlib import Path


class TestReadYaml(unittest.TestCase):


    def test_readyaml(self):
        TESTPATH = Path(__file__).parent
        answer = {'first': ['second', 'third', 'fourth'], 'fifth': {'sixth': 'seventh'}}
        yamltestfile = TESTPATH / 'yamltestfile.yml'
        self.assertEqual(readYAML(yamltestfile), answer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
