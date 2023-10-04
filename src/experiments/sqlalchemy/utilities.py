import pendulum


def create_random_name(prefix: str=''):
    tz = pendulum.local_timezone()
    timestamp = pendulum.now(tz).strftime('%Y%m%d%H%M%S.%f')
    if prefix != '':
        prefix = prefix + '-'
    name = f'{prefix}{timestamp}'
    return name