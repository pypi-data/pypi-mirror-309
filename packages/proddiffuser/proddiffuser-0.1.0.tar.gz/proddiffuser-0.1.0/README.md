# Background Generator

製品画像の背景を生成・合成するPythonパッケージです。

## 概要
このプロジェクトは、Yahoo Inc.の[photo-background-generation](https://huggingface.co/yahoo-inc/photo-background-generation)をベースに開発されています。元のプロジェクトは「Salient Object-Aware Background Generation using Text-Guided Diffusion Models」（CVPR 2024）で発表された手法を実装したものです。

## 使い方
使い方は以下です。

```bash
pip install proddiffuser
```
プロンプトで背景を生成する場合
```bash
proddiffuser generate --product product.jpg --prompt "beach sunset" --output result.png
```
#既存の背景画像を使用
```bash
background-generator generate --product product.jpg --background bg.jpg --output result.png
```
Pythonで使用
```python
from proddiffuser import BackgroundGenerator
generator = BackgroundGenerator()
result = generator.generate_background_with_prompt_and_mask_or_combine(
product_image_path="product.jpg",
prompt="beach sunset",
scale=0.3
)
result.save("output.png")
```
## ライセンス
Apache License 2.0
