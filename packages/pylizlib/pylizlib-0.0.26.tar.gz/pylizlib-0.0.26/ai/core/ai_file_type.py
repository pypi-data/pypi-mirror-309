from enum import Enum

from network import netutils


class AiFileType(Enum):
    HG_MMPROJ = "mmproj"
    HG_GGML = "ggml"
    PT = "pt"


class AiFile:
    def __init__(
            self,
            file_name: str,
            url: str,
            file_type: AiFileType
    ):
        self.file_name = file_name
        self.url = url
        self.file_type = file_type

    def get_file_size_byte(self) -> int:
        return netutils.get_file_size_byte(self.url)


class AiHgFile:
    def __init__(
            self,
            repository: str,
            file_name: str,
    ):
        self.repository = repository
        self.file_name = file_name

