import logging
import colorlog


class CustomColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        # Set color for name
        name_color = {
            'UniversalAgent': '34m',  # Blue
            'TranscriptLoop': '32m',  # Green
            'AudioProcessor': '33m',  # Yellow
            'Client': '35m'
        }.get(record.name, '37m')  # Default color is white

        record.name = f'\033[1;{name_color}{record.name}\033[0m'
        return super().format(record)


def setup_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Disable log propagation

    # Avoid adding handlers repeatedly if the logger already has them
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(CustomColoredFormatter(
            '[%(name)s] %(log_color)s%(asctime)s - %(levelname)s: %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        ))
        logger.addHandler(handler)
    return logger