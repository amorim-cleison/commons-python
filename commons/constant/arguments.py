from commons.util import Argument

GLOBAL_ARGS = [
    Argument("-c",
             "--config",
             type=str,
             default="./config/config.yaml",
             help="Configuration file"),
    Argument("-l",
             "--log",
             type=str,
             default="./output.log",
             help="Location to save log file"),
    Argument("-v",
             "--verbosity",
             type=int,
             default=5,
             help="Verbosity level for logging")
]
