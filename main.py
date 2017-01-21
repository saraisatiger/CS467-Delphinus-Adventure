#!/usr/bin/env python3
from gameclient.game_client import *

# For debugging
from debug.debug import *
logger = logging.getLogger(__name__)


def main():
    logger.debug("Entering main() loop")
    GC = GameClient()



if __name__ == "__main__": main()
