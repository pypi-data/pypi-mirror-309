class Db:
    enable = False
    @staticmethod
    def print(*args, **kwargs):
        if Db.enable:
            print(*args, **kwargs)