# pylint: disable=import-outside-toplevel, unused-import
from django.test.testcases import (
    TestCase,
)


class ReportTestCase(TestCase):
    def test_report(self):
        # Пока просто импортируем модуль для проверки совместимости
        from eduimporter.report import BaseFailureImportReport  # noqa
