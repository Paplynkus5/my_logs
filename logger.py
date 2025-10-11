import logging

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(name)s, %(levelname)s: %(message)s", "%H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


DATA_FILE = open('user.dat', 'r+t')
