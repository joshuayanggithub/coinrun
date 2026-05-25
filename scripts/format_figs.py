from pathlib import Path
from PIL import Image


def resize_to_height(im: Image.Image, target_h: int) -> Image.Image:
    if im.height == target_h:
        return im
    w = int(im.width * (target_h / im.height))
    return im.resize((w, target_h), Image.LANCZOS)


def concat_side_by_side(img1_path: Path, img2_path: Path, out_path: Path) -> None:
    a = Image.open(img1_path).convert("RGBA")
    b = Image.open(img2_path).convert("RGBA")

    target_h = max(a.height, b.height)
    a2 = resize_to_height(a, target_h)
    b2 = resize_to_height(b, target_h)

    new = Image.new("RGBA", (a2.width + b2.width, target_h), (255, 255, 255, 0))
    new.paste(a2, (0, 0), a2)
    new.paste(b2, (a2.width, 0), b2)

    new.convert("RGB").save(out_path, "PNG")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    figs = Path(__file__).resolve().parents[1] / "figs"
    img1 = figs / "train loss vs compute.png"
    img2 = figs / "val loss vs compute.png"
    out = figs / "train_and_val_loss.png"

    if not img1.exists() or not img2.exists():
        raise SystemExit("Expected files not found in figs/; check filenames")

    concat_side_by_side(img1, img2, out)
