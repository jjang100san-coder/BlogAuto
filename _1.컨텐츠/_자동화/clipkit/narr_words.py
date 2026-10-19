# -*- coding: utf-8 -*-
# 내레이션 단어 시각 → narration\<EP>\nXX.words.json  (2026.10.19)
#   shorts.prep 이 이 파일이 있으면 말 자막을 「비례 배분」이 아니라 실제 말한 시각에 붙인다(없으면 예전대로).
#   faster-whisper 가 있어야 단어 시각이 나온다(stt.words). whisper-cli 뿐이면 아무것도 안 만들고 알린다.
#   python narr_words.py <장면 스크립트.py>        narr_pick 이 고른 nXX.mp3 전부
#   python narr_words.py <narration\EP 폴더>        폴더 안 nXX.mp3 전부
import os, re, sys, glob, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import stt


def main(target):
    if target.endswith('.py'):
        base = os.path.dirname(os.path.abspath(target))
        ep = re.findall(r"build\(\w+, BASE, '([^']+)', '([^']+)'\)", open(target, encoding='utf-8').read())[-1][0]
        nd = os.path.join(base, 'narration', ep)
    else:
        nd = target
    if stt.engine() != 'fw':
        print('단어 시각은 faster-whisper 가 있어야 한다 — python stt.py pull 뒤 다시. (지금 엔진: %s)' % stt.engine()); return
    for f in sorted(glob.glob(os.path.join(nd, 'n[0-9][0-9].mp3'))):
        w = stt.words(f)
        out = f[:-4] + '.words.json'
        json.dump(w, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
        print('%s  %d단어  %s' % (os.path.basename(f), len(w), ' '.join(x[2] for x in w)[:60]))


if __name__ == '__main__':
    main(sys.argv[1])
