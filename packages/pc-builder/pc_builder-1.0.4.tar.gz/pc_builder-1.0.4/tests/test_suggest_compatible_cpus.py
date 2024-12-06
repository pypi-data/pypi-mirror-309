import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.cpu import suggestCompatibleCPUs


class TestSuggestCompatibleCPUs(unittest.TestCase):

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_suggest_compatible_cpus(self, mock_load_cpus):
        """Testing if the function correctly filters out incompatible CPUs."""

        cpu1 = MagicMock()
        cpu1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        cpu2 = MagicMock()
        cpu2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        cpu3 = MagicMock()
        cpu3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_cpus.return_value = [cpu1, cpu2, cpu3]

        userBuild = MagicMock()

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(cpu1, result)
        self.assertIn(cpu2, result)
        self.assertNotIn(cpu3, result)

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_suggest_compatible_cpus_limit_results(self, mock_load_cpus):
        """Testing if the function returns no more than 5 compatible CPUs."""

        compatible_cpus = [MagicMock() for _ in range(10)]
        for cpu in compatible_cpus:
            cpu.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_cpus.return_value = compatible_cpus

        userBuild = MagicMock()

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 5)
        for cpu in compatible_cpus[:5]:
            self.assertIn(cpu, result)

    @patch("pc_builder.components.cpu.loadCPUsfromJSON")
    def test_suggest_compatible_cpus_no_compatible_found(self, mock_load_cpus):
        """Testing if the function returns an empty list when no compatible CPUs are found."""

        cpu1 = MagicMock()
        cpu1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        cpu2 = MagicMock()
        cpu2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_cpus.return_value = [cpu1, cpu2]

        userBuild = MagicMock()

        result = suggestCompatibleCPUs(userBuild, cpuComp=None)

        self.assertEqual(len(result), 0)
