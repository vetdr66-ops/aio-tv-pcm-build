#!/usr/bin/env python3
"""Transactional MPV AudioTrack PCM tap patcher. Stages, validates, backs up, then commits."""
from pathlib import Path
import base64, zlib, tempfile, shutil, subprocess, sys, time, re

OLD_PATCH = zlib.decompress(base64.b64decode('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')).decode('utf-8')
GEN_PATCH = zlib.decompress(base64.b64decode('eJzNWW1v2zYQ/u5fwfiDK3m2E7fA2tV1gCxNhwJpEizZsKIoBFqibSKyqIpUHC/NfvvuKFIvlh17ideWHwxL4r3y7rnTaZyIGYmpmoZ8RPgsFokiF3DZaLx7f3pChiQRQpF90qRpwMW+SNU+FZ6+UAn1r3t+syFFmvgM9iJJL2E08BS7VQ6LfBHwaDJspmrcfdV0G42AjUnC4pD6zBORzxwRBh0SsXmHhHTEQvd1g8CahGJEQ5Ix1nd8kUYKRGS3evoSiV39lI/Nhr0h6WcscCWUS0Z+hwd8xk6SRCTOuHmnBd2/Juw2Zr5iAemTGVX+tEPGwCMgd5rV/YCMechIGvlTGk1Y0GtmsnJrjSrGnJIlfTC0YmTj2bNnUiWpr0jszzxFY0+G4NY7zXAW33j29owpGlBFif0z0FtSHqlXHlDTRSho8OnDxZ/exfEH7+rowvtw9Jd3cfTx9Pzorffrx6uTy8+Dxv0AJHZ2IvbFc5A7YRFLqOIieoo+pKnFF8yaqxyF/L0jJWbcJyMhQsIiOgpZkEmuPJFpjAELz6y5uGW/TX7lihzAEVlSAhtZQl70yYgrCQ9AWSKZlKBESZ8eae9XpOQOkIoqtlEDyJLsmd6+1rrayqg8Lr1Q+NfeOGHMaZmz6QWJAOUDl7Rajf9ObTzgVjz0LRXQrnCNe/B5F58/4CFweSU2JVOescLBZ9aixp1NfWfPaICx6EFah9znqqSCPaQOxPdMJAtPJAFLPOp/SXnCXLcADKbSJCIH2UkbrlKJhK1gaxTpWI0QfA6WRCQsZFSC/Y0S+z4khD2OH8PaarYDknn6fCBRNsjCXWvkZCaPRUKcwcA1oINLJ86cSmsnSHEKkS3ST13tykFOoa3ey7cPy9RuJSYLD+e3c7MAm71SHlvGlk9JwwrZFOrZRkfgpgf9UGOrKA83ssVNW7FFQ7Si4DgkcmuZWg3tmjoFCOJxlM7j8BDqGflJn0qLHNy+HGcrrTLKnYvkJWZv3iD5VyAv9t8TFkJdvlvLoBwN/1QoG5WjM87zxSymOkWzUu3NGb0uvFlzxXL4tnJ5nUKNTo1s+RgwuTfmWMn1/cyO+yz5SbPwUpfOQX+T61uBIjZZzsoK3rb/OuRG8IC0TY2u26OX5H+zopB7Po0p+Gxh8aYSrh2dCwPTj0USy2K9u2jjr8k/nbi5al+/kj0jqAZCXZuyj80LOAx6i4VOc9lN0qL6mT5DzXEtdGrDh6XAgmv5SZO2iFPuji5Pz6+84/M/zq5IF3PqcyEJibqH1ls9eySjhWKSHK44onUuzEMAm9QK00wYWOzHC8cGhtmzdLlaD3erypgdjzYfgeOpNfFbBfsjonVFeXsywlcjucJyd7VofWivCO8tEp4MKwwenwkVe3fVhVSYVkpdUeQG1dqSZUFpL1TW4mq5W9hhQpQcrniUsnL1qyv4CLhYFce4NsEGrqdDB65dHiu6wim3Kj/SOe1Y3OZGYsxDxRIeTQiC5spWAn1lX19tHsepnDpZhm/A2dXAavwA5BUYdospxDeT2VmV6G7mKBQJRWASUfDj+vfzahRDnLaribAU5ZJ9SVmkR0JFf2QSZSk/8j+WOH9mc6T8mr4LPWowNqwNc56iqvGpopPtpx2VszMFhQpd5T0UBO/AkxmLsLBkf+QDEQAL2wWz09Oju46ZzZh74oYl41DM3QdHIN9Lq4e5rI9lwHUM4i3CeYuZQT7KWNmILLc/peY+7h5CCzSjCvuII5wKv9OXvZOz4/O3789+896fHP/c/+XFy7LzNWY/HvxzoM/1KnlnV7oWHi4lzySlyWpUtULsUNkT47Fkirwh1PdZjHfGCZ1BaYa+ckZxoIZqHJQLlIVAHLg5Ndg3oL/sx6fyIk2VQAHCkiF5iPjxYCbrYKpAeMsCxCf++aFgNlhvR8dtF87Dn6bRNdS+zFkSOLi1LP2/JXbK0ZNJB1AbhRxwbYtRtV06uVHFYqr1lJxbGu8gmNBZHDIcXpekrIK00gtIbEcqNS/tovVaY7ZTyF01zKupWClOBW3Wk2/tBahEIV2oKQI2kRGN5VSorYqSjS2T7w4VUP06VlIHUwZuKOltB/yaZbHbgn/5Vl6R1k7lv59OmxlVzyzvA6iUS/miPyH25glXLPsgmH0xw4H58ofBGHpW5TTLn2W4FGEWFTF+nSOAcyHPPsOZ3WeCXF5cHhNoe1IG0RFwHyJjzgCzEwbZXdp6ihElwqBruaMkLknApQ+QDnE7WpQ/BBWUVxYd08i4CjYbpEQO7NYPU2Qw52oqUgV63GSbLq4uS3zecjqJhFT26xB5jtQQnHpWT0QULsh8yiKTmZLgRDCf5SOjfwEtsR+G')).decode('utf-8')
RESET_NAME = 'pcm_tap_' + 'reset'
ZERO_INIT = '0' + 'u'
HEAD_ZERO = 'atomic_store_explicit(&pcm_tap.head, ' + '0'
TAIL_ZERO = 'atomic_store_explicit(&pcm_tap.tail, ' + '0'
FILES = ['audio/out/ao.h', 'audio/out/internal.h', 'audio/out/buffer.c', 'audio/out/ao_audiotrack.c', 'libmpv/client.h']

