class Logger:
    @staticmethod
    def info(msg: str):
        print(f'INFO: {msg}')

    @staticmethod
    def exception(exception: any):
        if isinstance(exception, Exception):
            print(f'EXCEPTION: {str(exception)}')

        elif isinstance(exception, str):
            print(f'EXCEPTION: {exception}')
