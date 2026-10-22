# -*- coding: utf-8 -*-
"""GPT-SoVITS v2pro 批量旁白生成脚本
用法: python gen_gsovits.py
前提: GPT-SoVITS API 已在 127.0.0.1:9880 启动
"""
import requests, json, time, os, wave

API = "http://127.0.0.1:9880/tts"
REF_AUDIO = r"主参考音.wav"          # 已验收的同音色参考
REF_TEXT = "参考音对应的文本"
AUX = [
    (r"辅助1.wav", "辅助1文本"),
    (r"辅助2.wav", "辅助2文本"),
]
OUT_DIR = r"output"
os.makedirs(OUT_DIR, exist_ok=True)

NARRATIONS = [
    ("镜1", "1931年，九一八事变，华北告急。"),
    ("镜2", "1933年2月，13427箱文物，分五批，秘密装箱。"),
    # ... 在此添加所有镜的 (名称, 文本)
]

def generate(name, text, retries=3):
    for seed in range(retries):
        payload = {
            "text": text,
            "text_lang": "zh",
            "ref_audio_path": REF_AUDIO,
            "prompt_text": REF_TEXT,
            "prompt_lang": "zh",
            "aux_ref_audio_paths": [a[0] for a in AUX],
            "aux_ref_text_list": [a[1] for a in AUX],
            "aux_ref_lang_list": ["zh"] * len(AUX),
            "media_type": "wav",
            "seed": seed,
        }
        r = requests.post(API, json=payload, timeout=600)
        if r.status_code == 200 and len(r.content) > 1000:
            path = os.path.join(OUT_DIR, f"{name}.wav")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"OK {name} seed={seed} size={len(r.content)}")
            return path
        print(f"RETRY {name} seed={seed} status={r.status_code}")
    return None

# 批量生成
for name, text in NARRATIONS:
    out = generate(name, text)
    if not out:
        print(f"FAIL {name}")
print("GEN_DONE")
