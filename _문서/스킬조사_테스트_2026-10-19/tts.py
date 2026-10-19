# -*- coding: utf-8 -*-
import sys, wave, numpy as np, sherpa_onnx
M = "tts/vits-mimic3-ko_KO-kss_low"
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{M}/ko_KO-kss_low.onnx", lexicon="", tokens=f"{M}/tokens.txt",
                                               data_dir=f"{M}/espeak-ng-data"), num_threads=4))
tts = sherpa_onnx.OfflineTts(cfg)
def say(text, out, speed=1.0):
    a = tts.generate(text, sid=0, speed=speed)
    s = (np.array(a.samples) * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(a.sample_rate); w.writeframes(s.tobytes())
    return len(s) / a.sample_rate
if __name__ == "__main__":
    print(say(sys.argv[1], sys.argv[2]), "초")
