import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, Mock, patch
from jscaffold.iounit.envvar import EnvVar
from jscaffold.panel.formpanel import FormPanel
import pytest


@patch("jscaffold.services.changedispatcher.ChangeDispatcher.dispatch", Mock())
class TestFormPanel(IsolatedAsyncioTestCase):
    def test_form(self):
        """
        FormPanel can be created
        """
        v = EnvVar("test")
        form1 = FormPanel()
        form2 = form1.form(v)
        assert form1.log_view == form2.log_view

    def test_output_only_form(self):
        """
        Try to create a form with only output.
        No error should be raised.
        """
        FormPanel().run("ls")

    @pytest.mark.asyncio()
    async def test_submit_output_only(self):
        callback = MagicMock()
        form = FormPanel().run(callback)
        form.submit()
        await asyncio.sleep(0)
        callback.assert_called_once()

    @pytest.mark.asyncio()
    async def test_submit_should_be_debounced(self):
        """
        Another submit should not work until the first one is done.
        """
        callback = MagicMock()
        form = FormPanel().run(callback)
        form.submit()  # Run immediately
        assert form.state.is_submitting is True
        form.submit()  # Debounced
        form.submit()
        await asyncio.sleep(0)
        callback.assert_called_once()
        await asyncio.sleep(0.2)
        assert callback.call_count == 2
