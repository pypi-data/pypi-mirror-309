import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.ram import suggestCompatibleRAMs

class TestSuggestCompatibleRAMs(unittest.TestCase):

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_suggest_compatible_rams(self, mock_load_rams):
        """Testing if the function correctly filters out incompatible RAMs."""

        ram1 = MagicMock()
        ram1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        ram2 = MagicMock()
        ram2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        ram3 = MagicMock()
        ram3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_rams.return_value = [ram1, ram2, ram3]

        userBuild = MagicMock()

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(ram1, result)
        self.assertIn(ram2, result)
        self.assertNotIn(ram3, result)

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_suggest_compatible_rams_limit_results(self, mock_load_rams):
        """Testing if the function returns no more than 5 compatible RAMs."""

        compatible_rams = [MagicMock() for _ in range(10)]
        for ram in compatible_rams:
            ram.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_rams.return_value = compatible_rams

        userBuild = MagicMock()

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 5)
        for ram in compatible_rams[:5]:
            self.assertIn(ram, result)

    @patch("pc_builder.components.ram.loadRAMsfromJSON")
    def test_suggest_compatible_rams_no_compatible_found(self, mock_load_rams):
        """Testing if the function returns an empty list when no compatible RAMs are found."""

        ram1 = MagicMock()
        ram1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        ram2 = MagicMock()
        ram2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_rams.return_value = [ram1, ram2]

        userBuild = MagicMock()

        result = suggestCompatibleRAMs(userBuild, ramComp=None)

        self.assertEqual(len(result), 0)
