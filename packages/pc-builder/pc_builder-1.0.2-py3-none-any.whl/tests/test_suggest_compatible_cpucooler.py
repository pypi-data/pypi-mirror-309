import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.cpucooler import suggestCompatibleCPUcoolers

class TestSuggestCompatibleCpuCoolers(unittest.TestCase):

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_suggestCompatibleCPUcoolers(self, mock_load_coolers):
        """Testing if the function correctly filters out incompatible CPU coolers."""

        cooler1 = MagicMock()
        cooler1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        cooler2 = MagicMock()
        cooler2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        cooler3 = MagicMock()
        cooler3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_coolers.return_value = [cooler1, cooler2, cooler3]

        userBuild = MagicMock()

        result = suggestCompatibleCPUcoolers(userBuild, cpucoolerComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(cooler1, result)
        self.assertIn(cooler2, result)
        self.assertNotIn(cooler3, result)

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_suggestCompatibleCPUcoolers_limit_results(self, mock_load_coolers):
        """Testing if the function returns no more than 5 compatible CPU coolers."""

        compatible_coolers = [MagicMock() for _ in range(10)]
        for cooler in compatible_coolers:
            cooler.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_coolers.return_value = compatible_coolers

        userBuild = MagicMock()

        result = suggestCompatibleCPUcoolers(userBuild, cpucoolerComp=None)

        self.assertEqual(len(result), 5)
        for cooler in compatible_coolers[:5]:
            self.assertIn(cooler, result)

    @patch("pc_builder.components.cpucooler.loadCPUCoolersfromJSON")
    def test_suggestCompatibleCPUcoolers_no_compatible_found(self, mock_load_coolers):
        """Testing if the function returns an empty list when no compatible CPU coolers are found."""

        cooler1 = MagicMock()
        cooler1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        cooler2 = MagicMock()
        cooler2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_coolers.return_value = [cooler1, cooler2]

        userBuild = MagicMock()

        result = suggestCompatibleCPUcoolers(userBuild, cpucoolerComp=None)

        self.assertEqual(len(result), 0)