import pytest

from tests.conftest import BaseTest
from python3_capsolver.core.enum import SaveFormatsEnm
from python3_capsolver.core.captcha_instrument import FileInstrument


class TestFileInstrument(BaseTest):
    """
    Success tests
    """

    def test_file_processing_exist(self):
        assert "file_processing" in FileInstrument.__dict__.keys()
        assert "aio_file_processing" in FileInstrument.__dict__.keys()

    def test_captcha_base64(self):
        assert self.read_image_as_str() == FileInstrument().file_processing(captcha_base64=self.read_image())

    def test_captcha_file(self):
        assert self.read_image_as_str() == FileInstrument().file_processing(
            captcha_file=self.image_captcha_path_example
        )

    @pytest.mark.parametrize("const_save_format", SaveFormatsEnm)
    def test_captcha_link(self, const_save_format):
        result = FileInstrument().file_processing(
            save_format=const_save_format, captcha_link=self.image_captcha_url_example
        )
        assert isinstance(result, str)

    async def test_aio_captcha_base64(self):
        assert self.read_image_as_str() == await FileInstrument().aio_file_processing(captcha_base64=self.read_image())

    async def test_aio_captcha_file(self):
        assert self.read_image_as_str() == await FileInstrument().aio_file_processing(
            captcha_file=self.image_captcha_path_example
        )

    @pytest.mark.parametrize("const_save_format", SaveFormatsEnm)
    async def test_aio_captcha_link(self, const_save_format):
        result = await FileInstrument().aio_file_processing(
            save_format=const_save_format, captcha_link=self.image_captcha_url_example
        )
        assert isinstance(result, str)

    """
    Failed tests
    """

    def test_file_processing_err(self):
        with pytest.raises(ValueError):
            FileInstrument().file_processing()

    async def test_aio_file_processing_err(self):
        with pytest.raises(ValueError):
            await FileInstrument().aio_file_processing()
