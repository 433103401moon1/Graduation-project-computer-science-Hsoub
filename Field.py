from abc import ABC

class Field(ABC):
    field_type = None

    def __init__(self, max_length=255, unique=None):
        if unique is True:
            self.unique = 'UNIQUE'
        else:
            self.unique = ''
        
        if max_length:
            self.max_length = max_length
        
    def __repr__(self):
        column = []
        if self.field_type == 'VARCHAR':
            column.append(f'VARCHAR({self.max_length})')
        else:
            column.append(self.field_type)
            column.append(self.unique)
        return ''.join(column).strip()

class TextField(Field):
    field_type = 'TEXT'

    def __init__(self, unique=None):
        self.unique = unique
        super().__init__(unique=unique)

class IntegerField(Field):
    field_type = 'INTEGER'

    def __init__(self, unique=None):
        self.unique = unique
        super().__init__(unique=unique)


class DatatTime(Field):
    field_type = 'TIMESTAMP'

    def __init__(self, unique = None):
        self.unique = unique
        super().__init__(unique=unique)