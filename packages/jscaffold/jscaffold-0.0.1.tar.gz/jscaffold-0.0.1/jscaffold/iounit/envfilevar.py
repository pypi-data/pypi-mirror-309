from contextlib import contextmanager
from jscaffold.patchers.assign import PatchAssignment
from .valuable import Valuable


class EnvFileVar(Valuable):
    default_filename = None

    def __init__(self, key, filename=None):
        super().__init__()

        if filename is not None:
            self.filename = filename
        elif EnvFileVar.default_filename is not None:
            self.filename = EnvFileVar.default_filename
        else:
            raise ValueError("filename is not provided")
        self._key = key
        self.patcher = PatchAssignment()

    def _get_key(self):
        return self._key

    def _get_id(self):
        return f"EnvFile:{self.filename}:{self.key}"

    def _write(self, value, context=None):
        content = self._read_file_content()
        replaced, _ = self.patcher(
            content if content is not None else "", self.key, value
        )

        file = open(self.filename, "w")
        file.write(replaced)
        file.close()

        if context is not None and context.log is not None:
            context.log(
                f"Set {self.key}={self._format_display_value(value)} to {self.filename}\n"
            )

    def _read(self, context=None):
        content = self._read_file_content()
        if content is None:
            return None

        _, value = self.patcher(content, self.key)
        return value

    def _read_file_content(self):
        try:
            file = open(self.filename, "r")
            content = file.read()
            file.close()
            self.content = content
        except FileNotFoundError:
            return None
        return content

    @classmethod
    @contextmanager
    def use(cls, filename: str):
        try:
            EnvFileVar.default_filename = filename
            yield
        finally:
            EnvFileVar.default_filename = None
