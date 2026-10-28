"""Encode lossless Manim PNGs directly to a high-quality, compatible H.264 MP4.

python export_phone.py /tmp/learning-dynamics-phone/images/learning_dynamics_phone ../images
"""
from pathlib import Path
from fractions import Fraction
import re
import sys
import av
from PIL import Image


def export(source, destination):
    source,destination=Path(source),Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    frames=[p for p in source.glob('LearningDynamicsPhone*.png') if re.search(r'\d+\.png$',p.name)]
    frames.sort(key=lambda p:int(re.search(r'(\d+)\.png$',p.name).group(1)))
    assert frames, f'No PNG frames in {source}'
    video=destination/'learning-dynamics-phone.mp4'
    with av.open(str(video),'w',options={'movflags':'+faststart'}) as container:
        stream=container.add_stream('libx264',rate=30,options={'crf':'14','preset':'slow'})
        stream.width,stream.height=1080,1920
        stream.pix_fmt='yuv420p'
        for i,path in enumerate(frames):
            with Image.open(path) as image:
                frame=av.VideoFrame.from_image(image.convert('RGB'))
            frame.pts=i
            frame.time_base=Fraction(1,30)
            for packet in stream.encode(frame): container.mux(packet)
        for packet in stream.encode(): container.mux(packet)
    Image.open(frames[-1]).save(destination/'learning-dynamics-phone-poster.png')
    # Check the actual phone-size reading experience, not only the full-size render.
    preview_dir=source.parent/'phone-previews'
    preview_dir.mkdir(exist_ok=True)
    for index in [0,round(2.5*30),round(4.8*30)]:
        with Image.open(frames[min(index,len(frames)-1)]) as image:
            image.resize((390,693),Image.Resampling.LANCZOS).save(preview_dir/f'phone-preview-{index}.png')
    print(f'{len(frames)} lossless source frames encoded to {video}; CRF 14, 1080 x 1920')


if __name__=='__main__':
    export(*sys.argv[1:])
