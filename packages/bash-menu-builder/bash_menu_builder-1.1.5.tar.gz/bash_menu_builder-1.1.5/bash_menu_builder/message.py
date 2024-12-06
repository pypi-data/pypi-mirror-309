from enum import Enum

from .draw import Draw


class MessageType(Enum):
    ERROR: str = 'error'
    WARNING: str = 'warning'
    SUCCESS: str = 'success'


class Message:
    __tabs: int = 0

    def set_tabs(count: int = 0):
        Message.__tabs = count

    @staticmethod
    def error(message: str, title: str = 'Error'):
        Message.__message(MessageType.ERROR, title, message)

    @staticmethod
    def warning(message: str, title: str = 'Warning'):
        Message.__message(MessageType.WARNING, title, message)

    @staticmethod
    def success(message: str, title: str = 'Success'):
        Message.__message(MessageType.SUCCESS, title, message)

    @staticmethod
    def __message(message_type: MessageType, title: str, message: str) -> None:
        messages: list[str] = message.split('\n')
        message_len: int = Draw.count_biggest_line(message.split('\n'))

        if message_len < len(title) + 15:
            message_len = len(title) + 15

        if message_type.value == MessageType.ERROR.value:
            makeup_title: str = "%s{Red}╭──[{BIRed} %s {Red}]%s╮"
            makeup_text: str = "%s{Red}│{IRed} %s%s {Red}│"
        elif message_type.value == MessageType.WARNING.value:
            makeup_title: str = "%s{Yellow}╭──[{BIYellow} %s {Yellow}]%s╮"
            makeup_text: str = "%s{Yellow}│{IYellow} %s%s {Yellow}│"
        elif message_type.value == MessageType.SUCCESS.value:
            makeup_title: str = "%s{Green}╭──[{BIGreen} %s {Green}]%s╮"
            makeup_text: str = "%s{Green}│{IGreen} %s%s {Green}│"
        else:
            raise RuntimeError('Incorrect type of message!')

        print(Draw.paint(makeup_title) % ('\t' * Message.__tabs, title, ('─' * (message_len - (len(title) + 4)))))

        for msg in messages:
            print(Draw.paint(makeup_text) % ('\t' * Message.__tabs, msg, (' ' * Draw.get_count_spaces_for_line_up(msg, message_len))))

        print(Draw.paint("%s╰%s╯{ColorOff}") % ('\t' * Message.__tabs, '─' * (message_len + 2)))
