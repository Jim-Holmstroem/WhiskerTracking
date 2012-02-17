import unittest, numpy

from wmath import weighted_choice

class TestWeightedRandomChoice(unittest.TestCase):
    
    def setUp(self):
        self.test_population = numpy.array(range(20))

    def test_returns_nonzero_weight_indices_with_nonzero_probability(self):
        tries_left = int(10*float(max(self.test_population))/min(self.test_population[numpy.nonzero(self.test_population)])*len(self.test_population))

        returned = numpy.zeros_like(self.test_population)
        num_returned = 0

        # Filter out the zeros. Pretend as if all zero-weight indices have been returned for the purpose of checking later. If they do get returned, fail() is called at that time.
        for i, n in enumerate(self.test_population):
            if n == 0:
                returned[i] = 1
                num_returned += 1

        while num_returned < len(self.test_population) and tries_left > 0:
            i = weighted_choice(self.test_population)
            if(self.test_population[i] == 0):
                self.fail("Zero weight index returned: " + str(i))
            if returned[i] == 0:
                returned[i] = 1
                num_returned += 1
            tries_left -= 1

        if num_returned != len(self.test_population):
            # Build error message.
            not_returned = []
            for i, r in enumerate(returned):
                if r == 0:
                    not_returned.append(i)
            self.fail("All indices had not been returned after too many tries. Indices " + str(not_returned) + " were not returned.")

    def test_returns_indices_within_expected_scope(self):
        min_index = 0
        max_index = len(self.test_population) # Not inclusive
        tries_left = len(self.test_population)*100
        while tries_left > 0:
            i = weighted_choice(self.test_population)
            self.assertTrue(i >= 0)
            self.assertTrue(i < max_index)
            tries_left -= 1

    def test_returns_indices_with_expected_probability(self):
        permitted_relative_deviation = 0.01 # 0.01 = 1%
        num_samples = len(self.test_population)*1000
        return_frequencies = numpy.zeros(len(self.test_population))
        expected_frequencies = self.test_population / float(sum(self.test_population)) * num_samples

        for loop in xrange(num_samples):
            return_frequencies[weighted_choice(self.test_population)] += 1
        
        for i, freq in enumerate(return_frequencies):
            if expected_frequencies[i] == 0:
                if freq == 0:
                    continue
                else:
                    self.fail("Zero-weight index was returned: " + i)
                

            relative_deviation = abs(float(freq)/expected_frequencies[i] - 1)
            print i, relative_deviation

            self.assertTrue(relative_deviation <= permitted_relative_deviation, "Frequency deviates too much: " + str(relative_deviation*100) + "%")

if __name__ == '__main__':
    unittest.main()
