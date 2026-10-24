"""Edit, master and encode every deliverable from the rendered frames and audio stems.

usage: python3 -I tools/deliver.py <brand-film dir>
expects out/frames/{main,shock,curiosity}/NNNNN.png and out/audio/{variant}/{music,sfx}.wav
"""
import json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image
from scipy.io import wavfile

ROOT = os.path.abspath(sys.argv[1])
OUT = os.path.join(ROOT, 'out')
DEL = os.path.join(ROOT, 'deliverables')
TMP = os.path.join(OUT, 'tmp')
FPS = 60
SR = 48000
NAME = 'DevEraXTech_EngineeredExcellence'

# Cut lists in seconds. Joins fall on scene boundaries or on static brand frames.
CUT_15 = [(0.0, 6.0), (24.3, 28.0), (29.0, 31.3), (33.0, 36.0)]
CUT_06 = [(30.0, 36.0)]
FULL = [(0.0, 36.0)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:])
        raise SystemExit(f'failed: {" ".join(cmd[:6])} ...')
    return r


def read_wav(p):
    sr, x = wavfile.read(p)
    assert sr == SR
    return x.astype(np.float64) / (2 ** 31 - 1)


def assemble_audio(x, segs, xf=0.02):
    """Concatenate segments with short equal-power crossfades at each join."""
    out = None
    n = int(xf * SR)
    for a, b in segs:
        s = x[int(a * SR):int(b * SR)].copy()
        if out is None:
            out = s
            continue
        fade = np.sin(np.linspace(0, np.pi / 2, n))[:, None]
        out[-n:] = out[-n:] * fade[::-1] + s[:n] * fade
        out = np.concatenate([out, s[n:]])
    return out


