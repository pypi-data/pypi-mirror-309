import typer

from douyin.fudai import Fudai

app = typer.Typer()


@app.command()
def fudai_choujiang(
    device_id: str = typer.Argument(..., help="设备ID,例如:192.168.123.13:5555"),
    debug: bool = typer.Option(
        True, "--debug/--no-debug", "-d", help="是否开启调试模式"
    ),
    switch: bool = typer.Option(
        False, "--switch/--no-switch", "-s", help="是否自动切换直播间"
    ),
    prize_min: int = typer.Option(600, "--prize-min", "-p", help="奖品最小参考价值"),
):
    """
    抖音自动福袋抽奖.

    """
    fudai = Fudai(device_id, prize_min_value=prize_min, defbug=debug, switch=switch)
    fudai.get_battery_level()
    fudai.choujiang()