def replace_once(source, old, new, label):
    n = source.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {n}')
    return source.replace(old, new, 1)

def patch_staged(root):
    patch_file = root.parent / '_apply_pts_base.py'
    patch_file.write_text(OLD_PATCH, encoding='utf-8')
    p = subprocess.run([sys.executable, str(patch_file), str(root)], text=True, capture_output=True)
    patch_file.unlink(missing_ok=True)
    if p.returncode:
        raise RuntimeError('Base PTS patch failed; originals untouched.\n' + p.stdout + p.stderr)
    f = root / 'audio/out/ao_audiotrack.c'
    try:
        exec(compile(GEN_PATCH, 'corrected_generation_patch', 'exec'), {'root': root, 'Path': Path})
    except Exception as exc:
        staged_text = f.read_text(encoding='utf-8')
        marker = 'int mpv_pcm_tap_set_enabled'
        pos = staged_text.find(marker)
        if pos >= 0:
            start = max(0, staged_text.rfind('\n', 0, pos - 1) - 1200)
            end = min(len(staged_text), staged_text.find('\n}', pos) + 2 + 500)
            context = staged_text[start:end]
        else:
            context = 'The staged function marker was not found.'
        raise RuntimeError(str(exc) + '\n\n--- STAGED FUNCTION CONTEXT (original files untouched) ---\n' + context) from exc

    s = f.read_text(encoding='utf-8')
    recreate_pattern = re.compile(
        r'(?P<indent>[ \t]*)if \(AudioTrack_Recreate\(ao\) < 0\) \{\s*'
        r'(?P=indent)[ \t]*MP_ERR\(ao, "AudioTrack_Recreate failed\\n"\);\s*'
        r'(?P=indent)\}\s*(?P=indent)pcm_tap_reset\(\);',
        re.MULTILINE)
    def recreate_replacement(match):
        indent = match.group('indent')
        return (indent + 'if (AudioTrack_Recreate(ao) < 0) {\n' +
                indent + '    MP_ERR(ao, "AudioTrack_Recreate failed\\n");\n' +
                indent + '    atomic_fetch_and_explicit(&pcm_tap.state, ~1u, memory_order_acq_rel);\n' +
                indent + '    atomic_store_explicit(&pcm_tap.diagnostic_state, -20, memory_order_release);\n' +
                indent + '} else {\n' +
                indent + '    pcm_tap_advance_generation();\n' +
                indent + '}')
    s, recreate_count = recreate_pattern.subn(recreate_replacement, s, count=1)
    if recreate_count != 1:
        raise RuntimeError('AudioTrack_Recreate staged block did not match safely; originals untouched.')
    f.write_text(s, encoding='utf-8')
    reset_pattern = re.compile(
        r"^static\s+void\s+" + re.escape(RESET_NAME) +
        r"\s*\(\s*void\s*\)\s*\{.*?^\}",
        re.MULTILINE | re.DOTALL)
    reset_match = reset_pattern.search(s)
    if not reset_match:
        raise RuntimeError('Could not locate the complete PCM reset function; originals untouched.')
    old_reset_body = reset_match.group(0)
    required_reset_parts = (
        'atomic_store_explicit(&pcm_tap.head,',
        'atomic_store_explicit(&pcm_tap.tail,',
        'atomic_store_explicit(&pcm_tap.diagnostic_state,',
    )
    if not all(part in old_reset_body for part in required_reset_parts):
        raise RuntimeError('PCM reset function differs from expected base patch; originals untouched.')

    # Convert the verified reset body into a one-time initializer without
    # clearing SPSC queue indices or changing the session generation.
    new_init = old_reset_body
    new_init = new_init.replace(
        'static void ' + RESET_NAME + '(void)',
        'static void pcm_tap_initialize(void)', 1)
    new_init = replace_once(
        new_init,
        '    atomic_store_explicit(&pcm_tap.enabled, false, memory_order_release);',
        '    atomic_fetch_and_explicit(&pcm_tap.state, ~1u, memory_order_acq_rel);',
        'initializer enabled-state conversion')
    new_init = replace_once(
        new_init,
        '    atomic_store_explicit(&pcm_tap.head, 0u, memory_order_relaxed);\n',
        '', 'initializer head preservation')
    new_init = replace_once(
        new_init,
        '    atomic_store_explicit(&pcm_tap.tail, 0u, memory_order_relaxed);\n',
        '', 'initializer tail preservation')
    new_init = replace_once(
        new_init,
        'atomic_is_lock_free(&pcm_tap.enabled)',
        'atomic_is_lock_free(&pcm_tap.state)', 'initializer lock-free state')
    if ('pcm_tap_reset' in new_init or
            'atomic_store_explicit(&pcm_tap.head,' in new_init or
            'atomic_store_explicit(&pcm_tap.tail,' in new_init):
        raise RuntimeError('initializer still contains a queue-index reset; originals untouched.')
    s = s[:reset_match.start()] + new_init + s[reset_match.end():]

    s = replace_once(s, '    ' + RESET_NAME + '();\n    pthread_mutex_init(&p->lock, NULL);',
                     '    pcm_tap_initialize();\n    pthread_mutex_init(&p->lock, NULL);', 'initialization call')
    reset_lines = [line for line in s.splitlines(True) if line.strip() == RESET_NAME + '();']
    if len(reset_lines) != 1:
        raise RuntimeError(f'expected one AO-reset call to convert, found {len(reset_lines)}')
    s = ''.join(
        line.replace(RESET_NAME + '();', 'pcm_tap_advance_generation();')
        if line.strip() == RESET_NAME + '();' else line
        for line in s.splitlines(True)
    )
    if re.search(r'^\s*(?:static\s+void\s+)?' + re.escape(RESET_NAME) + r'\s*(?:\(|;)', s, re.MULTILINE):
        raise RuntimeError('old reset function or call remains')
    generation_helper = '''static void pcm_tap_advance_generation(void)
{
    uint32_t old_state = atomic_load_explicit(&pcm_tap.state, memory_order_acquire);
    for (;;) {
        uint32_t generation = ((old_state >> 1) + 1u) & 0x7fffffffu;
        uint32_t new_state = (generation << 1) | (old_state & 1u);
        if (atomic_compare_exchange_weak_explicit(
                &pcm_tap.state, &old_state, new_state,
                memory_order_acq_rel, memory_order_acquire))
            return;
    }
}

'''
    s = replace_once(
        s,
        'static void uninit_jni(struct ao *ao)',
        generation_helper + 'static void uninit_jni(struct ao *ao)',
        'AO-reset generation helper')
    s = replace_once(
        s,
        '    if ((atomic_load_explicit(&pcm_tap.state, memory_order_acquire) >> 1) !=\n        generation)\n        return;',
        '    uint32_t capture_state = atomic_load_explicit(&pcm_tap.state, memory_order_acquire);\n'
        '    if (!(capture_state & 1u) || (capture_state >> 1) != generation)\n'
        '        return;',
        'capture enabled-and-generation guard')
    f.write_text(s, encoding='utf-8')

    checks = {
        'PTS segment struct': 'AO_READ_DATA_MAX_PTS_SEGMENTS' in (root/'audio/out/ao.h').read_text(encoding='utf-8'),
        'segment-aware buffer reader': 'int ao_read_data_with_segments(' in (root/'audio/out/buffer.c').read_text(encoding='utf-8'),
        'public tap API': 'mpv_pcm_tap_read' in (root/'libmpv/client.h').read_text(encoding='utf-8'),
        'initialize exists once': s.count('static void pcm_tap_initialize(void)') == 1,
        'old reset absent': RESET_NAME not in s,
        'head not reset': HEAD_ZERO not in s,
        'tail not reset': TAIL_ZERO not in s,
        'generation slot': 'uint32_t generation;' in s,
        'generation read filter': 'slot->generation != generation' in s,
        'generation capture guard': '!(capture_state & 1u)' in s,
        'AO reset advances generation': s.count('pcm_tap_advance_generation();') == 2,
        'recreate success advances generation': bool(re.search(
            r'else\s*\{\s*pcm_tap_advance_generation\(\);\s*\}', s)),
        'generation helper exists once': s.count('static void pcm_tap_advance_generation(void)') == 1,
        'generation helper preserves enabled bit': '(old_state & 1u)' in s,
        'pending queue guard': 'if (head != tail)' in s,
        'AudioTrack write capture': 'pcm_tap_capture(ao, p, samples, ret' in s,
        'diagnostic failure': 'diagnostic_state, -20' in s,
    }
    for name, ok in checks.items(): print(('PASS' if ok else 'FAIL') + ' | ' + name)
    failed = [k for k,v in checks.items() if not v]
    if failed: raise RuntimeError('Staging validation failed: ' + ', '.join(failed))

