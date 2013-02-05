
CONFIG_SECTION = "app:west-server"
CONFIG_KEY = ""
CONFIG_SEP = ""


if __name__ == "__main__":
    # west import
    from west.config import Config
    from west.log import get_logger
    from west.twisted.server import add_site

    # init config
    logger = get_logger(__file__, "west.socket")
    Config()

    # prepare config cb
    config_func = Config().get_func(CONFIG_SECTION, CONFIG_KEY, CONFIG_SEP)
    # start site
    add_site(config_func)

    # run baby! run!
    from twisted.internet import reactor
    reactor.run()
