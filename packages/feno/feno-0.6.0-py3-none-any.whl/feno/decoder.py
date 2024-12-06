import chardet
from .debug import Db
from .text import Text
class Decoder:

    @staticmethod
    def load(file_path: str) -> str:
        with open(file_path, "rb") as file:
            raw_data = file.read()
            enc_dict = chardet.detect(raw_data)
            Db.print(Text("{g} encoding: {y}", file_path, str(enc_dict)))
            encoding = enc_dict["encoding"]
            if encoding is None or enc_dict["confidence"] < 0.95 :
                encoding = "utf-8"
            try:
                content = raw_data.decode(encoding)
            except UnicodeDecodeError as e:
                content = raw_data.decode(enc_dict["encoding"])
            return content.replace("\r\n", "\n")

    @staticmethod
    def save(file_path: str, content: str):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
