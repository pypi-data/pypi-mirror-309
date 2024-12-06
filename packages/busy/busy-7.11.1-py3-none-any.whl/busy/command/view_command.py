import re
from busy.command import CollectionCommand, MultiCollectionCommand
from busy.error import BusyError
from busy.model.item import Item

from wizlib.parser import WizParser

FIELDS = [r'^val:[a-z].*$', 'base', 'url', 'checkbox',
          'tags', 'elapsed', 'simple', 'listable', 'nodata',
          'state', r'^tag:[a-zA-Z][a-zA-Z0-9\-]*$']


class ViewCommand(MultiCollectionCommand):
    """Output items using specified fields. Designed to replace base, describe,
    simple, etc. Defaults to the top item. Outputs with space separation. Note
    that blank lines will appear for any entry with no value."""

    name = 'view'
    fields: str = 'base'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--fields', '-f', default='base')

    @CollectionCommand.wrap
    def execute(self):
        fields = self.fields.split(',')
        unknown_fields = [f for f in fields if
                          not any(re.match(p, f) for p in FIELDS)]
        if any(unknown_fields):
            raise BusyError(f"Unknown field(s) {','.join(unknown_fields)}")

        cols = range(len(fields))
        widths = [1 for f in cols]
        rows = []
        for item in self.selected_items:
            row = []
            for col in cols:
                field = fields[col]
                if field.startswith('val:'):
                    key = field[4]
                    val = item.data_value(key)
                elif field.startswith('tag:'):
                    tag = field[4:]
                    val = tag if tag in item.tags else ''
                else:
                    val = getattr(item, field)
                val = str(val) if val is not None else ''
                widths[col] = max(widths[col], len(val))
                row.append(val)
            rows.append(row)
        return '\n'.join(' '.join(f"{r[c]:<{widths[c]}}"
                                  for c in cols) for r in rows)
