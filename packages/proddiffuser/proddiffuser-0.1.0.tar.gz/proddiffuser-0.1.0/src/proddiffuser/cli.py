from pathlib import Path

import click

from .generator import BackgroundGenerator


@click.group()
def cli():
    """背景生成・合成ツール"""
    pass

@cli.command()
@click.option("--product", required=True, help="製品画像のパス")
@click.option("--prompt", help="背景生成用プロンプト")
@click.option("--background", help="背景画像のパス")
@click.option("--output", required=True, help="出力先パス")
@click.option("--scale", default=1.0, help="製品画像のスケール")
@click.option("--device", help="使用するデバイス (cuda/cpu)")
def generate(product, prompt, background, output, scale, device):
    """画像を生成・合成します"""
    generator = BackgroundGenerator(device=device)
    
    # 前景処理
    foreground = generator.process_foreground(product)
    
    # 背景準備
    if prompt:
        background_image = generator.generate_background(prompt)
    elif background:
        background_image = Path(background)
    else:
        raise click.BadParameter("プロンプトまたは背景画像が必要です")
    
    # 合成
    result = generator.combine_images(
        foreground=foreground,
        background=background_image,
        scale=scale
    )
    
    # 保存
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path)
    click.echo(f"画像を保存しました: {output_path}")

def main():
    cli()

if __name__ == "__main__":
    main()
