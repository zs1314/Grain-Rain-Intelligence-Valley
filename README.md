# Grain Rain Intelligence Valley

一个面向「农业气象与降雨决策」的小型 Python 工程模板。这个仓库从空白初始化为**可运行、可测试、可扩展**的代码库，包含：

- 清晰的项目结构（`src/`、`tests/`、文档与示例数据）。
- 可复用的降雨分析核心逻辑（统计、趋势判断、风险等级）。
- 面向命令行的入口（读取 CSV，输出分析报告）。
- 自动化测试与开发工具配置（`pytest`、`ruff`、`mypy`）。

## 功能概览

### 1) 基础统计
- 样本数量、总降雨量、均值、中位数、最大值、最小值。

### 2) 趋势分析
- 根据首尾区间均值判断降雨趋势：`increasing` / `decreasing` / `stable`。

### 3) 风险评估
- 结合平均降雨与趋势，给出风险级别：`low` / `medium` / `high`。

### 4) 作物建议
- 基于风险级别给出建议策略，辅助后续业务扩展。

## 项目结构

```text
.
├── README.md
├── pyproject.toml
├── src/
│   └── grain_rain_intelligence_valley/
│       ├── __init__.py
│       ├── analytics.py
│       └── cli.py
└── tests/
    └── test_analytics.py
```

## 快速开始

### 环境要求
- Python 3.11+

### 安装依赖（开发模式）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 运行测试

```bash
pytest
```

### 命令行使用

准备一个 `rainfall.csv`：

```csv
day,rainfall_mm
1,12.4
2,9.8
3,10.1
4,15.2
5,18.0
```

运行分析：

```bash
griv-analyze rainfall.csv
```

示例输出：

```json
{
  "count": 5,
  "total": 65.5,
  "mean": 13.1,
  "median": 12.4,
  "minimum": 9.8,
  "maximum": 18.0,
  "trend": "increasing",
  "risk": "medium",
  "recommendation": "建议优化排水并关注短期强降雨预警。"
}
```

## 开发命令

```bash
ruff check .
ruff format .
mypy src
pytest
```

## 后续可扩展方向

- 接入真实气象 API 进行实时数据分析。
- 增加季节性分解、异常检测与更细粒度风险模型。
- 支持 Web API（FastAPI）和可视化仪表盘。

## 许可证

MIT