def master(x, path, target=-14.0):
    """Glue compression, true-peak limiting and two-pass EBU R128 loudness to -14 LUFS."""
    raw = os.path.join(TMP, 'raw.wav')
    wavfile.write(raw, SR, (np.clip(x, -1, 1) * (2 ** 31 - 1)).astype(np.int32))
    chain = 'acompressor=threshold=-22dB:ratio=2:attack=15:release=180:makeup=2dB'
    r = run(['ffmpeg', '-hide_banner', '-y', '-i', raw, '-af',
             f'{chain},loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    j = r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1]
    m = json.loads(j)
    ln = (f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(['ffmpeg', '-hide_banner', '-y', '-i', raw, '-af', f'{chain},{ln},alimiter=limit=0.84:level=false,aresample=48000',
         '-c:a', 'pcm_s24le', path])
    return path


def stage_frames(variant_dirs, segs, name):
    """Symlink (or blend) frames for an edit into one sequential directory."""
    d = os.path.join(TMP, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    k = 0
    prev_last = None
    for si, (a, b) in enumerate(segs):
        f0, f1 = int(round(a * FPS)), int(round(b * FPS))
        for f in range(f0, f1):
            src = variant_dirs(f)
            dst = os.path.join(d, f'{k:05d}.png')
            # 4-frame dissolve where an edit joins two near-identical brand frames
            if prev_last is not None and f - f0 < 4 and a >= 28:
                w = (f - f0 + 1) / 5
                im = Image.blend(Image.open(prev_last).convert('RGB'), Image.open(src).convert('RGB'), w)
                im.save(dst)
            else:
                os.symlink(src, dst)
            k += 1
        prev_last = variant_dirs(f1 - 1)
    return d


def frames_main(f):
    return os.path.join(OUT, 'frames', 'main', f'{f:05d}.png')


def frames_alt(variant):
    def pick(f):
        return os.path.join(OUT, 'frames', variant if f < 180 else 'main', f'{f:05d}.png')
    return pick


def encode(frames_dir, audio, out, profile):
    """profile: master | tiktok | instagram | preview"""
    v_in = ['-framerate', str(FPS), '-i', os.path.join(frames_dir, '%05d.png')]
    a_in = ['-i', audio] if audio else ['-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=stereo']
    common = ['-map', '0:v', '-map', '1:a', '-shortest', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709']
    if profile == 'master':
        v = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '8', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-tune', 'film', '-x264-params', 'keyint=60']
        a = ['-c:a', 'pcm_s24le']
    elif profile == 'tiktok':
        v = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.2', '-tune', 'film', '-g', '60']
        a = ['-c:a', 'aac', '-b:a', '320k', '-ar', '48000']
    elif profile == 'instagram':
        v = ['-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-maxrate', '8M', '-bufsize', '16M', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.1', '-tune', 'film', '-g', '30']
        a = ['-c:a', 'aac', '-b:a', '256k', '-ar', '48000']
    else:
        v = ['-vf', 'scale=540:960:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-pix_fmt', 'yuv420p', '-g', '60']
        a = ['-c:a', 'aac', '-b:a', '160k']
    mov = ['-movflags', '+faststart'] if out.endswith('.mp4') else []
    run(['ffmpeg', '-hide_banner', '-y', *v_in, *a_in, *common, *v, *a, *mov, out])
    return out


def main():
    os.makedirs(TMP, exist_ok=True)
    for sub in ('master', 'tiktok', 'instagram', 'openings', 'thumbnails', 'audio'):
        os.makedirs(os.path.join(DEL, sub), exist_ok=True)
    A = lambda v, s: read_wav(os.path.join(OUT, 'audio', v, f'{s}.wav'))
    mix = {v: A(v, 'music') + A(v, 'sfx') for v in ('main', 'shock', 'curiosity')}
    sfx = {v: A(v, 'sfx') for v in ('main',)}

    print('mastering audio')
    au = lambda n: os.path.join(DEL, 'audio', n)
    master(assemble_audio(mix['main'], FULL), au(f'{NAME}_36s_music+sfx_master.wav'))
    master(assemble_audio(sfx['main'], FULL), au(f'{NAME}_36s_sfx-only_master.wav'))
    master(assemble_audio(mix['main'], CUT_15), au(f'{NAME}_15s_music+sfx_master.wav'))
    master(assemble_audio(mix['main'], CUT_06), au(f'{NAME}_06s_sonic-identity_master.wav'))
    for v in ('shock', 'curiosity'):
        master(assemble_audio(mix[v], FULL), os.path.join(TMP, f'{v}_full.wav'))
        master(assemble_audio(mix[v], [(0, 3.0)]), os.path.join(TMP, f'{v}_3s.wav'))
    # keep the unmastered stems too, for any later re-mix
    for v in ('main',):
        for s in ('music', 'sfx'):
            shutil.copy(os.path.join(OUT, 'audio', v, f'{s}.wav'), au(f'{NAME}_36s_stem_{s}.wav'))

    print('staging edits')
    full = stage_frames(frames_main, FULL, 'full')
    c15 = stage_frames(frames_main, CUT_15, 'c15')
    c06 = stage_frames(frames_main, CUT_06, 'c06')

    print('encoding main film')
    mpath = os.path.join(DEL, 'master', f'{NAME}_36s_1080x1920_60p_master.mov')
    if not os.path.exists(mpath) or '--force-master' in sys.argv:
        encode(full, au(f'{NAME}_36s_music+sfx_master.wav'), mpath, 'master')
    for prof, fold in (('tiktok', 'tiktok'), ('instagram', 'instagram')):
        tag = '60p' if prof == 'tiktok' else '30p'
        encode(full, au(f'{NAME}_36s_music+sfx_master.wav'), os.path.join(DEL, fold, f'{NAME}_36s_{prof}_{tag}_music.mp4'), prof)
        encode(full, au(f'{NAME}_36s_sfx-only_master.wav'), os.path.join(DEL, fold, f'{NAME}_36s_{prof}_{tag}_sfx-only.mp4'), prof)
        encode(full, None, os.path.join(DEL, fold, f'{NAME}_36s_{prof}_{tag}_muted-safe.mp4'), prof)
        encode(c15, au(f'{NAME}_15s_music+sfx_master.wav'), os.path.join(DEL, fold, f'{NAME}_15s_{prof}_{tag}.mp4'), prof)
        encode(c06, au(f'{NAME}_06s_sonic-identity_master.wav'), os.path.join(DEL, fold, f'{NAME}_06s_{prof}_{tag}.mp4'), prof)

    print('encoding alternate openings')
    for v in ('shock', 'curiosity'):
        d3 = stage_frames(frames_alt(v), [(0, 3.0)], f'{v}3')
        encode(d3, os.path.join(TMP, f'{v}_3s.wav'), os.path.join(DEL, 'openings', f'{NAME}_alt-opening-{v}_3s_60p.mp4'), 'tiktok')
        df = stage_frames(frames_alt(v), FULL, f'{v}full')
        encode(df, os.path.join(TMP, f'{v}_full.wav'), os.path.join(DEL, 'openings', f'{NAME}_36s_alt-opening-{v}_tiktok_60p.mp4'), 'tiktok')

    print('review copy')
    encode(full, au(f'{NAME}_36s_music+sfx_master.wav'), os.path.join(DEL, f'{NAME}_36s_review_540x960.mp4'), 'preview')
    shutil.rmtree(TMP, ignore_errors=True)
    print('done')


if __name__ == '__main__':
    main()
