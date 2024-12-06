#built-in
from __future__ import annotations
from itertools import combinations

#internal dependencies
from goombay.algorithms.base import GLOBALBASE as __GLOBALBASE, LOCALBASE as __LOCALBASE
import goombay.algorithms.editdistance as gb

try:
    # external dependencies
    import numpy
    from numpy import float64
    from numpy._typing import NDArray
except ImportError:
    raise ImportError("Please pip install all dependencies from requirements.txt!")

def main():
    seq1 = "HOUSEOFCARDSFALLDOWN"
    seq2 = "HOUSECARDFALLDOWN"
    seq3 = "FALLDOWN"

    print(feng_doolittle(seq1, seq2, seq3)) 

class Feng_Doolittle():
    def __init__(self, pairwise: str = "needleman_wunsch"):
        self.pairwise = pairwise

    def __call__(self, *sequences: str) -> None:
        if len(sequences) < 2:
            raise ValueError("Must have at least 2 sequences for multiple sequence alignment")

        alignment_scores = {}

        for combination in combinations(sequences, 2):
            score = sum([1 for a, b in zip(combination[0], combination[1]) if a == b])
            alignment_scores.setdefault(combination[0], dict())[combination[1]] = score
            alignment_scores.setdefault(combination[1], dict())[combination[0]] = score
            print(combination)
            print(score)
        print(alignment_scores)
        for alignment in alignment_scores.values():
            print(max(alignment, key=alignment.values))
            print(alignment)



feng_doolittle = Feng_Doolittle()

if __name__ == "__main__":
    main()
