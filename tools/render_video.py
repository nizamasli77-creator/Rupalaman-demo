"""Render an animated HTML page to MP4.
The HTML must define window.__render(t) (t in seconds) that draws the frame at time t
inside an element with id="stage" sized WxH. Usage:
  python3 tools/render_video.py page.html out.mp4 --w 1080 --h 1920 --dur 15 --fps 30 [--audio sound.wav]
Uses the preinstalled Chromium (Playwright) and ffmpeg."""
import argparse, os, subprocess, tempfile
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser()
ap.add_argument("html"); ap.add_argument("out")
ap.add_argument("--w", type=int, default=1080); ap.add_argument("--h", type=int, default=1920)
ap.add_argument("--dur", type=float, default=15); ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--audio", default=None)
a = ap.parse_args()
tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": a.w, "height": a.h})
    pg.goto("file://" + os.path.abspath(a.html)); pg.wait_for_timeout(1200)
    n = int(a.dur * a.fps)
    for i in range(n):
        pg.evaluate(f"window.__render({i / a.fps})")
        pg.locator("#stage").screenshot(path=f"{tmp}/f{i:05d}.png")
    b.close()
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i", f"{tmp}/f%05d.png"]
if a.audio: cmd += ["-i", a.audio, "-shortest", "-c:a", "aac", "-b:a", "160k"]
cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", a.out]
subprocess.run(cmd, check=True)
print("ok", a.out)
