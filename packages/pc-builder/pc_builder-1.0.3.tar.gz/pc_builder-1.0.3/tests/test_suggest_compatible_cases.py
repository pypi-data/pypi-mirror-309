import unittest
from unittest.mock import MagicMock, patch
from pc_builder.suggestions.case import suggestCompatibleCases


class TestSuggestCompatibleCases(unittest.TestCase):

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_suggest_compatible_cases(self, mock_load_cases):
        """Testing if the function correctly filters out incompatible Cases."""

        case1 = MagicMock()
        case1.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        case2 = MagicMock()
        case2.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        case3 = MagicMock()
        case3.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_cases.return_value = [case1, case2, case3]

        userBuild = MagicMock()

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 2)
        self.assertIn(case1, result)
        self.assertIn(case2, result)
        self.assertNotIn(case3, result)

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_suggest_compatible_cases_limit_results(self, mock_load_cases):
        """Testing if the function returns no more than 5 compatible Cases."""

        compatible_cases = [MagicMock() for _ in range(10)]
        for case in compatible_cases:
            case.checkCompatibility = MagicMock(return_value=(True, "Compatible"))

        mock_load_cases.return_value = compatible_cases

        userBuild = MagicMock()

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 5)
        for case in compatible_cases[:5]:
            self.assertIn(case, result)

    @patch("pc_builder.components.case.loadCasesfromJSON")
    def test_suggest_compatible_cases_no_compatible_found(self, mock_load_cases):
        """Testing if the function returns an empty list when no compatible Cases are found."""

        case1 = MagicMock()
        case1.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        case2 = MagicMock()
        case2.checkCompatibility = MagicMock(return_value=(False, "Incompatible"))

        mock_load_cases.return_value = [case1, case2]

        userBuild = MagicMock()

        result = suggestCompatibleCases(userBuild, caseComp=None)

        self.assertEqual(len(result), 0)
