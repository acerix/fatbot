#!/usr/bin/env python3

import config

import logging
import os
import time

def main():

    logging.basicConfig(
        filename = os.path.join(config.cache_dir, config.app_name + '.log'),
        level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
    )

    logging.info('Starting '+config.settings['bot']['name']+' version '+config.settings['bot']['version'])
    print('Starting '+config.settings['bot']['name']+' version '+config.settings['bot']['version'])

    print('I am fatbot')

if __name__ == "__main__":
    main()

