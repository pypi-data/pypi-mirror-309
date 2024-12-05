from typing import Optional, Tuple, Union

import torch
from diffusers import DiffusionPipeline
from PIL import Image, ImageOps
from tqdm import tqdm
from transparent_background import Remover


class BackgroundGenerator:
    """背景生成と画像合成を行うクラス"""
    
    def __init__(self, device: Optional[str] = None):
        """
        Args:
            device: 使用するデバイス。None の場合は自動選択
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.remover = Remover()
        self.pipe = None  # 必要時に初期化

    def _init_pipeline(self):
        """Stable Diffusion パイプラインの初期化"""
        if self.pipe is None:
            self.pipe = DiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5"
            ).to(self.device)

    def generate_background(
        self, prompt: str, size: Tuple[int, int] = (512, 512)
    ) -> Image.Image:
        """プロンプトから背景画像を生成

        Args:
            prompt: 生成プロンプト
            size: 出力サイズ

        Returns:
            生成された背景画像
        """
        self._init_pipeline()
        image = self.pipe(prompt).images[0]
        return image.resize(size, Image.Resampling.LANCZOS)

    def process_foreground(self, image_path: str) -> Image.Image:
        """前景画像の背景を除去

        Args:
            image_path: 画像パス

        Returns:
            背景除去済み画像
        """
        product_image = Image.open(image_path).convert("RGB")
        foreground = self.remover.process(product_image)
        return foreground.convert("RGBA")

    def combine_images(
        self,
        foreground: Image.Image,
        background: Union[str, Image.Image],
        scale: float = 1.0,
        position: Optional[Tuple[int, int]] = None,
        target_size: Tuple[int, int] = (512, 512),
    ) -> Image.Image:
        """前景と背景を合成

        Args:
            foreground: 前景画像
            background: 背景画像またはパス
            scale: 前景のスケール
            position: 配置位置（Noneの場合は中央）
            target_size: 出力サイズ

        Returns:
            合成画像
        """
        if isinstance(background, str):
            background = Image.open(background)
        
        background = background.convert("RGBA")
        background = self._resize_with_padding(background, target_size)
        
        new_width = int(foreground.width * scale)
        new_height = int(foreground.height * scale)
        foreground = foreground.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if position is None:
            x = (background.width - foreground.width) // 2
            y = (background.height - foreground.height) // 2
        else:
            x, y = position

        combined = background.copy()
        combined.paste(foreground, (x, y), foreground)
        return combined

    def _resize_with_padding(
        self, img: Image.Image, target_size: Tuple[int, int]
    ) -> Image.Image:
        """アスペクト比を保持してリサイズし、パディングを追加

        Args:
            img: 入力画像
            target_size: 目標サイズ

        Returns:
            リサイズ済み画像
        """
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        delta_width = target_size[0] - img.size[0]
        delta_height = target_size[1] - img.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        return ImageOps.expand(img, padding)
