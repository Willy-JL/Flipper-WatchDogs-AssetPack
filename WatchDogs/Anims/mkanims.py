from PIL import Image, ImageSequence
import pathlib
import shutil
import sys

if len(sys.argv) < 2:
    raise Exception("Bad arguments!")

ratio = 128 / 64



for input in sys.argv[1:]:
    input = pathlib.Path(input).absolute()

    output = input.with_suffix("")
    shutil.rmtree(output, ignore_errors=True)
    output.mkdir(exist_ok=True)

    img = Image.open(input)
    img_ratio = img.width / img.height
    if img_ratio > ratio:
        resize = (int(64 * img_ratio), 64)
        off = (resize[0] - 128) // 2
        crop = (off, 0, resize[0] - off, resize[1])
    else:
        resize = (128, int(128 / img_ratio))
        off = (resize[1] - 64) // 2
        crop = (0, off, resize[0], resize[1] - off)

    for i, frame in enumerate(ImageSequence.Iterator(img)):
        frame.resize(resize).crop(crop).save(output / f"frame_{i}.png", format="PNG")

    (output / "meta.txt").write_text(f"""Filetype: Flipper Animation
Version: 1

Width: 128
Height: 64
Passive frames: {img.n_frames}
Active frames: 0
Frames order: {' '.join(str(i) for i in range(img.n_frames))}
Active cycles: 0
Frame rate: 4
Duration: 3600
Active cooldown: 0

Bubble slots: 0
""")
    manifest = pathlib.Path("./manifest.txt").absolute()
    if manifest.is_file():
        manifest_text = manifest.read_text()
        if f"Name: {output.name}\n" not in manifest_text:
            manifest.write_text(manifest_text + f"""
Name: {output.name}
Min butthurt: 0
Max butthurt: 18
Min level: 1
Max level: 30
Weight: 3
""")
