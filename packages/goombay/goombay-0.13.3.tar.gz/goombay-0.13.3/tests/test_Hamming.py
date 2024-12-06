from __future__ import annotations
import unittest
from goombay import hamming

class TestHamming(unittest.TestCase):    
    def test_distance_diff(self):
        dist = hamming.distance("ACTG", "FHYU")
        self.assertEqual(dist, 4.0)

    def test_similarity_diff(self):
        sim = hamming.similarity("ACTG", "FHYU")
        self.assertEqual(sim, 0.0)

    def test_norm_distance_diff(self):
        dist = hamming.normalized_distance("ACTG", "FHYU")
        self.assertEqual(dist, 1.0)

    def test_norm_similarity_diff(self):
        sim = hamming.normalized_similarity("ACTG", "FHYU")
        self.assertEqual(sim, 0.0)

    def test_distance_sim(self):
        dist = hamming.distance("ACTG", "ACTG")
        self.assertEqual(dist, 0.0)

    def test_similarity_sim(self):
        sim = hamming.similarity("ACTG", "ACTG")
        self.assertEqual(sim, 4.0)

    def test_norm_distance_sim(self):
        dist = hamming.normalized_distance("ACTG", "ACTG")
        self.assertEqual(dist, 0.0)

    def test_norm_similarity_sim(self):
        sim = hamming.normalized_similarity("ACTG", "ACTG")
        self.assertEqual(sim, 1.0)

    def test_norm_distance1(self):
        dist = hamming.normalized_distance("ACTG", "AATG")
        self.assertEqual(dist, 0.25)

    def test_norm_distance2(self):
        dist = hamming.normalized_distance("ACTG", "AAAG")
        self.assertEqual(dist, 0.5)

    def test_norm_distance3(self):
        dist = hamming.normalized_distance("ACTG", "AAAA")
        self.assertEqual(dist, 0.75)
 
    def test_norm_similarity1(self):
        sim = hamming.normalized_similarity("ACTG", "AATG")
        self.assertEqual(sim, 0.75)

    def test_norm_similarity2(self):
        sim = hamming.normalized_similarity("ACTG", "AAAG")
        self.assertEqual(sim, 0.5)

    def test_norm_similarity3(self):
        sim = hamming.normalized_similarity("ACTG", "AAAA")
        self.assertEqual(sim, 0.25)

    def test_diff_len(self):
        dist = hamming.distance("ACTG", "AATGA")
        self.assertEqual(dist, 2.0)

    def test_diff_len2(self):
        dist = hamming.distance("AATGA", "ACTG")
        self.assertEqual(dist, 2.0)

    def test_binary_diff(self):
        distarray = hamming.binary_distance_array("ACTG", "AATG")
        ans = [1,0,1,1]
        self.assertEqual(distarray, ans)

    def test_binary_sim(self):
        simarray = hamming.binary_similarity_array("ACTG", "AATG")
        ans = [0,1,0,0]
        self.assertEqual(simarray, ans)

    def test_align1(self):
        align = hamming.align("ACTG", "ATGA")
        ans = f"ACTG\nATGA"
        self.assertEqual(align, ans)

    def test_align2(self):
        align = hamming.align("ACTGAA", "ATGA")
        ans = f"ACTGAA\nATGA"
        self.assertEqual(align, ans)

    def test_align_num1(self):
        align = hamming.align(12, 13)
        ans ="0b1100\n0b1101"
        self.assertEqual(align, ans)

    def test_align_num2(self):
        numdist = hamming.distance(12, 13)
        self.assertEqual(numdist, 1)

    def test_align_num1_string(self):
        align = hamming.align("12", "13")
        ans ="0b1100\n0b1101"
        self.assertEqual(align, ans)

    def test_align_num2_string(self):
        numdist = hamming.distance("12", "13")
        self.assertEqual(numdist, 1)

if __name__ == '__main__':
    unittest.main()
