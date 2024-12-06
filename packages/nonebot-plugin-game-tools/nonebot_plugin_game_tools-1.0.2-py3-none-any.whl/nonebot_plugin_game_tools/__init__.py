from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
import main

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_game_tools",
    description="游戏工具插件.",
    usage="菜单",
    type="application",
    homepage="https://github.com/snowrabbit-top/nonebot_plugin_game_tools",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config = get_plugin_config(Config)
