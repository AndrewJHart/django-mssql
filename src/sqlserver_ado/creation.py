DATA_TYPES = {
    'AutoField':         'int IDENTITY (1, 1)',
    'BooleanField':      'bit',
    'CharField':         'varchar(%(max_length)s)',
    'CommaSeparatedIntegerField': 'varchar(%(max_length)s)',
    'DateField':         'smalldatetime',
    'DateTimeField':     'smalldatetime',
    'DecimalField':      'numeric(%(max_digits)s, %(decimal_places)s)',
    'FileField':         'varchar(%(max_length)s)',
    'FilePathField':     'varchar(%(max_length)s)',
    'FloatField':        'double precision',
    'ImageField':        'varchar(%(max_length)s)',
    'IntegerField':      'int',
    'IPAddressField':    'char(15)',
    'NullBooleanField':  'bit',
    'OneToOneField':     'int',
    'PhoneNumberField':  'varchar(20)',
    'PositiveIntegerField': 'int CONSTRAINT [CK_int_pos_%(column)s] CHECK ([%(column)s] > 0)',
    'PositiveSmallIntegerField': 'smallint CONSTRAINT [CK_smallint_pos_%(column)s] CHECK ([%(column)s] > 0)',
    'SlugField':         'varchar(%(max_length)s)',
    'SmallIntegerField': 'smallint',
    'TextField':         'text',
    'TimeField':         'time',
    'USStateField':      'varchar(2)',
}
