import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api import config_router, exclude_router, history_router
from .api.config import init_config
from .api.history import get_report_manager

app = FastAPI(
    title="OhMyPrompt",
    docs_url=None,  # 禁用 Swagger UI
    redoc_url=None,  # 禁用 ReDoc
)

# 静态文件和模板配置
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"

# 确保 dist 目录存在
dist_path = static_path / "dist"
dist_path.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
templates = Jinja2Templates(directory=str(templates_path))

# 注册 API 路由
app.include_router(exclude_router, prefix="/api/exclude")
app.include_router(config_router, prefix="/api/config")
app.include_router(history_router, prefix="/api/history")


@app.on_event("startup")
async def startup_event() -> None:
    """启动时初始化配置管理器"""
    project_root = os.environ.get("PROJECT_ROOT")
    if not project_root:
        raise RuntimeError("未设置 PROJECT_ROOT 环境变量")
    print(f"初始化配置，项目根目录: {project_root}")
    init_config(project_root)
    
    # 配置依赖注入
    app.dependency_overrides[get_report_manager] = lambda: get_report_manager(project_root)
    
    print("初始化完成")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/history", response_class=HTMLResponse)
async def history_view(request: Request) -> HTMLResponse:
    """历史记录页面"""
    return templates.TemplateResponse("index.html", {"request": request})
