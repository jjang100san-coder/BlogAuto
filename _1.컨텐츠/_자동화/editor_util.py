# -*- coding: utf-8 -*-
"""에디터 프레임 확보 + 방해 팝업 처리 공용 헬퍼."""
import time

POPUP = ".se-popup-alert-confirm"
BTN_CANCEL = ".se-popup-button-cancel"

def dismiss_restore_popup(fr, log=None):
    """'작성 중인 글이 있습니다' 팝업이 뜨면 [취소]를 눌러 새 글로 시작."""
    try:
        pop = fr.locator(POPUP)
        if pop.count() and pop.first.is_visible():
            txt = (pop.first.inner_text() or "").replace("\n", " ")[:60]
            fr.locator(BTN_CANCEL).first.click()
            time.sleep(1.5)
            if log: log("  팝업 처리(취소=새 글로 시작): %s" % txt)
            return True
    except Exception:
        pass
    return False

def _ready(fr, log=None):
    """이 프레임이 에디터인지 확인하고, 맞으면 팝업까지 처리한다."""
    fr.wait_for_selector(".se-content", timeout=5000)
    dismiss_restore_popup(fr, log)
    if fr.locator(".se-documentTitle").count() == 0:
        return False
    # 팝업이 프레임 확보 직후 뒤늦게 뜨는 경우가 있어 한 번 더 확인
    for _ in range(4):
        time.sleep(1)
        dismiss_restore_popup(fr, log)
    return True


def get_editor_frame(page, timeout=60, log=None):
    """에디터 프레임을 찾는다.

    새 글 쓰기 화면은 에디터가 iframe#mainFrame 안에 있지만,
    발행글 수정 화면(PostWriteForm.naver?...&redirect=Update)에는
    mainFrame 이 아예 없고 최상위 프레임이 곧 에디터다. 둘 다 받는다.
    """
    end, last = time.time() + timeout, None
    while time.time() < end:
        try:                                  # (1) 최상위 프레임이 에디터인 경우
            if page.main_frame.locator(".se-content").count() > 0:
                if _ready(page.main_frame, log):
                    if log: log("  에디터 위치: 최상위 프레임 (수정 화면)")
                    return page.main_frame
        except Exception as e:
            last = e
        try:                                  # (2) mainFrame 안에 있는 경우
            el = page.wait_for_selector("iframe#mainFrame", timeout=5000)
            fr = el.content_frame()
            if fr and _ready(fr, log):
                return fr
        except Exception as e:
            last = e
        time.sleep(1)
    raise RuntimeError("에디터 프레임을 찾지 못했습니다: %r" % last)
