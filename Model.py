class Model:
    db = None
    connection = None

    def __init__(self):
        self._create_table()
        self._save = False

    @classmethod
    def _get_table_name(cls):
        return cls.__name__.lower()
    
    @classmethod
    def get_columns(cls):
        columns = {}
        for key, value in cls.__dict__.items():
            if str(key).startswith('_'):
                continue
            columns[str(key)] = str(value)
        return columns
    
    def _create_table(self):
        columns = ', '.join(' '.join((key, value)) for (key, value) in self.get_columns().items())
        sql = f'CREATE TABLE IF NOT EXISTS {self._get_table_name()} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})'
        cursor = self.connection.cursor()
        result = cursor.execute(sql)
        return result

    def save(self):
        if self._saved:
            self._update()
            return
        fields = []
        values = []
        for key, value in self._get_values().items():
            fields.append(key)
            values.append(f'"{value}"')

        self._insert_into(fields, values)

    def _get_values(self):
        values = {}
        for key, value in self.__dict__.items():
            if str(key).startswith('_'):
                continue
            if value is False:
                value = 0
            if value is True:
                value = 1
            values[key] = value
        return values
    
    @classmethod
    def create(cls, **kwargs):
        fields = list(kwargs.keys())
        values = []
        for value in kwargs.values():
            values.append(f"'{value}'")
        cls._insert_into(fields, values)

    @classmethod
    def _insert_into(cls, fields, values):
        sql = f'INSERT INTO {cls._get_table_name()} ({", ".join(fields)}) VALUES ({", ".join(values)})'
        result = cls.connection.execute(sql)
        cls.connection.commit()
        cls._saved = True
        return result

    @classmethod
    def all(cls):
        sql = f'SELECT * FROM {cls._get_table_name()}'
        records = cls.connection.execute(sql)
        return records.fetchall()
    
    @classmethod
    def get(cls, col_name, val):
        sql = f'SELECT * FROM {cls._get_table_name()} WHERE {col_name} = "{val}"'
        record = cls.connection.execute(sql)
        result = record.fetchone()
        if result is None:
            return None
        return dict(result)
    
    @classmethod
    def find(cls, col_name, operator, val):
        if operator == 'LIKE':
            value = '%' + value + '%'
        
        sql = f'SELECT * FROM {cls._get_table_name()} WHERE {col_name} {operator} "{val}"'
        records = cls.connection.execute(sql)
        result = [dict(row) for row in records.fetchall()]
        if len(result) == 0:
            return None
        return result
    
    
    def _update(cls, col_name, val):
        new_values = []
        for key, value in cls._get_values().items():
            new_values.append(f'{key} = "{value}"')
        
        expression = ', '.join(new_values)
        sql = f'UPDATE {cls._get_table_name()} SET {expression} WHERE {col_name} = {val}'
        cls.connection.execute(sql)
        cls.connection.commit()
        cls._saved = True


    @classmethod
    def _deleteByID(cls, col_name, id):
        sql = f'DELETE FROM {cls._get_table_name()} WHERE {col_name} = {id}'
        cls.connection.execute(sql)
        cls.connection.commit()
        cls._saved = True

    @classmethod
    def _findAndDelete(cls, col_name, operator, value):
        if operator == 'LIKE':
            value = '%' + value + '%'
        
        sql = f'DELETE FROM {cls._get_table_name()} WHERE {col_name} {operator} "{value}"'
        cls.connection.execute(sql)
        cls.connection.commit()
        cls._saved = True