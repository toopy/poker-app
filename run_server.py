#!/usr/bin/env python
from west import log
log.load_config()


CONFIG_SECTION = "app:west-server"
CONFIG_KEY = ""
CONFIG_SEP = ""


if __name__ == "__main__":
    from west.config import Config
    # init config
    Config()
    # prepare config cb
    config_func = Config().get_func(CONFIG_SECTION, CONFIG_KEY, CONFIG_SEP)

    # start site
    from west.socket.twisted.server import add_site
    add_site(config_func)

    # run baby! run!
    from twisted.internet import reactor
    reactor.run()
