import os
import tempfile

import pytest
from PIL import Image


# テスト用の画像を作成する fixture
@pytest.fixture
def sample_image():
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        image = Image.new('RGB', (100, 100), color='red')
        image.save(f.name)
        yield f.name
        os.unlink(f.name)

def test_background_generator_init():
    from proddiffuser.generator import BackgroundGenerator  # パッケージ名を変更
    generator = BackgroundGenerator(device="cpu")
    assert generator.device == "cpu"

def test_process_foreground(sample_image):
    from proddiffuser.generator import BackgroundGenerator  # パッケージ名を変更
    generator = BackgroundGenerator(device="cpu")
    result = generator.process_foreground(sample_image)
    assert isinstance(result, Image.Image)
    assert result.mode == "RGBA"
