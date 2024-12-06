from enum import Enum
from jscaffold.iounit.format import Format
from jscaffold.iounit.iounit import Inputable
from jscaffold.services.tkservice import tk_serivce
from ipywidgets import widgets
from jscaffold.iounit.valuable import Valuable
import tempfile
import os
from pathlib import Path

from jscaffold.widgets.ipywidgetwrapper import IPYWidgetWrapper


def read_input(input: Inputable):
    if isinstance(input, Valuable):
        return input.value
    else:
        return input.read()


class InputWidgetType(Enum):
    Text = "text"
    Select = "select"
    Textarea = "textarea"
    FileUpload = "upload_file"
    LocalPath = "local_path"
    Number = "number"


class InputWidget(IPYWidgetWrapper):
    def __init__(self, type, input, child):
        self.type = type
        self.input = input
        format = input.format if hasattr(input, "format") else Format()
        self.desc_html = widgets.HTML(
            value=format.desc if format.desc is not None else ""
        )
        self.widget = widgets.VBox([child, self.desc_html])
        self.update_widget()

    def update_widget(self):
        format = self.input.format if hasattr(self.input, "format") else Format()
        desc = format.desc
        if desc is not None:
            self.desc_html.value = desc
        self.desc_html.layout.visibility = "visible" if desc else "hidden"

    def get_widget(self):
        return self.widget

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, _value):
        raise NotImplementedError

    def observe(self, func):
        raise NotImplementedError


class TextInputWidget(InputWidget):
    def __init__(self, input: Inputable):
        value = input.read() if input is not None else None
        format = input.format if hasattr(input, "format") else Format()
        password = format.password
        placeholder = input.get_defaults() if hasattr(input, "get_defaults") else None
        if placeholder is None:
            placeholder = ""
        layout = widgets.Layout(width="360px")
        if password is True:
            text_widget = widgets.Password(
                value=value,
                layout=layout,
                placeholder=placeholder,
                disabled=format.readonly,
            )
        else:
            text_widget = widgets.Text(
                value=value,
                layout=layout,
                placeholder=placeholder,
                disabled=format.readonly,
            )

        self.text_widget = text_widget
        super().__init__(InputWidgetType.Text.value, input, text_widget)

    @property
    def value(self):
        return self.text_widget.value

    @value.setter
    def value(self, value):
        if value is None:
            value = ""
        if self.text_widget.value != value:
            self.text_widget.value = str(value) if value is not None else ""

    def observe(self, func):
        self.text_widget.observe(func)


DEFAULT_ROW_COUNT = 5


class TextAreaInputWidget(InputWidget):
    def __init__(self, input: Inputable):
        value = input.read()
        placeholder = input.get_defaults()
        if placeholder is None:
            placeholder = ""
        format = input.format
        rows = (
            format.multiline
            if not isinstance(format.multiline, bool)
            else DEFAULT_ROW_COUNT
        )
        layout = widgets.Layout(width="360px")
        textarea = widgets.Textarea(
            value=value,
            rows=rows,
            placeholder=placeholder,
            layout=layout,
            disabled=format.readonly,
        )
        self.textarea = textarea
        super().__init__(InputWidgetType.Textarea.value, input, textarea)

    @property
    def value(self):
        return self.textarea.value

    @value.setter
    def value(self, value):
        if value is None:
            value = ""
        if self.textarea.value != value:
            self.textarea.value = str(value) if value is not None else ""

    def observe(self, func):
        return self.textarea.observe(func)


