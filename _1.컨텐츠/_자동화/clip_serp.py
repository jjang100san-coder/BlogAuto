# 네이버 클립 검색 상위 카드 수집 — 잘 나가는 클립의 공통점 조사용(10/10)
# 사용: python clip_serp.py <저장폴더> "검색어1" "검색어2" ...
#   → <저장폴더>\clip_serp.json (검색어별 카드: 순위·제목·채널·올린 때·조회수·커버 주소) + thumbs\<검색어>_<순위>.jpg(커버)
# 검색 결과 페이지(search.naver.com 클립 탭)를 그대로 읽는다. 로그인·API 키 불필요. 검색어 사이 1.5초 쉼
import sys, os, re, json, time, html, urllib.request, urllib.parse

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read().decode('utf-8', 'ignore')


def views(s):
    """「조회 1.2만」→12000, 「조회 3,174」→3174."""
    m = re.search(r'조회\s*([\d.,]+)\s*(만|천)?', s)
    if not m:
        return None
    v = float(m.group(1).replace(',', ''))
    return int(v * {'만': 10000, '천': 1000}.get(m.group(2), 1))


def parse(h):
    cards = []
    for blk in re.split(r'data-template-id="clipItem"', h)[1:]:
        mid = re.search(r'data-media-id="([0-9A-F]{20,})"', blk)
        title = re.search(r'sds-comps-text-ellipsis-2[^"]*"[^>]*>(.*?)</span>', blk, re.S)
        chan = re.search(r'sds-comps-text-ellipsis-1 sds-comps-text-type-caption[^"]*"[^>]*>(.*?)</span>', blk, re.S)
        age = re.search(r'>(\d+\s*(?:분|시간|일|주|개월|년)\s*전|\d{4}\.\d{2}\.\d{2}\.?)<', blk)
        thumb = re.search(r'<img[^>]+src="(https://search\.pstatic\.net/common/\?src=[^"]+)"[^>]*>', blk)
        dur = re.search(r'>(\d{1,2}:\d{2})<', blk)
        clean = lambda x: html.unescape(re.sub('<[^>]+>', '', x)).strip() if x else ''
        cards.append(dict(media_id=mid.group(1) if mid else '', title=clean(title.group(1) if title else ''),
                          channel=clean(chan.group(1) if chan else ''), age=age.group(1) if age else '',
                          views=views(clean(blk)), duration=dur.group(1) if dur else '',
                          thumb=html.unescape(thumb.group(1)) if thumb else ''))
    # 같은 영상이 두 번 잡히면 하나로
    seen, out = set(), []
    for c in cards:
        if c['media_id'] and c['media_id'] not in seen:
            seen.add(c['media_id']); out.append(c)
    return out


def main(dest, queries):
    os.makedirs(os.path.join(dest, 'thumbs'), exist_ok=True)
    res = {}
    for q in queries:
        h = get('https://search.naver.com/search.naver?ssc=tab.clip.all&query=' + urllib.parse.quote(q))
        cards = parse(h)
        for i, c in enumerate(cards[:20]):
            c['rank'] = i + 1
            if c['thumb']:
                f = os.path.join(dest, 'thumbs', '%s_%02d.jpg' % (re.sub(r'\W', '', q), i + 1))
                try:
                    u = re.sub(r'&type=[^&]+', '', c['thumb'])   # 큰 원본
                    open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read())
                    c['thumb_file'] = f
                except Exception as e:
                    c['thumb_err'] = str(e)
        res[q] = cards[:20]
        print('%s  카드 %d개  조회수 있는 것 %d개' % (q, len(cards), sum(1 for c in cards if c['views'])))
        time.sleep(1.5)
    json.dump(res, open(os.path.join(dest, 'clip_serp.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
