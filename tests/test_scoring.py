import unittest

from app.scoring import (
    calculate_experience_score,
    calculate_tfidf_similarity,
    extract_years_of_experience,
)


class TestScoring(unittest.TestCase):

    def test_experience_extraction(self):

        text = """
        Machine Learning Engineer with
        3 years of experience.
        """

        self.assertEqual(
            extract_years_of_experience(text),
            3.0
        )


    def test_experience_requirement_met(self):

        score = calculate_experience_score(
            3,
            2
        )

        self.assertEqual(
            score,
            1.0
        )


    def test_experience_requirement_partial(self):

        score = calculate_experience_score(
            1,
            2
        )

        self.assertEqual(
            score,
            0.5
        )


    def test_tfidf_similarity(self):

        job = """
        Python machine learning SQL
        Pandas NumPy data analysis
        """

        relevant = """
        Python machine learning SQL
        Pandas NumPy data analysis
        """

        unrelated = """
        Graphic design illustration
        photography animation
        """

        scores = calculate_tfidf_similarity(
            job,
            [relevant, unrelated]
        )

        self.assertGreater(
            scores[0],
            scores[1]
        )


if __name__ == "__main__":
    unittest.main()
