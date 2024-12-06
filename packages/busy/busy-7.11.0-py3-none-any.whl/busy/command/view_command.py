import re
from busy.command import CollectionCommand, MultiCollectionCommand
from busy.error import BusyError
from busy.model.item import Item

from wizlib.parser import WizParser

FIELDS = [r'^val:[a-z].*$', 'base', 'url', 'checkbox',
          'tags', 'elapsed', 'simple', 'listable', 'nodata']


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

        def row(item: Item):
            result = []
            for field in fields:
                if field.startswith('val:'):
                    key = field[4]
                    val = item.data_value(key)
                else:
                    val = getattr(item, field)
                result.append(str(val) if val is not None else '')
            return ' '.join(result)

        return self.output_items(row)
