# SpeFileParser

`SpeFileParser` 是一个用于从光谱文件名中提取实验参数的 Python 模块。该模块提供了一个函数 `get_spe_info()`，它能够解析符合特定命名规则的光谱文件名，并提取出文件中所包含的光谱仪、激光和实验相关的参数。

## 功能

- 从光谱文件名中提取光谱仪（Spectrometer）、激光（Laser）和实验信息（ExperimentalInfo）等参数。
- 支持光谱文件名格式如：`NPOM150-PIKE0P45-LASER[YSL-w785-p100%-nd220-35.92uW]-PI[1200ms-60um-150i-785c]-TEST[1-2-3]-oiDF-NC23 34.csv`
- 提取的参数包括光谱仪名称、曝光时间、单位，激光设备名称、波长、功率设置等实验相关的信息。

## 安装

该模块可以直接从源代码安装。首先，下载或克隆项目文件。

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

## 依赖

- Python 3.x
- `re` 模块（Python内置）

## 使用

在您的 Python 代码中，您可以使用以下方式导入并使用该模块：
```python
from labtools.spefileparser import get_spe_info

# 示例光谱文件名
spe_file_name = 'NPOM150-PIKE0P45-LASER[YSL-w785-p100%-nd220-35.92uW]-PI[1200ms-60um-150i-785c]-TEST[1-2-3]-oiDF-NC23 34.csv'

# 获取提取的光谱信息
spectrometer, laser, exp_info = get_spe_info(spe_file_name)

# 打印结果
print(spectrometer.devName)  # 打印光谱仪设备名称
print(laser.waveLength)      # 打印激光波长
print(exp_info.sampleName)   # 打印样品名称
```

## 参数

`get_spe_info()` 函数的参数如下：

- **spe_file_name** : 字符串类型，表示光谱文件的文件名。该文件名应符合特定的命名格式（如：`NPOM150-PIKE0P45-LASER[YSL-w785-p100%-nd220-35.92uW]-PI[1200ms-60um-150i-785c]-TEST[1-2-3]-oiDF-NC23 34.csv`）。

## 返回值

该函数返回三个对象，分别为：

1. **Spectrometer** : 包含光谱仪信息，包括设备名称（`devName`）、曝光时间（`expTime`）、单位（`speUnit`）。
2. **Laser** : 包含激光器信息，包括设备名称（`devName`）、波长（`waveLength`）、功率设置（`powerSet1`、`powerSet2`）、功率值（`powerValue`）、功率单位（`powerUnit`）。
3. **ExperimentalInfo** : 包含实验相关信息，包括样品名称（`sampleName`）、实验类型（`speType`）、颗粒ID（`partID`）和颗粒备注（`partNote`）。

## 示例

假设我们有如下文件名：

```css
NPOM150-PIKE0P45-LASER[YSL-w785-p100%-nd220-35.92uW]-PI[1200ms-60um-150i-785c]-TEST[1-2-3]-oiDF-NC23 34.csv
```

调用 `get_spe_info()` 解析后，您可以得到如下信息：

```python
# 示例输出
spectrometer.devName = "PIKE0P45"
spectrometer.expTime = 0.012
spectrometer.speUnit = "nm"

laser.devName = "YSL"
laser.waveLength = 785
laser.powerSet1 = "220"
laser.powerSet2 = 100
laser.powerValue = 35.92
laser.powerUnit = "uW"

exp_info.sampleName = "NPOM150"
exp_info.speType = "oiDF"
exp_info.partID = "NC23"
exp_info.partNote = ""
```

## License

- 该项目是开源的，您可以根据需要进行修改和分发，具体许可协议请参见 [LICENSE]()。

