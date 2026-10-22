# voice-clone-gsovits

**GPT-SoVITS v2pro 零样本音色克隆 + F0 基频性别质检** — 解决长句克隆时音色漂移（男声变女声）的稳定方案。

## 为什么用 GPT-SoVITS

| 对比项 | VoxCPM | GPT-SoVITS v2pro |
|--------|--------|------------------|
| 长句稳定性 | 差，易漂性别 | 好，参考音锁音色 |
| 速度（CPU） | 慢（数分钟/条） | 快（23-77s/条） |
| Windows 依赖 | 需手动配 torch | 官方整合包解压即用 |
| 音色控制 | 弱 | 主参考+辅助参考音锁死 |

## 环境准备

1. 下载 GPT-SoVITS v2pro Windows 整合包（约 8GB），解压到任意目录
2. 模型权重放在 `GPT-SoVITS-v2pro-xxxx/GPT_SoVITS/pretrained_models/`
3. 用 `runtime\python.exe` 启动 API：
   ```
   runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -dr 0
   ```
   `-dr 0` = CPU 模式（无独显也可）

## 快速开始

```bash
pip install -r requirements.txt
# 修改 gen_gsovits.py 顶部的参考音路径和旁白文本
python gen_gsovits.py          # 批量生成旁白
python f0_check.py output      # 质检（自动判定男声/女声）
```

## F0 性别质检规则

| F0 中位 | 判定 | 处理 |
|---------|------|------|
| < 160 Hz | 男声 | 通过 |
| 160-175 Hz | 模糊 | 人工试听 |
| > 175 Hz | 女声 | 重试（换种子/参考音） |

## API 调用要点

```json
{
  "text": "旁白文本",
  "text_lang": "zh",
  "ref_audio_path": "主参考.wav",
  "prompt_text": "参考音对应的文本",
  "prompt_lang": "zh",
  "aux_ref_audio_paths": ["辅助1.wav", "辅助2.wav"],
  "aux_ref_text_list": ["辅助1文本", "辅助2文本"],
  "aux_ref_lang_list": ["zh", "zh"],
  "media_type": "wav",
  "seed": -1
}
```

## 脚本说明

| 文件 | 功能 |
|------|------|
| `gen_gsovits.py` | 批量调用 API 生成旁白，失败自动换种子重试 |
| `f0_check.py` | librosa pyin 检测 F0 基频，自动判定男女声 |

## 注意事项

- 长句（>15 字）更容易漂移，拆成短句生成更稳
- 半角括号包裹音色描述，避免模型误读
- 生成速度：CPU 模式每条 23-77 秒，可批量跑

## 许可

MIT
