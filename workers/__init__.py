import ast
import importlib
import pkgutil
from pathlib import Path


def has_worker_task(file_path: Path) -> bool:
    tree = ast.parse(file_path.read_text())

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "worker_task":
                    return True

                if (
                    isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Name)
                    and decorator.func.id == "worker_task"
                ):
                    return True

    return False


def discover_worker_modules() -> list[str]:
    modules: list[str] = []

    for _, package_name, ispkg in pkgutil.iter_modules(
        __path__,
        __name__ + ".",
    ):
        if not ispkg:
            continue

        package = importlib.import_module(package_name)

        for module in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + ".",
        ):
            spec = module.module_finder.find_spec(module.name, None)

            if spec is None or spec.origin is None:
                continue

            if has_worker_task(Path(spec.origin)):
                modules.append(module.name)

    return sorted(modules)
