# -*- coding: utf-8 -*-
import os, subprocess, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from tts import say
O = "out"; os.makedirs(O, exist_ok=True)
def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def mp3(wav, out): ff("-i", wav, "-codec:a", "libmp3lame", "-q:a", "3", out)
def lufs(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rfind("{"):])
    return j
def silence(sec, out): ff("-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", str(sec), out)
def concat(parts, out):
    with open(f"{O}/_list.txt", "w") as f:
        for p in parts: f.write(f"file '{os.path.abspath(p)}'\n")
    ff("-f", "concat", "-safe", "0", "-i", f"{O}/_list.txt", "-c", "copy", out)

if __name__ == "__main__":
    # 1) 「2편에서」 vs 「다음 편에서」
    say("2편에서 계속.", f"{O}/a1.wav"); silence(0.7, f"{O}/s.wav"); say("다음 편에서 계속.", f"{O}/a2.wav")
    concat([f"{O}/a1.wav", f"{O}/s.wav", f"{O}/a2.wav"], f"{O}/01.wav"); mp3(f"{O}/01.wav", f"{O}/01_이편_vs_다음편.mp3")

    # 2) 「사고 재고」 vs 풀어 쓴 문장
    say("유튜브에서 사고 재고 한 영상은, 한 편뿐이었어.", f"{O}/b1.wav")
    say("제품을 직접 사서, 저울에 달아 보고 밟아 보며 비교한 영상은, 한 편뿐이었어.", f"{O}/b2.wav")
    concat([f"{O}/b1.wav", f"{O}/s.wav", f"{O}/b2.wav"], f"{O}/02.wav"); mp3(f"{O}/02.wav", f"{O}/02_사고재고_vs_풀어쓴문장.mp3")

    # 3) 실제 대본 한 줄 (등산스틱 3번째 줄)
    say("여덟 편 중에, 광고 없이 제품을 직접 산 영상은 한 편뿐이었어. 무게를 달고, 밟아 보며 비교했지.", f"{O}/c1.wav")
    mp3(f"{O}/c1.wav", f"{O}/03_실제대본_등산스틱.mp3")

    # 4) 음량 보정 — 무봉산 대본 3줄을 일부러 다른 음량으로
    lines = ["퇴근하고 바로 갈 수 있는 곳을, 가까운 순으로 세워 봤어.",
             "출발 지점에서 사십오 킬로미터 안에, 조건에 맞는 후보가 백사십구 곳.",
             "결국 무봉산으로 정했어. 내가 걸어서 남길 기록이 첫 자료가 돼."]
    gains = ["-2dB", "-16dB", "-7dB"]
    parts = []
    for i, (s, g) in enumerate(zip(lines, gains)):
        say(s, f"{O}/d{i}.wav"); ff("-i", f"{O}/d{i}.wav", "-af", f"volume={g}", f"{O}/d{i}g.wav"); parts += [f"{O}/d{i}g.wav", f"{O}/s.wav"]
    concat(parts[:-1], f"{O}/04_before.wav"); mp3(f"{O}/04_before.wav", f"{O}/04_음량_보정전.mp3")
    m = lufs(f"{O}/04_before.wav")
    ff("-i", f"{O}/04_before.wav", "-af",
       f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=summary",
       "-ar", "22050", f"{O}/04_after.wav")
    m2 = lufs(f"{O}/04_after.wav")
    # 줄마다 통합 음량(보정 전/후)
    def seg_lufs(path, t0, t1):
        r = subprocess.run(["ffmpeg", "-ss", str(t0), "-to", str(t1), "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
        return re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]
    import wave
    def dur(p):
        with wave.open(p) as w: return w.getnframes() / w.getframerate()
    t = 0; rows = []
    for i in range(3):
        d = dur(f"{O}/d{i}g.wav"); rows.append((lines[i][:14] + "…", gains[i], seg_lufs(f"{O}/04_before.wav", t, t + d), seg_lufs(f"{O}/04_after.wav", t, t + d))); t += d + 0.7
    mp3(f"{O}/04_after.wav", f"{O}/04_음량_보정후.mp3")
    print("| 줄 | 일부러 준 차이 | 보정 전 LUFS | 보정 후 LUFS |"); print("|---|---|---|---|")
    for r in rows: print("| %s | %s | %s | %s |" % r)
    print("| **전체 통합** | | **%s** (TP %s) | **%s** (TP %s) |" % (m['input_i'], m['input_tp'], m2['input_i'], m2['input_tp']))
