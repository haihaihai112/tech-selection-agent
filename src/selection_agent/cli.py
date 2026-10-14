import argparse
import os
import uvicorn

from .config import Settings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8050)
    parser.add_argument('--fixture', action='store_true')
    parser.add_argument('--no-ui', action='store_true')
    args = parser.parse_args()
    if args.fixture:
        os.environ['AGENT_MODE'] = 'fixture'
    from .api import create_app
    uvicorn.run(create_app(Settings(), with_ui=not args.no_ui), host=args.host, port=args.port, log_level='warning')


if __name__ == '__main__':
    main()
