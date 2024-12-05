import os
import ast
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class LoggerInfo:
    name: str
    library: str
    file_location: str
    line_number: int


def _adjust_name(name: str) -> str:
    if "site-packages." in name:
        return name.split("site-packages.")[1]
    else:
        return name


class EnhancedLoggerVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str = "<current_file>"):
        self.loggers: List[LoggerInfo] = []
        self.has_loguru_import = False
        self.loguru_import_line = 0
        self.file_path = file_path

    def resolve_logger_name(self, node: ast.Call) -> str:
        """
        Attempt to resolve the logger name from the call arguments.
        Handles common patterns like __name__, __package__, etc.
        """
        if not node.args:
            return "<root>"

        arg = node.args[0]

        # Handle string literals
        if isinstance(arg, ast.Constant):
            return arg.value

        # Handle __name__
        if isinstance(arg, ast.Name) and arg.id == "__name__":
            # Convert file path to python module path
            module_path = self.file_path.replace("/", ".").replace("\\", ".")
            # Remove .py extension if present
            if module_path.endswith(".py"):
                module_path = module_path[:-3]
            return module_path

        # Handle __package__
        if isinstance(arg, ast.Name) and arg.id == "__package__":
            package_path = (
                os.path.dirname(self.file_path).replace("/", ".").replace("\\", ".")
            )
            return package_path or "<root_package>"

        # Handle string operations (like __name__.split('.')[-1])
        if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute):
            if isinstance(arg.func.value, ast.Name) and arg.func.value.id == "__name__":
                module_path = self.file_path.replace("/", ".").replace("\\", ".")
                if module_path.endswith(".py"):
                    module_path = module_path[:-3]
                # If it's a split operation, try to handle it
                if arg.func.attr == "split":
                    return f"<split_of_{module_path}>"

        # Handle concatenation
        if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
            left = self.resolve_constant_str(arg.left)
            right = self.resolve_constant_str(arg.right)
            if left and right:
                return f"{left}{right}"

        return "<dynamic_logger>"

    def resolve_constant_str(self, node: ast.AST) -> Optional[str]:
        """Helper method to resolve constant string values"""
        if isinstance(node, ast.Constant):
            return node.s
        if isinstance(node, ast.Name) and node.id == "__name__":
            module_path = self.file_path.replace("/", ".").replace("\\", ".")
            if module_path.endswith(".py"):
                module_path = module_path[:-3]
            return module_path
        return None

    def visit_Call(self, node):
        # Standard logging module patterns
        if isinstance(node.func, ast.Attribute) and isinstance(
            node.func.value, ast.Name
        ):
            # logging.getLogger() pattern
            if node.func.value.id == "logging" and node.func.attr == "getLogger":
                name = self.resolve_logger_name(node)

                self.loggers.append(
                    LoggerInfo(
                        name=_adjust_name(name),
                        library="logging",
                        file_location=self.file_path,
                        line_number=node.lineno,
                    )
                )

            # structlog patterns
            elif node.func.value.id == "structlog":
                if node.func.attr in ["get_logger", "getLogger"]:
                    name = self.resolve_logger_name(node)

                    self.loggers.append(
                        LoggerInfo(
                            name=name,
                            library="structlog",
                            file_location=self.file_path,
                            line_number=node.lineno,
                        )
                    )
                elif node.func.attr == "wrap_logger":
                    self.loggers.append(
                        LoggerInfo(
                            name="<wrapped_logger>",
                            library="structlog",
                            file_location=self.file_path,
                            line_number=node.lineno,
                        )
                    )

        self.generic_visit(node)

    def visit_Import(self, node):
        # Track logger-related imports
        for alias in node.names:
            if alias.name in ["logging", "structlog"]:
                self.loggers.append(
                    LoggerInfo(
                        name=f"imported_{alias.name}",
                        library=alias.name,
                        file_location=self.file_path,
                        line_number=node.lineno,
                    )
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Track from ... import ... patterns
        if node.module == "loguru" and any(
            alias.name == "logger" for alias in node.names
        ):
            self.has_loguru_import = True
            self.loguru_import_line = node.lineno
            self.loggers.append(
                LoggerInfo(
                    name="loguru.logger",
                    library="loguru",
                    file_location=self.file_path,
                    line_number=node.lineno,
                )
            )
        elif node.module in ["logging", "structlog"]:
            for alias in node.names:
                self.loggers.append(
                    LoggerInfo(
                        name=f"{node.module}.{alias.name}",
                        library=node.module,
                        file_location=self.file_path,
                        line_number=node.lineno,
                    )
                )
        self.generic_visit(node)


def find_loggers(project_path: str) -> Dict[str, List[LoggerInfo]]:
    """
    Scan a Python project for logger instances from various logging libraries.

    Args:
        project_path: Path to the project root

    Returns:
        dict: Dictionary mapping file paths to lists of LoggerInfo objects
    """
    logger_instances = {}

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())

                    relative_path = os.path.relpath(file_path, project_path)
                    visitor = EnhancedLoggerVisitor(relative_path)
                    visitor.visit(tree)

                    if visitor.loggers:
                        logger_instances[relative_path] = visitor.loggers

                except (SyntaxError, UnicodeDecodeError):
                    continue

    return logger_instances


def print_enhanced_report(logger_instances: Dict[str, List[LoggerInfo]]):
    """Print a detailed report of all logger instances found."""
    print("\nEnhanced Logger Usage Report")
    print("=" * 60)

    # Collect statistics
    library_stats = {}
    all_loggers = []

    for file_loggers in logger_instances.values():
        for logger in file_loggers:
            all_loggers.append(logger)
            library_stats[logger.library] = library_stats.get(logger.library, 0) + 1

    # Print summary
    print(f"\nTotal logger instances: {len(all_loggers)}")
    print("\nLogger instances by library:")
    for lib, count in sorted(library_stats.items()):
        print(f"  - {lib}: {count}")

    # Print detailed breakdown
    print("\nDetailed logger instances by file:")
    for file_path, loggers in sorted(logger_instances.items()):
        print(f"\n{file_path}:")
        for logger in sorted(loggers, key=lambda x: (x.library, x.line_number)):
            print(f"  - [{logger.library}] Line {logger.line_number}: {logger.name}")


def main() -> None:
    # Replace with your project path
    project_path = "."  # Default to current directory
    logger_instances = find_loggers(project_path)
    print_enhanced_report(logger_instances)


if __name__ == "__main__":
    main()