class SelectInputWidget(InputWidget):
    def __init__(self, input: Inputable):
        value = input.read()
        format = input.format
        self.format = format
        if value not in format.select:
            if input.defaults in format.select:
                value = input.defaults
            else:
                value = None
        layout = widgets.Layout(width="360px")
        select_widget = widgets.Select(
            options=format.select, value=value, disabled=format.readonly, layout=layout
        )
        self.select_widget = select_widget
        super().__init__(InputWidgetType.Select.value, input, select_widget)

    @property
    def value(self):
        return self.select_widget.value

    @value.setter
    def value(self, value):
        if value not in self.format.select:
            value = None
        self.select_widget.value = value

    def observe(self, func):
        return self.select_widget.observe(func)

    def update_widget(self):
        super().update_widget()
        self.select_widget.disabled = self.format.readonly
        orig_value = self.select_widget.value
        self.select_widget.options = self.format.select
        if orig_value in self.format.select:
            self.select_widget.value = orig_value


class FileUploadInputWidget(InputWidget):
    def __init__(self, input: Inputable):
        value = str(input) if input is not None else None

        format = input.format
        text_box = widgets.Text(value=value, disabled=format.readonly)
        uploader = widgets.FileUpload(multiple=False)
        self.text_box = text_box

        def get_upload_folder():
            if format.upload_folder is not None:
                return format.upload_folder
            base_dir = tempfile.mkdtemp()
            if format.mkdir:
                Path(base_dir).mkdir(parents=True, exist_ok=True)
            return base_dir

        def on_upload_change(change):
            if change["type"] == "change" and change["name"] == "value":
                (file_dict,) = uploader.value
                # Remarks: type, content, size inside the file_dict
                filename = file_dict["name"]
                base_dir = get_upload_folder()
                abs_path = os.path.join(base_dir, filename)
                named_file = open(abs_path, "wb")
                named_file.write(file_dict["content"])
                named_file.close()
                text_box.value = abs_path

        uploader.observe(on_upload_change, names="value")

        hbox = widgets.HBox([text_box, uploader], layout=widgets.Layout(width="360px"))
        super().__init__(InputWidgetType.FileUpload.value, input, hbox)

    @property
    def value(self):
        return self.text_box.value

    @value.setter
    def value(self, value):
        if self.text_box.value != value:
            self.text_box.value = str(value) if value is not None else ""

    def observe(self, func):
        return self.text_box.observe(func)


class LocalPathInputWidget(InputWidget):
    def __init__(self, input: Inputable):
        def on_click(_):
            self.browser_button.disabled = True
            file_path = tk_serivce.open_file_dialog(input.format.file_type)
            self.browser_button.disabled = False
            if file_path == "":
                return
            text_box.value = file_path

        value = input.read()
        format = input.format
        placeholder = input.get_defaults()
        if placeholder is None:
            placeholder = ""
        text_box = widgets.Text(
            value=value,
            placeholder=placeholder,
            disabled=format.readonly,
        )
        browse_button = widgets.Button(description="Browse", disabled=format.readonly)
        self.text_box = text_box
        self.browser_button = browse_button
        hbox = widgets.HBox(
            [text_box, browse_button], layout=widgets.Layout(width="360px")
        )
        browse_button.on_click(on_click)
        super().__init__(InputWidgetType.LocalPath.value, input, hbox)

    @property
    def value(self):
        return self.text_box.value

    @value.setter
    def value(self, value):
        if self.text_box.value != value:
            self.text_box.value = str(value) if value is not None else ""

    def observe(self, func):
        return self.text_box.observe(func)


class NumberInputWidget(InputWidget):
    def __init__(self, input: Inputable):
        value = read_input(input)
        placeholder = input.get_defaults()
        if placeholder is None:
            placeholder = ""
        format = input.format
        layout = widgets.Layout(width="360px")

        float_text = widgets.FloatText(
            value=value,
            plreaceholder=placeholder,
            layout=layout,
            disabled=format.readonly,
        )

        self.float_text = float_text
        super().__init__(InputWidgetType.Textarea.value, input, float_text)

    def update_widget(self):
        super().update_widget()
        format = self.input.format
        self.float_text.disabled = format.readonly

    @property
    def value(self):
        return self.float_text.value

    @value.setter
    def value(self, value):
        if value is not None and self.float_text.value != value:
            self.float_text.value = float(value)

    def observe(self, func):
        return self.float_text.observe(func)
