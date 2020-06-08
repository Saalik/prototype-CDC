import argparse
import flask
import flask.views
import json
import logging
import sys


from rainbowfs.logger import Logger


APP = flask.Flask(__name__)
LOGGER = Logger()


def return_fmt(id_):
    """
    format output
    """
    data = {'id': id_}
    return json.dumps(data)


@APP.route('/log/high', methods=['GET'])
def get_high():
    """
    get_high
    """
    return return_fmt(LOGGER.id_high)


@APP.route('/log/low', methods=['GET'])
def get_low():
    """
    get_low
    """
    return return_fmt(LOGGER.id_low)


@APP.route('/log/<int:id_>', methods=['GET'])
def get(id_):
    """
    get log
    """
    data = LOGGER.get(id_)

    if data is None:
        flask.abort(404)

    return data


@APP.route('/log/<int:id_from_>/<int:id_to_>', methods=['GET'])
def get_range(id_from_, id_to_):
    """
    get log
    """
    return flask.Response(LOGGER.get_range(id_from_, id_to_))


@APP.route('/log', methods=['POST'])
def append():
    """
    flush logs
    """
    id_ = LOGGER.append(json.dumps(flask.request.json))

    return return_fmt(id_)


@APP.route('/log', methods=['PUT'])
def flush_all():
    """
    flush all logs
    """
    id_ = LOGGER.flush()

    return return_fmt(id_)


@APP.route('/log/<int:id_>', methods=['PUT'])
def flush(id_):
    """
    flush logs from low to :id_
    """
    id_ = LOGGER.flush(id_)

    return return_fmt(id_)


@APP.route('/log', methods=['DELETE'])
def truncate_all():
    """
    truncate all log
    """
    id_ = LOGGER.truncate()

    return return_fmt(id_)


@APP.route('/log/<int:id_>', methods=['DELETE'])
def truncate(id_):
    """
    truncate log
    """
    id_ = LOGGER.truncate(id_)

    return return_fmt(id_)


def main():
    parser = argparse.ArgumentParser(prog="RainbowFS Log API")

    parser.add_argument('--http-ip',
                        default='0.0.0.0',
                        help='listening HTTP ip')

    parser.add_argument('--http-port',
                        default=5000,
                        type=int,
                        help='listening HTTP port')

    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    APP.logger.addHandler(handler)

    APP.run(debug=False,
            host=args.http_ip,
            port=args.http_port)


if __name__ == '__main__':
    main()
