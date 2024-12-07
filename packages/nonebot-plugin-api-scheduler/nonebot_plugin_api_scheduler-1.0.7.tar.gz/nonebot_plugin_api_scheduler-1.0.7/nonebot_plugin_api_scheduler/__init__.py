import nonebot
from nonebot.log import logger
from importlib.util import find_spec

if not find_spec("nonebot.adapters.fastapi"):
    logger.warning("FastAPI 驱动器未安装，请安装后重试：pip install nonebot2[fastapi]")
    raise RuntimeError("FastAPI 驱动器未安装，停止插件加载")

# 检查是否安装 nonebot_plugin_apscheduler 插件
if not find_spec("nonebot_plugin_apscheduler"):
    logger.warning("插件 nonebot_plugin_apscheduler 未安装，请安装后重试：pip install nonebot-plugin-apscheduler")
    raise RuntimeError("nonebot_plugin_apscheduler 插件未安装，停止插件加载")

from nonebot.plugin import PluginMetadata
from fastapi import FastAPI, Depends, HTTPException, status
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageSegment,
    Message,
)
from pydantic import BaseModel
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import time

__plugin_meta__ = PluginMetadata(
    name="{nonebot-plugin-api-scheduler}",
    description="{像操作API一样设置定时任务&计划任务}",
    usage="{https://github.com/mmdexb/nonebot-plugin-api-scheduler/blob/master/README.md}",
    type="{application}",
    homepage="{https://github.com/mmdexb/nonebot-plugin-api-scheduler/}",
    supported_adapters={"~onebot.v11"},
)

app: FastAPI = nonebot.get_app()
security = HTTPBasic()

async def do_send(bot: Bot, msg: str, img_url: str, qqgroup_id: str, is_at_all: bool):
    message = MessageSegment.text(msg)
    if img_url:
        message += MessageSegment.image(img_url)
    if is_at_all:
        message += MessageSegment.at("all")
    message = Message(message)
    await bot.send_group_msg(group_id=int(qqgroup_id), message=message)


class timer_model(BaseModel):
    # 在时间戳执行
    timestamp: str  # 2024-10-18 18:00:00
    content: str
    img_url: str
    qqgroup_id: str
    is_at_all: bool


class scheduler_model(BaseModel):
    # 每几天的几时几分执行
    day: int
    hour: int
    minute: int
    second: int
    content: str
    img_url: str
    qqgroup_id: str
    is_at_all: bool

@app.post("/scheduler/timer")
async def scheduler_timer(timer: timer_model):
    if not find_spec("nonebot_plugin_apscheduler"):
        return {"code": 500, "msg": "插件未安装，无法设置任务"}
    
    timestamp = timer.timestamp
    run_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    try:
        scheduler.add_job(do_send, "date", run_date=run_time, args=[list(nonebot.get_bots().values())[0], timer.content,
                                                                    timer.img_url, timer.qqgroup_id, timer.is_at_all])
    except IndexError:
        return {"code": 500, "msg": "机器人未上线"}
    return {"code": 200, "msg": "任务已设定"}


@app.post("/scheduler/plan")
async def scheduler_plan(plan: scheduler_model):
    if not find_spec("nonebot_plugin_apscheduler"):
        return {"code": 500, "msg": "插件未安装，无法设置任务"}
    
    day = plan.day
    hour = plan.hour
    minute = plan.minute
    second = plan.second
    try:
        scheduler.add_job(do_send, "cron", day=f'*/{day}', hour=hour, minute=minute, second=second,
                          args=[list(nonebot.get_bots().values())[0], plan.content,
                                plan.img_url, plan.qqgroup_id, plan.is_at_all])
    except IndexError:
        return {"code": 500, "msg": "机器人未上线"}
    return {"code": 200, "msg": "任务已设定"}


@app.get("/scheduler/cancel")
async def scheduler_cancel(job_id: str):
    if not find_spec("nonebot_plugin_apscheduler"):
        return {"code": 500, "msg": "插件未安装，无法取消任务"}
    
    scheduler.remove_job(job_id)
    return {"code": 200, "msg": "任务已取消"}


@app.get("/scheduler/list")
async def scheduler_list():
    if not find_spec("nonebot_plugin_apscheduler"):
        return {"code": 500, "msg": "插件未安装，无法获取任务列表"}
    
    jobs = scheduler.get_jobs()
    job_list = []
    for job in jobs:
        print(job)

        send_what: str = job.args[1] + "\n"
        if job.args[2] != "":
            send_what += job.args[2] + "\n"
        if job.args[4]:
            send_what += "@全体成员"
        job_list.append(
            {
                "id": job.id,
                "name": job.name,
                "send_what": send_what,
                "send_to": job.args[3],
                "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S") if job.next_run_time else None,
                "trigger": str(job.trigger)
            }
        )

    return {"code": 200, "msg": "任务列表", "data": job_list}


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin"
    if (credentials.username != correct_username or
            credentials.password != correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(authenticate)])
async def dashboard():
    html_file = open("dashboard.html", "r", encoding="utf-8").read()
    return html_file
