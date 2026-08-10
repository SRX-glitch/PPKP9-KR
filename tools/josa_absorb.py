# -*- coding: utf-8 -*-
"""이름 뒤에 남는 1바이트 일본어 조사를 «앞 이름의 한국어 받침»으로 골라 흡수한다.

왜 필요한가
-----------
사용자가 「우리빅토리즈**は**」「곤타（곤다）**だ、**」처럼 한국어 문장에 일본어 조사가
붙어 나오는 것을 지적했다(세션41·43). 구조는 이렇다:

    <F808> 이름 <F809> は          ← 이름은 스크립트 안 «정적 리터럴», 조사는 1바이트 런

`build_kr` 의 `absorb` 가 이미 이 일을 한다 — 조사를 이름의 리전 엔트리 끝에 붙이고
스크립트의 조사 바이트를 0x00 으로 지운다. 한국어 조사는 **앞 음절의 받침**으로 갈리는데
그 앞 음절이 우리가 번역한 이름이므로 **빌드 시점에 결정된다**(훅이 필요 없다).

⛔ 그런데 그 `absorb` 는 **오버레이28(파일 25)에만** 걸려 있었다. `lines` 가
`survey/ov28/dialogue_runs.tsv` 이고 오프셋 기준이 `OV_FILE_START` 라서다.
파일 4/27(side_region)·30(tail_region)은 같은 구조를 갖고도 아무도 흡수하지 않았다.

실측(세션43, 정본 폭 표): 이름 삽입 뒤 조사 전용 런 939개 중 **F8 09(정적 이름) 뒤가
246개** — 이게 이 모듈이 처리하는 모집단이다. 나머지 10개는 `F8 07`(스탯 인덱스, 파일 8)
뒤라 앞 요소가 런타임에 정해지므로 여기서는 손대지 않는다.

⛔ 「に」「で」「へ」는 일부러 제외한다 — 「に」는 장소면 에, 사람이면 에게인데 바이트
스트림에 그 구분이 없다. 틀린 조사는 일본어보다 나쁘다(`build_kr._JOSA` 와 같은 규칙).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

# build_kr._JOSA 와 같은 표. 한쪽만 고치면 파일마다 조사가 갈리므로 여기서 다시 쓰지 말고
# 필요하면 양쪽을 함께 고칠 것.
JOSA = {"は": ("은", "는"), "が": ("이", "가"), "を": ("을", "를"),
        "と": ("과", "와"), "も": ("도", "도"), "の": ("의", "의"),
        "や": ("이랑", "랑")}


def pick(ko_name, jp_particle):
    """`ko_name` 뒤에 붙일 한국어 조사, 판단할 수 없으면 None."""
    pair = JOSA.get(jp_particle)
    if not pair or not ko_name:
        return None
    last = ko_name.rstrip()[-1:]
    if not last or not (0xAC00 <= ord(last) <= 0xD7A3):
        return None                     # 한글 음절이 아니면 받침을 못 읽는다
    return pair[0] if (ord(last) - 0xAC00) % 28 else pair[1]


def runtime_particle_sites(pristine, lo, hi, widths):
    """[(offset, byte, jp)] — 앞 요소가 **런타임에 정해지는** 1바이트 조사 자리.

    `<F807 스탯인덱스> 「が」 <F86A 숫자> 「上がった」` 꼴의 상태 증감 줄이다. 사용자가
    「파워가 ５감소」로 지적한 그 자리이며, 세션43이 F8 07 의 피연산자가 `17 aa`/`02 9e`
    **두 값뿐**임을 확인했다 — 스탯별 상수가 아니라 변수 슬롯이므로 어느 라벨이 앞에
    올지 빌드 시점에 알 수 없고, 따라서 은/는·이/가를 정적으로 고를 수 없다.

    ⇒ 사용자 결정(세션43): **조사를 지운다.** 「힘 ５ 감소」는 게임 수치 표시로 자연스러운
    한국어이고, 10곳을 위해 render_char 훅 + 받침 비트맵(512B) + 폰트 배정 제약을 들이는
    것보다 안전하다. 0x00 은 엔진 자신의 좁은 공백이라 새 코드가 필요 없다.
    """
    bare = {int(k): v for k, v in widths["bare"].items()}
    f8 = {int(k): v for k, v in widths["f8"].items() if v}
    out, i, last = [], lo, None
    while i < hi - 1:
        b = pristine[i]
        if b == 0:
            i += 1
            last = None
            continue
        if b >= 0xF8:
            if b == 0xF8:
                last = pristine[i + 1]
                i += f8.get(pristine[i + 1], 2)
            else:
                last = None
                i += bare.get(b, 1)
            continue
        st, chars = i, []
        while i < hi:
            c = pristine[i]
            if c == 0 or c >= 0xF8:
                break
            cc, nxt = P.bytes_to_cc(pristine, i)
            ch = P.CC2CH.get(cc)
            if ch is None:
                break
            chars.append(ch)
            i = nxt
        t = "".join(chars)
        # 딱 «1바이트짜리 조사 하나»만. 두 글자 이상이면 문장 조각일 수 있어 손대지 않는다.
        if last == 0x07 and i - st == 1 and t in JOSA:
            out.append((st, pristine[st], t))
        if i == st:
            i += 1
    return out


def blank_runtime_particles(rom, fid, pristine, widths, verbose=True):
    """`runtime_particle_sites` 를 라이브 ROM 에서 0x00 으로 지운다.

    게이트 셋을 통과한 자리만 쓴다:
      ① 원본에서 그 바이트가 기록된 조사와 같아야 한다(다른 패스가 이미 손댔으면 건너뛴다)
      ② 라이브 바이트도 아직 그 조사여야 한다
      ③ ⛔ 세션29 세이브 파손 규칙: 겹치는 정렬 u32 가 오버레이를 가리키면 포인터 배열이다
    """
    import expand_overlay as XO
    fatp = int.from_bytes(pristine[0x48:0x4C], "little")
    plo = int.from_bytes(pristine[fatp + fid * 8:fatp + fid * 8 + 4], "little")
    phi = int.from_bytes(pristine[fatp + fid * 8 + 4:fatp + fid * 8 + 8], "little")
    fatl = int.from_bytes(rom[0x48:0x4C], "little")
    llo = int.from_bytes(rom[fatl + fid * 8:fatl + fid * 8 + 4], "little")
    info = XO.overlay_of_file(bytes(rom), fid)
    ram, size = (info[2], info[3]) if info else (0, 0)
    n = refused = 0
    for off, byte, jp in runtime_particle_sites(pristine, plo, phi, widths):
        live = off - plo + llo
        if rom[live] != byte:
            continue                    # 이미 다른 패스가 바꿨다
        a = live & ~3
        if ram and (ram <= int.from_bytes(rom[a:a + 4], "little") < ram + size):
            refused += 1                # 포인터 배열로 보인다 — 건드리지 않는다
            continue
        rom[live] = 0x00
        n += 1
    if verbose and (n or refused):
        print(f"  file {fid}: {n} runtime particles blanked"
              + (f", {refused} refused (pointer array)" if refused else ""))
    return {"blanked": n, "refused": refused}


def sites(rom, lo, hi, tr):
    """{이름 런 오프셋: (한국어 조사, 조사 오프셋, 일본어 이름, 이름 바이트수, 한국어 이름)}.

    `rom` 은 **원본(pristine)**, `tr` 은 {일본어 런: 한국어} 이다. 판정은 전부
    원본 바이트에서 하고, 실제 쓰기는 호출자가 라이브 오프셋으로 한다.
    """
    out = {}
    i = lo
    while i < hi - 4:
        # `F8 08` 로 열리는 이름 삽입만 본다
        if rom[i] != 0xF8 or rom[i + 1] != 0x08:
            i += 1
            continue
        j = i + 2
        chars = []
        while j < hi:
            c = rom[j]
            if c == 0 or c >= 0xF8:
                break
            cc, nxt = P.bytes_to_cc(rom, j)
            ch = P.CC2CH.get(cc)
            if ch is None:
                break
            chars.append(ch)
            j = nxt
        name = "".join(chars)
        # 닫기가 바로 뒤에 있어야 이름이다
        if not name or rom[j:j + 2] != b"\xf8\x09":
            i += 2
            continue
        q = j + 2
        pb = rom[q] if q < hi else 0
        # 1바이트 charcode 만(2바이트 리드 0xE8~0xF7 과 종결 0x00 은 제외)
        if pb == 0 or pb >= 0xE8:
            i = j + 2
            continue
        nxt_b = rom[q + 1] if q + 1 < hi else 0
        if nxt_b != 0 and nxt_b < 0xF8:
            i = j + 2
            continue                    # 조사 런이 1바이트보다 길다 — 통째로 번역 대상
        ko = tr.get(name)
        pko = pick(ko, P.CC2CH.get(pb - 1))
        if pko:
            # 이름 런의 «텍스트» 시작 오프셋을 키로. budget 은 원본 런의 바이트 수라
            # 호출자가 리다이렉트 이스케이프가 들어가는지 바로 판단할 수 있다.
            out[i + 2] = (pko, q, name, j - (i + 2), ko)
        i = j + 2
    return out
