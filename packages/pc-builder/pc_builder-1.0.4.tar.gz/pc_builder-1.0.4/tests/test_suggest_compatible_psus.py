import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.psu import suggestCompatiblePSUs


class TestSuggestCompatiblepsus(unittest.TestCase):

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_suggest_compatible_psus(self, mock_load_psus):
        """Testing if the function correctly filters out incompatible psus."""

        psu1 = MagicMock()
        psu1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        psu2 = MagicMock()
        psu2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        psu3 = MagicMock()
        psu3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_psus.return_value = [psu1, psu2, psu3]

        userBuild = MagicMock()

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(psu1, result)
        self.assertIn(psu2, result)
        self.assertNotIn(psu3, result)

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_suggest_compatible_psus_limit_results(self, mock_load_psus):
        """Testing if the function returns no more than 5 compatible psus."""

        compatible_psus = [MagicMock() for _ in range(10)]
        for psu in compatible_psus:
            psu.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_psus.return_value = compatible_psus

        userBuild = MagicMock()

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 5)
        for psu in compatible_psus[:5]:
            self.assertIn(psu, result)

    @patch("pc_builder.components.psu.loadPSUsfromJSON")
    def test_suggest_compatible_psus_no_compatible_found(self, mock_load_psus):
        """Testing if the function returns an empty list when no compatible psus are found."""

        psu1 = MagicMock()
        psu1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        psu2 = MagicMock()
        psu2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_psus.return_value = [psu1, psu2]

        userBuild = MagicMock()

        result = suggestCompatiblePSUs(userBuild, psuComp=None)

        self.assertEqual(len(result), 0)
