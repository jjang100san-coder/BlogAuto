# -*- coding: utf-8 -*-
import subprocess, json, re, sys, os, wave
sys.stdout.reconfigure(encoding='utf-8')
O = "out"
lines = ["퇴근하고 바로 갈 수 있는 곳을, 가까운 순으로 세워 봤어.", "출발 지점에서 사십오 킬로미터 안에, 조건에 맞는 후보가 백사십구 곳.", "결국 무봉산으로 정했어. 내가 걸어서 남길 기록이 첫 자료가 돼."]
def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def mp3(wav, out): ff("-i", wav, "-codec:a", "libmp3lame", "-q:a", "3", out)
def lufs(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    return json.loads(r.stderr[r.stderr.rfind("{"):])
def seg_lufs(path, t0, t1):
    r = subprocess.run(["ffmpeg", "-ss", str(t0), "-to", str(t1), "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    return re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]
def dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
def concat(parts, out):
    with open(f"{O}/_list.txt", "w") as f:
        for p in parts: f.write(f"file '{os.path.abspath(p)}'\n")
    ff("-f", "concat", "-safe", "0", "-i", f"{O}/_list.txt", "-c", "copy", out)
parts = []
for i in range(3):
    m = lufs(f"{O}/d{i}g.wav")
    ff("-i", f"{O}/d{i}g.wav", "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true", "-ar", "22050", f"{O}/d{i}n.wav")
    parts += [f"{O}/d{i}n.wav", f"{O}/s.wav"]
concat(parts[:-1], f"{O}/04_perline.wav"); mp3(f"{O}/04_perline.wav", f"{O}/04_음량_보정후_줄마다.mp3")
t = 0
print("| 줄 | 보정 전 | 파일 전체 한 번 | **줄마다 따로** |"); print("|---|---|---|---|")
for i in range(3):
    d = dur(f"{O}/d{i}g.wav")
    print("| %s | %s | %s | **%s** |" % (lines[i][:14] + "…", seg_lufs(f"{O}/04_before.wav", t, t + d), seg_lufs(f"{O}/04_after.wav", t, t + d), seg_lufs(f"{O}/04_perline.wav", t, t + d))); t += d + 0.7
m = lufs(f"{O}/04_perline.wav"); print("| 전체 통합 | -26.1 | -15.5 | **%s** (TP %s) |" % (m['input_i'], m['input_tp']))
