import unittest
import threading
from pyteomics import cmass, cparser


class ThreadSafetyTest(unittest.TestCase):
    def test_concurrent_shared_composition_mass(self):
        """Test concurrent mass() calls on the same shared Composition instance."""
        comp = cmass.Composition(sequence='PEPTIDE')
        errors = []

        def worker(charge, average):
            for _ in range(2000):
                try:
                    m = comp.mass(charge=charge, average=average)
                    if m <= 0:
                        errors.append((charge, average, m))
                except Exception as e:
                    errors.append((charge, average, repr(e)))

        configs = [
            (None, False),
            (1, False),
            (2, False),
            (3, False),
            (None, True),
            (1, True),
            (2, True),
            (3, True),
        ]

        threads = [threading.Thread(target=worker, args=c) for c in configs]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])

    def test_concurrent_fast_mass(self):
        """Test concurrent calls to fast_mass and fast_mass2."""
        errors = []

        def worker():
            for _ in range(2000):
                try:
                    m1 = cmass.fast_mass('PEPTIDE')
                    m2 = cmass.fast_mass2('PEPTIDE')
                    if abs(m1 - 799.359) > 0.1 or abs(m2 - 799.359) > 0.1:
                        errors.append((m1, m2))
                except Exception as e:
                    errors.append(repr(e))

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])

    def test_concurrent_parser(self):
        """Test concurrent calls to cparser functions."""
        errors = []

        def worker():
            for _ in range(2000):
                try:
                    p = cparser.parse('PEPTIDE')
                    if len(p) != 7:
                        errors.append(p)
                    comp = cparser.amino_acid_composition('PEPTIDE')
                    if comp['P'] != 2 or comp['E'] != 2:
                        errors.append(comp)
                    l = cparser.length('PEPTIDE')
                    if l != 7:
                        errors.append(l)
                except Exception as e:
                    errors.append(repr(e))

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