def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python apply_mpv_pcm_tap_fixed_v6.py <MPV_SOURCE_ROOT>')
    source_root = Path(sys.argv[1]).expanduser().resolve()
    if source_root.name != 'mpv-78d43740f52db817d98bcf24fb30a76ab6fa13ff':
        raise SystemExit('رفض التعديل: مسار المصدر لا يطابق مجلد MPV المثبت في مشروعك.')
    for rel in FILES:
        if not (source_root/rel).is_file(): raise SystemExit('ملف مطلوب غير موجود: ' + str(source_root/rel))
    parent = source_root.parent
    with tempfile.TemporaryDirectory(prefix='mpv_pcm_tap_stage_', dir=parent) as td:
        stage = Path(td)/source_root.name
        for rel in FILES:
            dst = stage/rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source_root/rel, dst)
        patch_staged(stage)
        backup = parent/('mpv_pcm_tap_backup_' + time.strftime('%Y%m%d_%H%M%S'))
        backup.mkdir()
        committed = []
        try:
            for rel in FILES:
                bak = backup/rel; bak.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source_root/rel, bak)
            for rel in FILES:
                target = source_root/rel
                temp_target = target.with_name(target.name + '.pcm_tap_tmp')
                shutil.copy2(stage/rel, temp_target); temp_target.replace(target); committed.append(rel)
        except Exception:
            for rel in committed: shutil.copy2(backup/rel, source_root/rel)
            raise
    print('\nSUCCESS: PCM tap patch committed.')
    print('Backup:', backup)
    for rel in FILES: print(' -', rel)
    print('Queue head/tail are never reset; generation filtering is enabled.')

if __name__ == '__main__': main()