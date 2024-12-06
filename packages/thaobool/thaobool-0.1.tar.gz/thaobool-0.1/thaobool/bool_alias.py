# thaobool/bool_alias.py

class ThaoBool:
    def __bool__(self):
        return True

    def __repr__(self):
        return "Thao"

Thao = ThaoBool()
