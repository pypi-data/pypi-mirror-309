# pylint: disable=unspecified-encoding, consider-using-f-string, too-many-locals
from pathlib import (
    Path,
)

from django.test import (
    TestCase,
)

import eduimporter


class XLSReaderTestCase(TestCase):
    def test_xlsreader(self):

        xls_file_path = Path(__file__).parent / 'test_file.xls'

        def cells_to_pair(cells):
            cells = [c for c in cells if c]
            if cells:
                return cells[0], cells[1:]
            return ()

        config = {
            'test': {
                'date_and_int': {
                    'date': ('date', eduimporter.DateCell()),
                    'int': ('int', eduimporter.IntCell(default=-100)),
                },
                'mb_true': (
                    'mb_true',
                    eduimporter.MaybeTrueCell(pattern='y', match_type=eduimporter.MATCH_IF_STARTS_WITH)
                ),
                'enum': (
                    'enum',
                    eduimporter.EnumCell(choices=((1, 'aaa'), (2, 'bbb')), default=3)
                ),
                'opt_strs': {
                    # SUBTREE_CAN_BE_EMPTY: False,
                    'date': ('date', eduimporter.DateCell()),
                    'str': ('str', eduimporter.StringCell()),
                    'mb_str': ('mb_str', eduimporter.MaybeStringCell()),
                    'mb_int': ('mb_int', eduimporter.MaybeIntCell()),
                },
                'pasport': (
                    eduimporter.RegexColumnMatcher(
                        'Номер паспорта', '^(№|Номер) паспорта$'),
                    eduimporter.StringCell(),
                ),
                # Авто определение начала таблицы
                eduimporter.START_ROW: eduimporter.DynamicStartRow(['Date', 'Int']),
                # Не загружать последнюю строку
                eduimporter.END_ROW: -1,
                eduimporter.HEADER_PARSER: cells_to_pair,
            }
        }
        with xls_file_path.open(mode='rb') as xls_file:
            ldr = eduimporter.XLSLoader(xls_file, config=config)

            loaded = ldr.load()

            # ===================================================================
            # Проверка чтения файла
            # ===================================================================
            self.assertTrue(loaded)

            # ===================================================================
            # Проверка разбора шапки
            # ===================================================================
            headers = dict(header for header in ldr.headers['TEST'] if header)

            self.assertIn('единственное значение', headers['Ключ шапки'])

            for header in (1.0, 2.0, 3.0):
                with self.subTest(header):
                    self.assertIn(header, headers['Второй ключ шапки'])

            # ===================================================================
            # Проверка разбора строк без ошибок
            # ===================================================================
            data = ldr.data['TEST']
            success_rows = [5, 8, 9]

            self.assertEqual(len(success_rows), len(data))
            for row in data:
                with self.subTest(row):
                    # Номер строки находится в списке успешных
                    self.assertIn(row['__xls_pos__'][2], success_rows)

            # ===================================================================
            # Проверка разбора строк с ошибками
            # ===================================================================
            fail_rows = [6, 7, 10]

            errors = ldr.rows_log
            self.assertEqual(len(errors), len(fail_rows))
            for error in errors:
                with self.subTest(error):
                    rownum = error[2]
                    self.assertIn(rownum, fail_rows)
