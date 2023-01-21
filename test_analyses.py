import unittest
from query_api import query1_chart, query3_wahlbeteiligung, query3_direktkandidaten, query3_wahlbeteiligung2017, query3_direktkandidaten2017


class TestSum(unittest.TestCase):

    def test_q1(self):
        self.assertEqual(query1_chart(
        ), '{"CSU": 45, "CDU": 152, "DIE LINKE": 39, "FDP": 92, "SPD": 206, "GR\\u00dcNE": 118, "AfD": 83, "SSW": 1}')

    def test_q2(self):
        pass



if __name__ == '__main__':
    unittest.main()
