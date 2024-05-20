from contextlib import contextmanager
from rotkehlchen.db.dbhandler import DBHandler
from rotkehlchen.types import ExternalService, ExternalServiceApiCredentials


@contextmanager
def new_gevent_write_ctx(**kwargs):
    raise Exception('not called')


def test_connection(database: DBHandler):
    assert hasattr(database.conn, 'writer_client') is True
    database.conn.gevent_write_ctx = new_gevent_write_ctx

    with database.conn.read_ctx() as cursor:
        cursor.execute('SELECT COUNT(*) FROM external_service_credentials')
        assert cursor.fetchone()[0] == 7

    with database.user_write() as write_cursor:
        # test with an operation that we usually perform
        database.add_external_service_credentials(
            write_cursor=write_cursor,
            credentials=[
                ExternalServiceApiCredentials(
                    service=ExternalService.THEGRAPH,
                    api_key='test',
                ),
            ],
        )

    with database.conn.read_ctx() as cursor:
        cursor.execute('SELECT COUNT(*) FROM external_service_credentials')
        assert cursor.fetchone()[0] == 8
