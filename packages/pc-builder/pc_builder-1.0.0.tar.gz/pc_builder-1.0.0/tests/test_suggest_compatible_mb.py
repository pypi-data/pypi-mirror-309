import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.motherboard import suggestCompatibleMotherboards


class TestSuggestCompatibleMotherboards(unittest.TestCase):

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_suggest_compatible_mb(self, mock_load_motherboards):
        """Testing if the function correctly filters out incompatible Motherboards."""

        motherboard1 = MagicMock()
        motherboard1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        motherboard2 = MagicMock()
        motherboard2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        motherboard3 = MagicMock()
        motherboard3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_motherboards.return_value = [motherboard1, motherboard2, motherboard3]

        userBuild = MagicMock()

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(motherboard1, result)
        self.assertIn(motherboard2, result)
        self.assertNotIn(motherboard3, result)

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_suggest_compatible_mb_limit_results(self, mock_load_motherboards):
        """Testing if the function returns no more than 5 compatible Motherboards."""

        compatible_motherboards = [MagicMock() for _ in range(10)]
        for motherboard in compatible_motherboards:
            motherboard.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_motherboards.return_value = compatible_motherboards

        userBuild = MagicMock()

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 5)
        for motherboard in compatible_motherboards[:5]:
            self.assertIn(motherboard, result)

    @patch("pc_builder.components.motherboard.loadMBsfromJSON")
    def test_suggest_compatible_mb_no_compatible_found(self, mock_load_motherboards):
        """Testing if the function returns an empty list when no compatible Motherboards are found."""

        motherboard1 = MagicMock()
        motherboard1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        motherboard2 = MagicMock()
        motherboard2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_motherboards.return_value = [motherboard1, motherboard2]

        userBuild = MagicMock()

        result = suggestCompatibleMotherboards(userBuild, motherboardComp=None)

        self.assertEqual(len(result), 0)
