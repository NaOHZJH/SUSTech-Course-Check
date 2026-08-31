# CAS_Auto_Login 南科大选课辅助工具

自动登录南方科技大学 CAS 统一认证系统,查询已选课程信息,并导出 Excel 课程表。

## 功能特性

- 🔑 模拟 CAS 登录(自动获取 `execution` 参数并提交凭据)
- 📚 查询当前学期已选课程(容量 / 已选人数 / 选课系数)
- 📄 生成课程信息文本 `course_info.txt`
- 📊 导出课程表 Excel `course_schedule.xlsx`(按星期×节次排版,支持单双周标注、连续节次合并、冻结首行首列)
- 🔧 全部输出统一到 `output/` 目录,可通过 `.env` 自定义

## 项目结构

```
CAS_Auto_Login/
├── main.py                 # 程序入口:登录 → 查询 → 导出
├── config.py               # 配置(读取 .env)
├── CAS_Login.py            # CAS 登录逻辑
├── course_query.py         # 已选课程查询
├── course_info.py          # 课程信息文本输出
├── exporter/               # 导出器
│   ├── base.py             # 导出器抽象基类 + 时间解析
│   └── EXCEL_exporter.py   # Excel 课表导出
├── utils.py                # 辅助工具(选课状态分析等)
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量模板(复制为 .env 使用)
└── output/                 # 程序输出目录(自动创建)
    ├── course_info.txt     #   课程信息文本
    ├── course_schedule.xlsx#   课表 Excel
    └── resp.txt            #   查询异常时的调试响应
```

## 环境要求

- Python 3.9+ (推荐 3.11+)
- Windows / macOS / Linux 均可

## 安装与配置

### 1. 克隆项目并创建虚拟环境

```bash
git clone <your-repo-url>
cd CAS_Auto_Login

# Windows
python -m venv env
env\Scripts\activate

# macOS / Linux
python3 -m venv env
source env/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置账号信息

复制 `.env.example` 为 `.env`,并填写你的南科大 CAS 账号:

```env
# 南方科技大学CAS账号
USERNAME=你的学号
PASSWORD=你的密码

# 指定学年与学期
XN=2026-2027
XQ=1

# 调试模式(开启后输出更详细日志,并保留异常响应文件)
DEBUG=False

# 程序输出目录(可选,默认 output/)
# OUTPUT_DIR=output

# 课表导出文件路径(可选,默认 output/course_schedule.xlsx)
# SCHEDULE_FILE=output/course_schedule.xlsx
```

> ⚠️ `.env` 包含真实凭据,已被 `.gitignore` 忽略,请勿提交到版本库。

## 使用方法

```bash
python main.py
```

程序依次执行:

1. **登录** —— 使用 `.env` 中的账号密码登录 CAS
2. **查询选课** —— 查询指定学年学期的已选课程
3. **输出课程信息** —— 逐条打印课程,并写入 `output/course_info.txt`
4. **导出课表** —— 生成 `output/course_schedule.xlsx`

## 输出文件说明

| 文件 | 说明 |
|---|---|
| `output/course_info.txt` | 课程名称、容量、已选人数、选课系数(每次运行覆盖) |
| `output/course_schedule.xlsx` | 课程表:行 = 节次,列 = 星期;单元格含课程名、周次、单双周、教室;连续节次自动合并 |
| `output/resp.txt` | 仅查询异常时写入服务器原始响应,用于排查问题 |

## 常见问题

**Q: 登录失败怎么办?**
先确认 `.env` 中账号密码正确;若服务器返回异常,可设置 `DEBUG=True` 重跑,并查看 `output/resp.txt` 中的原始响应。

**Q: 怎么查询其他学期?**
修改 `.env` 中的 `XN`(学年,格式 `2026-2027`)和 `XQ`(学期,`1` 或 `2`)。

**Q: 导出文件能放到别的目录吗?**
可以,在 `.env` 中设置 `OUTPUT_DIR` 或 `SCHEDULE_FILE`。

## 免责声明

本项目仅用于个人学习与选课辅助,请遵守学校相关规定,勿滥用或用于商业用途。
