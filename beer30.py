#!/usr/bin/env python3

import argparse
import asyncio
import dotenv
import logging
import os

import beer30

dotenv.load_dotenv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--admins', metavar='ADMIN', nargs='+', help='slack id for admins: ie: "--admins U123 U456"')
    parser.add_argument('--log-level', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], default=os.environ.get('BEER30_LOG_LEVEL', 'WARNING'), help='level of logs')
    parser.add_argument('--password', default=os.environ.get('BEER30_PASSWORD', None), help='password to set light state')
    parser.add_argument('-p', '--port', type=int, default=os.environ.get('BEER30_PORT', 8080), help='the port for the http server')
    parser.add_argument('-t', '--token', default=os.environ.get('BEER30_SLACK_TOKEN', None), help='slack token for the bot')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=args.log_level)

    logging.debug('Getting main event loop.')
    loop = asyncio.get_event_loop()
    try:
        # Start light
        logging.info('Initializing light...')
        light = beer30.Light()
        logging.info('Light successfully initialized.')

        # Start bot
        logging.info('Initializing Slack bot...')
        bot = beer30.Bot(token = args.token, light = light, admins = args.admins)
        logging.info('Slack bot successfully initialized.')
        logging.debug('Adding bot to event loop.')
        loop.create_task(bot.start())

        # Start website
        logging.info('Initializing website...')
        site = beer30.Site(light = light, port = args.port, password = args.password)
        logging.info('Website successfully initialized.')
        logging.debug('Adding website to event loop.')
        loop.create_task(site.start())

        logging.debug('Starting main event loop...')
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt captured. Exiting application...')
    finally:
        logging.debug('Stopping main event loop...')
        loop.close()
        logging.debug('Main event loop stopped.')