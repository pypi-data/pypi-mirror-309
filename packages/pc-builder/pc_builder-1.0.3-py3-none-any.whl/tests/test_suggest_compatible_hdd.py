import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.hdd import suggestCompatibleHDDs

class TestSuggestCompatibleHDDs(unittest.TestCase):

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_suggest_compatible_hdds(self, mock_load_hdds):
        """Testing if the function correctly filters out incompatible HDDs."""

        hdd1 = MagicMock()
        hdd1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        hdd2 = MagicMock()
        hdd2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        hdd3 = MagicMock()
        hdd3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_hdds.return_value = [hdd1, hdd2, hdd3]

        userBuild = MagicMock()

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(hdd1, result)
        self.assertIn(hdd2, result)
        self.assertNotIn(hdd3, result)

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_suggest_compatible_hdds_limit_results(self, mock_load_hdds):
        """Testing if the function returns no more than 5 compatible HDDs."""

        compatible_hdds = [MagicMock() for _ in range(10)]
        for hdd in compatible_hdds:
            hdd.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_hdds.return_value = compatible_hdds

        userBuild = MagicMock()

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 5)
        for hdd in compatible_hdds[:5]:
            self.assertIn(hdd, result)

    @patch("pc_builder.components.hdd.loadHDDsfromJSON")
    def test_suggest_compatible_hdds_no_compatible_found(self, mock_load_hdds):
        """Testing if the function returns an empty list when no compatible HDDs are found."""

        hdd1 = MagicMock()
        hdd1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        hdd2 = MagicMock()
        hdd2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_hdds.return_value = [hdd1, hdd2]

        userBuild = MagicMock()

        result = suggestCompatibleHDDs(userBuild, hddComp=None)

        self.assertEqual(len(result), 0)
