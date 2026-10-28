"""Export the Manim MP4 as a looping GIF and a representative PNG.

Usage: python export_animation.py path/to/LearningDynamics.mp4 ../images
Uses PyAV and Pillow, both installed with Manim. No ffmpeg executable needed.
"""
from pathlib import Path
import sys
import av
from PIL import Image


def export(video, destination, stem="learning-dynamics-animated"):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        fps = float(stream.average_rate)
        samples = []
        for i, frame in enumerate(container.decode(stream)):
            if i % round(fps) == 0:
                samples.append(frame.to_image().resize((360, 225)))
        frame.to_image().save(destination / f"{stem}-poster.png")
    # One shared palette avoids flickering colours; sample the full evolution.
    # Preserve saturated annotation colours, which occupy few pixels in thumbnails.
    colors = ["#0B0D12", "#F4F4F4", "#A6ADB9", "#343B49", "#58C4DD",
              "#FFB86B", "#FC6255", "#83C167", "#F5D76E", "#FFFFFF",
              "#828A98", "#586171"]
    swatches = Image.new("RGB", (360, 225))
    for i, color in enumerate(colors):
        swatches.paste(color, (i*30, 0, (i+1)*30, 225))
    samples.append(swatches)
    atlas = Image.new("RGB", (360, 225*len(samples)))
    for i, sample in enumerate(samples):
        atlas.paste(sample, (0, 225*i))
    palette = atlas.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    with av.open(str(video)) as container:
        indexed = [frame.to_image().quantize(palette=palette, dither=Image.Dither.NONE)
                   for frame in container.decode(video=0)]
    # GIF times are integer centiseconds. Alternate delays to retain the video timing.
    durations = [10*(round((i+1)*100/fps)-round(i*100/fps)) for i in range(len(indexed))]
    indexed[0].save(destination / f"{stem}.gif", save_all=True,
                    append_images=indexed[1:], duration=durations, loop=0,
                    optimize=True, disposal=1)
    print(f"Exported {len(indexed)} frames, {sum(durations)/1000:.2f}s, {indexed[0].size}")


if __name__ == "__main__":
    export(*sys.argv[1:])
