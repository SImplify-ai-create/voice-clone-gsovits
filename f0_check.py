# -*- coding: utf-8 -*-
"""F0 基频性别质检
判定: F0中位 <160Hz=男, >175Hz=女, 中间=模糊需人工试听
用法: python f0_check.py <音频目录或单个wav>
"""
import sys, os, glob, warnings
import numpy as np
import librosa

warnings.filterwarnings("ignore")

def f0_median(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    if len(y) < sr * 0.5:
        return None  # 过短/无声
    f0, _, _ = librosa.pyin(y, fmin=50, fmax=400, sr=sr)
    f0 = f0[~np.isnan(f0)]
    return float(np.median(f0)) if len(f0) > 10 else None

def judge(f0):
    if f0 is None:
        return "无声段"
    if f0 < 160:
        return "男"
    if f0 > 175:
        return "女"
    return "模糊"

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    files = glob.glob(os.path.join(target, "*.wav")) if os.path.isdir(target) else [target]
    print(f"{'文件':<30} {'F0中位':>8} {'判定'}")
    for f in sorted(files):
        f0 = f0_median(f)
        name = os.path.basename(f)
        if f0 is None:
            print(f"{name:<30} {'—':>8} 无声段")
        else:
            print(f"{name:<30} {f0:>7.0f}Hz {judge(f0)}")
    print("===== F0_DONE =====")

if __name__ == "__main__":
    main()
