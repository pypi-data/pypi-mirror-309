from ipywidgets import widgets
from jscaffold.iounit.format import FileSource, FormatType
from jscaffold.widgets.inputwidget import (
    LocalPathInputWidget,
    SelectInputWidget,
    FileUploadInputWidget,
    TextAreaInputWidget,
    TextInputWidget,
    NumberInputWidget,
    InputWidgetType,
)
from ..iounit.iounit import Inputable


class WidgetWrapper:
    def __init__(
        self,
        widget,
        container,
        get_value=None,
        on_click=None,
        set_value=None,
        type=None,
    ):
        self.widget = widget
        self.container = container
        self.get_value = get_value
        self.set_value = set_value
        self.on_click = on_click
        self.type = type

    def focus(self):
        self.widget.focus()


class WidgetFactory:
    def create_link_button(self, description):
        style = """
        <style>
        .jsacffold-link-button {
            background: transparent;
            color: #1976d2;
            width: auto;
        }

        .jsacffold-link-button:hover {
            background: transparent;
            border: none;
            box-shadow: none ! important;
            opacity: 0.5;
        }

        .jsacffold-link-button:active {
            background: transparent;
            border: none;
            box-shadow: none ! important;
            opacity: 0.7;
        }

        .jsacffold-link-button:focus {
            border: none;
            box-shadow: none ! important;
            outline: none ! important;
        }
        </style>
        """
        style_html = widgets.HTML(style)

        button = widgets.Button(description=description)
        button.add_class("jscaffold-link-button")
        container = widgets.Box([button, style_html])

        return WidgetWrapper(
            button, container, on_click=lambda callback: button.on_click(callback)
        )

    def get_input_widget_type(self, input: Inputable):
        if not hasattr(input, "format"):
            return InputWidgetType.Text
        format = input.format
        if format.type == FormatType.Number.value:
            return InputWidgetType.Number
        elif (
            format.type == FormatType.File.value
            and format.file_source == FileSource.Upload.value
        ):
            return InputWidgetType.FileUpload
        if (
            format.type == FormatType.File.value
            and format.file_source == FileSource.Local.value
        ):
            return InputWidgetType.LocalPath
        if input is not None and isinstance(format.select, list):
            return InputWidgetType.Select
        if format.multiline is True or (
            isinstance(format.multiline, int) and format.multiline > 1
        ):
            return InputWidgetType.Textarea
        return InputWidgetType.Text

    def create_input(self, input: Inputable):
        input_widget_type = self.get_input_widget_type(input)

        if input_widget_type == InputWidgetType.Number:
            return NumberInputWidget(input)
        elif input_widget_type == InputWidgetType.Select:
            return SelectInputWidget(input)
        elif input_widget_type == InputWidgetType.Textarea:
            return TextAreaInputWidget(input)
        elif input_widget_type == InputWidgetType.FileUpload:
            return FileUploadInputWidget(input)
        elif input_widget_type == InputWidgetType.LocalPath:
            return LocalPathInputWidget(input)

        return TextInputWidget(input)

    def create_submit_area(self, on_submit, default_label="Submit"):
        submit_button = widgets.Button(description=default_label)

        def button_callback(_):
            on_submit()

        submit_button.on_click(button_callback)

        return (submit_button, submit_button)  # hbox, confirm_button
