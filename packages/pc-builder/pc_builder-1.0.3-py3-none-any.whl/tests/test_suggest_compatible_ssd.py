import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.ssd import suggestCompatibleSSDs

class TestSuggestCompatibleSSDs(unittest.TestCase):

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds(self, mock_load_ssds):
        """Testing if the function correctly filters out incompatible SSDs."""

        ssd1 = MagicMock()
        ssd1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        ssd2 = MagicMock()
        ssd2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        ssd3 = MagicMock()
        ssd3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_ssds.return_value = [ssd1, ssd2, ssd3]

        userBuild = MagicMock()

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(ssd1, result)
        self.assertIn(ssd2, result)
        self.assertNotIn(ssd3, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds_limit_results(self, mock_load_ssds):
        """Testing if the function returns no more than 5 compatible SSDs."""

        compatible_ssds = [MagicMock() for _ in range(10)]
        for ssd in compatible_ssds:
            ssd.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_ssds.return_value = compatible_ssds

        userBuild = MagicMock()

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 5)
        for ssd in compatible_ssds[:5]:
            self.assertIn(ssd, result)

    @patch("pc_builder.components.ssd.loadSSDsfromJSON")
    def test_suggest_compatible_ssds_no_compatible_found(self, mock_load_ssds):
        """Testing if the function returns an empty list when no compatible SSDs are found."""

        ssd1 = MagicMock()
        ssd1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        ssd2 = MagicMock()
        ssd2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_ssds.return_value = [ssd1, ssd2]

        userBuild = MagicMock()

        result = suggestCompatibleSSDs(userBuild, ssdComp=None)

        self.assertEqual(len(result), 0)
