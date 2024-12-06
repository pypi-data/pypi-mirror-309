import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.gpu import suggestCompatibleGPUs


class TestSuggestCompatibleGPUs(unittest.TestCase):

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_suggest_compatible_gpus(self, mock_load_gpus):
        """Testing if the function correctly filters out incompatible gpus."""

        gpu1 = MagicMock()
        gpu1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        gpu2 = MagicMock()
        gpu2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        gpu3 = MagicMock()
        gpu3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_gpus.return_value = [gpu1, gpu2, gpu3]

        userBuild = MagicMock()

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(gpu1, result)
        self.assertIn(gpu2, result)
        self.assertNotIn(gpu3, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_suggest_compatible_gpus_limit_results(self, mock_load_gpus):
        """Testing if the function returns no more than 5 compatible gpus."""

        compatible_gpus = [MagicMock() for _ in range(10)]
        for gpu in compatible_gpus:
            gpu.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_gpus.return_value = compatible_gpus

        userBuild = MagicMock()

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 5)
        for gpu in compatible_gpus[:5]:
            self.assertIn(gpu, result)

    @patch("pc_builder.components.gpu.loadGPUsfromJSON")
    def test_suggest_compatible_gpus_no_compatible_found(self, mock_load_gpus):
        """Testing if the function returns an empty list when no compatible gpus are found."""

        gpu1 = MagicMock()
        gpu1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        gpu2 = MagicMock()
        gpu2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_gpus.return_value = [gpu1, gpu2]

        userBuild = MagicMock()

        result = suggestCompatibleGPUs(userBuild, gpuComp=None)

        self.assertEqual(len(result), 0)
