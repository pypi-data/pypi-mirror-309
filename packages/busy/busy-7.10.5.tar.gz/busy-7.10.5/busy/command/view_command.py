import re
from busy.command import CollectionCommand
from busy.error import BusyError
from busy.model.item import Item

from wizlib.parser import WizParser

FIELDS = [r'^val:[a-z].*$']


class ViewCommand(CollectionCommand):
    """Output items using specified fields. Designed to replace base, describe,
    simple, etc. Defaults to the top item. Outputs crude comma separation."""

    name = 'view'
    fields: str = ''

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--fields', '-f', default='')

    @CollectionCommand.wrap
    def execute(self):
        fields = self.fields.split(',')
        unknown_fields = [f for f in fields if
                          not any(re.match(p, f) for p in FIELDS)]
        if any(unknown_fields):
            raise BusyError(f"Unknown field(s) {','.join(unknown_fields)}")

        def row(item: Item):
            if fields == ['']:
                return item.description
            result = ''
            for field in fields:
                if field.startswith('val:'):
                    key = field[4]
                    val = field[5:]
                    result += ',' if result else ''
                    result += item.data_value(key)
            return result

        return self.output_items(row)
