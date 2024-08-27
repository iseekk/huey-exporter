import click
import redis
from prometheus_client import start_http_server

from huey_exporter.EventQueue import EventQueue


@click.command()
@click.option('--connection-string', '-c',
              envvar='REDIS_CONNECTION_STRING',
              default='redis://localhost:6379',
              help='Connection string to redis including database. for example redis://localhost:6379/0'
              )
@click.option('--queue-name',
              '-q', envvar='QUEUE_NAME',
              required=True,
              help='Name of the queue to monitor'
              )
@click.option('--port', '-p',
              envvar='EXPORTER_PORT',
              default=9100,
              type=click.IntRange(0, 65535),
              help='Port to expose the metrics on'
              )
def run_exporter(connection_string, queue_name, port):
    # Start up the server to expose the metrics.
    start_http_server(port)
    connection_pool = redis.BlockingConnectionPool.from_url(
        connection_string,
        max_connections=5,
        timeout=10
    )
    queue = EventQueue(queue_name, connection_pool)
    queue.listen()


def main():
    run_exporter()


if __name__ == '__main__':
    main()
