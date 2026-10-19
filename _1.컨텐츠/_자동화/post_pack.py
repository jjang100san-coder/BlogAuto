# 클립 「게시물」 꾸러미를 폰으로 한 번에 옮기기 좋게 모은다 (10/8, 갤럭시 + 휴대폰과 연결/Quick Share)
#
# 사용:  python post_pack.py <클립폴더\post> [<클립폴더\post> ...]
#   → Blog\_오늘의게시물\<yymmdd>-<n>\<순번>_<제목>\ 에  (부를 때마다 n 이 1,2,3… 새 묶음)
#       1-1.jpg … 1-N.jpg, 2-1.jpg …  (꾸러미 번호-사진 순서, 4:5, 위치정보 등 EXIF 제거, 「찍은 시각」= 꾸러미마다 2099-12-31·12-30… 날짜, 사진은 1분씩 거꾸로 → 갤러리 맨 위에 꾸러미별 날짜 칸)
#       1-게시물.txt (앱에 붙여 넣을 글 + 맨 아래 장소 태그·AI 설정 메모 — 따로 태그 파일 없음)
#   폴더째 폰으로 보내면 끝. 폰에서는 앱 → 게시물 만들기 → 갤러리 맨 위 사진부터 차례로 누르고 글 붙여넣기.
#
# 원본 꾸러미(post 폴더) 규칙: 01_*.jpg ~ 0N_*.jpg 순서대로, 게시물.txt 하나. 영상(.mp4)은 옮기지 않는다(클립에 이미 있음).
import os, sys, glob, shutil, datetime as dt
from PIL import Image, ImageOps

BLOG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT_ROOT = os.path.join(BLOG, '_오늘의게시물')


def pack_time(pack_no, photo_no):
    """사진에 넣을 「찍은 시각」 — 꾸러미마다 다른 먼 미래 날짜(1번 = 2099-12-31, 2번 = 12-30 …), 사진은 1분씩 거꾸로.
    갤럭시 갤러리는 찍은 시각으로 날짜별로 묶어 최근 것을 위에 둔다 → 맨 위에 꾸러미별 날짜 칸이 생기고 그 안에 1→N 순서.
    (10/8: 만든 시각 근처로 넣었더니 직접 찍은 사진과 섞이고 자정을 넘긴 것은 「오늘」로 갈렸다)"""
    day = dt.datetime(2099, 12, 31, 23, 59, 0) - dt.timedelta(days=pack_no - 1)
    return day - dt.timedelta(minutes=photo_no - 1)


def title_of(post_dir):
    # <글폴더>\clip\post → 글폴더 이름에서 날짜를 뗀 부분
    name = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(post_dir))))
    return name.split('_', 1)[1] if '_' in name else name


def pack(post_dirs):
    today = dt.datetime.now()
    # 보낼 때마다 새 묶음 폴더: <yymmdd>-1, -2, -3 …(10/8 사용자 규칙 — 이미 보낸·게시한 묶음과 섞이지 않게)
    os.makedirs(OUT_ROOT, exist_ok=True)
    stem = today.strftime('%y%m%d')
    used = [int(d.split('-')[1]) for d in os.listdir(OUT_ROOT) if d.startswith(stem + '-') and d.split('-')[1].isdigit()]
    day_dir = os.path.join(OUT_ROOT, '%s-%d' % (stem, max(used, default=0) + 1))
    os.makedirs(day_dir)
    start = 1
    base_time = today
    for k, pd in enumerate(post_dirs):
        out = os.path.join(day_dir, '%02d_%s' % (start + k, title_of(pd)))
        os.makedirs(out, exist_ok=True)
        pics = sorted(f for f in glob.glob(os.path.join(pd, '*.jpg')) + glob.glob(os.path.join(pd, '*.png')))
        for i, f in enumerate(pics):
            im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
            if im.size != (1080, 1350):
                im = ImageOps.fit(im, (1080, 1350), centering=(0.5, 0.0))
            t = pack_time(start + k, i + 1)
            exif = Image.Exif()
            stamp = t.strftime('%Y:%m:%d %H:%M:%S')
            exif[0x0132] = stamp                    # DateTime
            exif.get_ifd(0x8769)[0x9003] = stamp    # DateTimeOriginal (찍은 시각)
            exif.get_ifd(0x8769)[0x9004] = stamp
            # 파일 이름 = <꾸러미 번호>-<사진 순서> (1-1, 1-2 … 2-1 …, 10/8 사용자 규칙 — 폰에서 꾸러미끼리 안 섞이게)
            p = os.path.join(out, '%d-%d.jpg' % (start + k, i + 1))
            im.save(p, quality=92, exif=exif)       # 원본 EXIF(위치정보 포함)는 버린다
            ts = t.timestamp(); os.utime(p, (ts, ts))
        # 글 하나로: 게시물.txt 맨 아래에 태그.txt(장소 정보태그·AI 활용 설정 메모)를 붙인다 — 따로 열기 번거롭다(10/8 사용자),
        # 사용자가 앱에 붙여 넣은 뒤 그 메모 줄은 보고 지운다
        src = os.path.join(pd, '게시물.txt')
        if os.path.exists(src):
            body = open(src, encoding='utf-8').read().rstrip('\n') + '\n'
            memo = os.path.join(pd, '태그.txt')
            if os.path.exists(memo):
                body += '\n────── 올릴 때 확인 후 지우기 ──────\n' + open(memo, encoding='utf-8').read().rstrip('\n') + '\n'
            open(os.path.join(out, '%d-게시물.txt' % (start + k)), 'w', encoding='utf-8').write(body)
        print('꾸러미', out, '사진 %d장' % len(pics))
    print('\n폰으로 보낼 폴더:', day_dir)
    return day_dir


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__ if __doc__ else '사용: python post_pack.py <post폴더> ...')
    pack(sys.argv[1:])
