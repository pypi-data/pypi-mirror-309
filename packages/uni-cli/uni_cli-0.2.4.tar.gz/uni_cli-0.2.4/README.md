### 项目使用 uv 管理虚拟环境

> https://docs.astral.sh/uv/

### 项目依赖安装

-   `uv sync`:同步 <u>pyproject.toml</u> 中的依赖
-   `uv pip install -r requirements.txt`:通过 pip 安装`requirements.txt`中的依赖<br/>
    paddleocr 需要 `paddlepaddle` 依赖, 安装文档见 [paddlepaddle](https://www.paddlepaddle.org.cn/install/quick)

### command

```shell
uv sync
uv run example hello Xiaoming
uv run example goodbye Xiaoming --formal
uv run say -t hello
uv run os
uv run bitget spot btc,eth
uv run bitget mix popcat
uv run pyv
uv run sync grid
uv run sync strategy
uv run fudai fudai.py 192.168.123.22:5555
uv run fudai 192.168.123.22:5555 --no-debug --switch -p 900
uv run fudai 192.168.123.22:5555 --no-debug -s -p 900
```
