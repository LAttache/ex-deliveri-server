import importlib
import pkgutil
from fastapi import APIRouter
from typing import List

def collect_routers() -> List[APIRouter]:
    routers = []
    package = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            routers.append(router)

    return routers
