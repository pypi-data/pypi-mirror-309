from dataclasses import dataclass, field
from typing import Dict, Set, Optional, List, Tuple
from pathlib import Path
from collections import Counter, defaultdict
import ast
from graphviz import Digraph  # 需要先安装: pip install graphviz


@dataclass
class FunctionInfo:
    """函数信息"""

    name: str
    module: str
    is_async: bool = False
    dependencies: Set[str] = field(default_factory=set)
    calls: Set[str] = field(default_factory=set)


@dataclass
class ClassInfo:
    """类信息"""

    name: str
    module: str
    bases: Set[str] = field(default_factory=set)
    methods: Dict[str, FunctionInfo] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)


@dataclass
class ModuleInfo:
    """模块信息"""

    name: str
    path: Path
    classes: Dict[str, ClassInfo] = field(default_factory=dict)
    functions: Dict[str, FunctionInfo] = field(default_factory=dict)
    imports: Dict[str, str] = field(default_factory=dict)
    from_imports: Dict[str, str] = field(default_factory=dict)


@dataclass
class DependencyStats:
    """依赖��计信息"""
    call_frequencies: Counter = field(default_factory=Counter)  # 调用频率
    dependency_frequencies: Counter = field(default_factory=Counter)  # 依赖频率
    circular_dependencies: List[List[str]] = field(default_factory=list)  # 循环依赖链


class ProjectScanner:
    """项目扫描器"""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.modules: Dict[str, ModuleInfo] = {}

    def scan(self) -> Dict[str, ModuleInfo]:
        """扫描项目文件"""
        for py_file in self.root_path.rglob("*.py"):
            if "__pycache__" in str(py_file) or "test" in str(py_file):
                continue

            try:
                module_name = self._get_module_name(py_file)
                module_info = ModuleInfo(name=module_name, path=py_file)
                self.modules[module_name] = module_info

                # 分析模块
                analyzer = ModuleAnalyzer(module_info)
                analyzer.analyze()
            except Exception as e:
                print(f"扫描文件 {py_file} 时出错: {e}")

        return self.modules

    def _get_module_name(self, file_path: Path) -> str:
        """获取模块名"""
        rel_path = file_path.relative_to(self.root_path)
        return str(rel_path.with_suffix("")).replace("/", ".")


class ModuleAnalyzer(ast.NodeVisitor):
    """模块分析器"""

    def __init__(self, module_info: ModuleInfo):
        self.module_info = module_info
        self.current_function: Optional[FunctionInfo] = None
        self.current_class: Optional[ClassInfo] = None

    def analyze(self):
        """分析模块"""
        try:
            with open(self.module_info.path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            self.visit(tree)
        except Exception as e:
            print(f"分析模块 {self.module_info.name} 时出错: {e}")

    def visit_Import(self, node: ast.Import):
        """处理import语句"""
        for alias in node.names:
            name = alias.asname or alias.name
            self.module_info.imports[name] = alias.name

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """处理from import语句"""
        if node.module:
            module_path = node.module
            for alias in node.names:
                name = alias.asname or alias.name
                # 记录完整的导入路径
                self.module_info.from_imports[name] = f"{module_path}.{alias.name}"

    def visit_Name(self, node: ast.Name):
        """处理标识符引用"""
        if isinstance(node.ctx, ast.Load):
            name = node.id
            # 忽略内部引用
            if name in {'self', 'cls', 'lines', 'data', 'result', 'value', 'options'}:
                return
                
            # 检查是否是导入的名称
            full_name = None
            imports_copy = dict(self.module_info.imports)
            from_imports_copy = dict(self.module_info.from_imports)
            
            if name in imports_copy:
                full_name = imports_copy[name]
            elif name in from_imports_copy:
                full_name = from_imports_copy[name]
            
            if full_name:
                if self.current_function:
                    self.current_function.dependencies.add(full_name)
                elif self.current_class:
                    self.current_class.dependencies.add(full_name)

    def visit_Call(self, node: ast.Call):
        """处理函数调用"""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            # 检查是否是导入的函数
            from_imports_copy = dict(self.module_info.from_imports)
            if func_name in from_imports_copy:
                func_name = from_imports_copy[func_name]
            if self.current_function:
                # 这是实际的函数调用
                self.current_function.calls.add(func_name)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                obj_name = node.func.value.id
                method_name = node.func.attr
                
                # 忽略 self 调用
                if obj_name == 'self':
                    if self.current_class:
                        # 记录为当前类的方法调用
                        full_name = f"{self.current_class.name}.{method_name}"
                        if self.current_function:
                            self.current_function.calls.add(full_name)
                else:
                    # 检查是否是导入的模块的方法
                    imports_copy = dict(self.module_info.imports)
                    if obj_name in imports_copy:
                        obj_name = imports_copy[obj_name]
                    full_name = f"{obj_name}.{method_name}"
                    if self.current_function:
                        self.current_function.calls.add(full_name)
                        # 只有外部对象才添加到依赖中
                        if obj_name in self.module_info.imports or obj_name in self.module_info.from_imports:
                            self.current_function.dependencies.add(obj_name)
        
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        """处理属性访问"""
        if isinstance(node.value, ast.Name):
            base_name = node.value.id
            # 忽略内部属性访问
            if base_name in {'self', 'cls'}:
                return
                
            attr_name = node.attr
            full_name = f"{base_name}.{attr_name}"
            
            # 检查是否是导入的模块的属性
            imports_copy = dict(self.module_info.imports)
            if base_name in imports_copy:
                module_path = imports_copy[base_name]
                full_name = f"{module_path}.{attr_name}"
                
                if self.current_function:
                    self.current_function.dependencies.add(full_name)
                elif self.current_class:
                    self.current_class.dependencies.add(full_name)
        
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """处理类定义"""
        prev_class = self.current_class
        class_info = ClassInfo(name=node.name, module=self.module_info.name)
        self.current_class = class_info

        # 处理基类
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_name = base.id
                class_info.bases.add(base_name)
                class_info.dependencies.add(base_name)

        # 访问类体
        for child in node.body:
            self.visit(child)

        self.module_info.classes[node.name] = class_info
        self.current_class = prev_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """处理函数定义"""
        prev_function = self.current_function
        func_info = FunctionInfo(
            name=node.name,
            module=self.module_info.name,
            is_async=isinstance(node, ast.AsyncFunctionDef)
        )
        self.current_function = func_info

        # 访问函数体
        for child in node.body:
            self.visit(child)

        if self.current_class:
            self.current_class.methods[node.name] = func_info
        else:
            self.module_info.functions[node.name] = func_info
        
        self.current_function = prev_function

    visit_AsyncFunctionDef = visit_FunctionDef


class DependencyAnalyzer:
    """依赖分析器"""
    # 内置模块和函数列表
    BUILTIN_MODULES = {
        'str', 'print', 'len', 'dict', 'set', 'list', 'tuple', 'int', 'float',
        'isinstance', 'sorted', 'any', 'all', 'sum', 'round', 'range',
        'json', 'os', 'sys', 'pathlib', 'typing', 'collections', 'datetime',
        'abc', 'enum', 'time', 'logging', 'subprocess', 'threading',
        'Path', 'Dict', 'Set', 'List', 'Optional', 'Union', 'Any', 'TypedDict',
        'defaultdict', 'Counter'
    }
    
    # 内置异常和日志相关
    BUILTIN_EXCEPTIONS_AND_LOGGING = {
        'Exception', 'RuntimeError', 'ValueError', 'TypeError', 'KeyError',
        'AttributeError', 'ImportError', 'FileNotFoundError',
        'logger.error', 'logger.warning', 'logger.info', 'logger.debug',
        'logging.error', 'logging.warning', 'logging.info', 'logging.debug',
        'logging.getLogger'
    }
    
    # 常见的内部引用
    INTERNAL_REFS = {
        'self', 'cls', 'lines', 'errors', 'data', 'config', 'result', 'value',
        'options', 'args', 'kwargs', 'obj', 'item', 'key', 'val', 'file',
        'path', 'name', 'text', 'content', 'info', 'error', 'warning',
        'module', 'function', 'method', 'class_name', 'base', 'attr'
    }

    def __init__(self, modules: Dict[str, ModuleInfo]):
        self.modules = modules
        self.dependency_graph = defaultdict(set)
        self.stats = DependencyStats()

    def _should_ignore(self, name: str) -> bool:
        """判断是否应该忽略该依赖"""
        # 分割完整路径
        parts = name.split('.')
        
        # 检查是否是内置模块、异常或引用
        if (parts[0] in self.BUILTIN_MODULES or 
            parts[0] in self.INTERNAL_REFS or 
            name in self.BUILTIN_EXCEPTIONS_AND_LOGGING):
            return True
            
        # 检查常见的内部属性访问
        if len(parts) > 1 and parts[0] in self.INTERNAL_REFS:
            return True
            
        # 检查日志相关调用
        if name.startswith('logger.') or name.startswith('logging.'):
            return True
            
        # 检查异常相关
        if name.endswith('Error') or name.endswith('Exception'):
            return True
            
        return False

    def _calculate_frequencies(self):
        """计算依赖和调用频率"""
        for module_info in self.modules.values():
            # 统计类中的频率
            for class_info in module_info.classes.values():
                for method_info in class_info.methods.values():
                    # 过滤调用频率
                    for call in method_info.calls:
                        if not self._should_ignore(call):
                            self.stats.call_frequencies[call] += 1
                    
                    # 过滤依赖频率
                    for dep in method_info.dependencies:
                        if not self._should_ignore(dep):
                            self.stats.dependency_frequencies[dep] += 1
                
                # 过滤类级依赖
                for dep in class_info.dependencies:
                    if not self._should_ignore(dep):
                        self.stats.dependency_frequencies[dep] += 1
            
            # 统计函数中的频率
            for func_info in module_info.functions.values():
                # 过滤调用频率
                for call in func_info.calls:
                    if not self._should_ignore(call):
                        self.stats.call_frequencies[call] += 1
                
                # 过滤依赖频率
                for dep in func_info.dependencies:
                    if not self._should_ignore(dep):
                        self.stats.dependency_frequencies[dep] += 1

    def _build_dependency_graph(self):
        """构建依赖图"""
        for module_name, module_info in self.modules.items():
            # 处理类依赖
            for class_info in module_info.classes.values():
                class_full_name = f"{module_name}.{class_info.name}"
                
                # 添加基类依赖（这是真正的依赖）
                for base in class_info.bases:
                    if not self._should_ignore(base):
                        self.dependency_graph[class_full_name].add(base)
                
                # 添加类级依赖（这是真正的依赖）
                for dep in class_info.dependencies:
                    if not self._should_ignore(dep):
                        self.dependency_graph[class_full_name].add(dep)
                
                # 处理方法
                for method_info in class_info.methods.values():
                    method_full_name = f"{class_full_name}.{method_info.name}"
                    # 添加方法的依赖（这是真正的依赖）
                    for dep in method_info.dependencies:
                        if not self._should_ignore(dep):
                            self.dependency_graph[method_full_name].add(dep)
                    # 添加方法的调用（这是函数调用关系）
                    for call in method_info.calls:
                        if not self._should_ignore(call):
                            # 使用不同的边样式来区分调用和依赖
                            self.dependency_graph[method_full_name].add(f"call:{call}")
            
            # 处理函数
            for func_info in module_info.functions.values():
                func_full_name = f"{module_name}.{func_info.name}"
                # 添加函数的依赖（这是真正的依赖）
                for dep in func_info.dependencies:
                    if not self._should_ignore(dep):
                        self.dependency_graph[func_full_name].add(dep)
                # 添加函数的调用（这是函数调用关系）
                for call in func_info.calls:
                    if not self._should_ignore(call):
                        # 使用不同的边样式来区分调用和依赖
                        self.dependency_graph[func_full_name].add(f"call:{call}")

    def analyze(self) -> DependencyStats:
        """分析依赖关系"""
        self._build_dependency_graph()
        self._calculate_frequencies()
        self._detect_circular_dependencies()
        return self.stats

    def _detect_circular_dependencies(self):
        """检测循环依赖"""
        visited = set()
        path = []
        # 创建依赖图的副本，避免在遍历过中修改
        dependency_graph_copy = {k: set(v) for k, v in self.dependency_graph.items()}
        
        def dfs(node: str):
            if node in path:
                # 找到循环依赖
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                cycle_key = tuple(sorted(cycle))  # 使用序后的元组作为键，避免重复
                if cycle_key not in seen_cycles:
                    seen_cycles.add(cycle_key)
                    self.stats.circular_dependencies.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.append(node)
            
            # 使用依赖图的副本进行遍历
            for neighbor in dependency_graph_copy.get(node, set()):
                dfs(neighbor)
            
            path.pop()
        
        # 用于去重的集合
        seen_cycles = set()
        
        # 对每个节点进行DFS
        nodes = list(dependency_graph_copy.keys())  # 创建键的列表副本
        for node in nodes:
            if node not in visited:
                dfs(node)

    def generate_graph(self, output_path: str = "dependency_graph"):
        """生成依赖关系图"""
        dot = Digraph(comment='项目依赖关系图')
        dot.attr(rankdir='LR')  # 从左到右布局
        
        # 设置节点和边的样式
        dot.attr('node', shape='box', style='rounded')
        
        # 添加模块子图
        for module_name, module_info in self.modules.items():
            with dot.subgraph(name=f'cluster_{module_name}') as c:
                c.attr(label=module_name, style='rounded')
                
                # 添加类节点
                for class_name, class_info in module_info.classes.items():
                    class_id = f"{module_name}.{class_name}"
                    c.node(class_id, class_name, style='filled', fillcolor='lightblue')
                    
                    # 添加方法节点
                    for method_name in class_info.methods:
                        method_id = f"{class_id}.{method_name}"
                        c.node(method_id, method_name, style='filled', fillcolor='lightgreen')
                        # 连接类和方法
                        dot.edge(class_id, method_id, style='dotted')
                
                # 添加独立函数节点
                for func_name in module_info.functions:
                    func_id = f"{module_name}.{func_name}"
                    c.node(func_id, func_name, style='filled', fillcolor='lightgrey')
        
        # 添加依赖关系边
        added_edges = set()  # 用于去重
        for source, targets in self.dependency_graph.items():
            for target in targets:
                if not self._should_ignore(target):
                    edge_key = (source, target)
                    if edge_key not in added_edges:
                        if target.startswith("call:"):
                            # 这是函数调用
                            real_target = target[5:]  # 移除 "call:" 前缀
                            weight = self.stats.call_frequencies.get(real_target, 0)
                            dot.edge(
                                source, real_target,
                                weight=str(weight),
                                label=str(weight) if weight > 1 else '',
                                style='dashed',  # 使用虚线表示调用
                                color='blue'
                            )
                        else:
                            # 这是依赖关系
                            dot.edge(
                                source, target,
                                style='solid',  # 使用实线表示依赖
                                color='black'
                            )
                        added_edges.add(edge_key)
        
        # 添加循环依赖标记
        for cycle in self.stats.circular_dependencies:
            for i in range(len(cycle)):
                source = cycle[i]
                target = cycle[(i + 1) % len(cycle)]
                edge_key = (source, target)
                if edge_key not in added_edges:
                    dot.edge(source, target, color='red', style='bold')
                    added_edges.add(edge_key)
        
        # 保存图片
        try:
            dot.render(output_path, format='png', cleanup=True)
            print(f"依赖图已保存到 {output_path}.png")
        except Exception as e:
            print(f"生成依赖图时出错: {e}")


def analyze_project(src_path: str) -> Tuple[Dict[str, ModuleInfo], DependencyStats]:
    """分析项目并返回模块信息和依赖统计"""
    try:
        scanner = ProjectScanner(Path(src_path))
        modules = scanner.scan()
        
        # 分析依赖
        analyzer = DependencyAnalyzer(modules)
        stats = analyzer.analyze()
        
        # 生成依赖图
        analyzer.generate_graph()
        
        return modules, stats
    except Exception as e:
        raise RuntimeError(f"项目分析失败: {str(e)}")


if __name__ == "__main__":
    try:
        modules, stats = analyze_project("src")
        
        # 打印模块信息
        for module_name, module_info in modules.items():
            print(f"\n模块: {module_name}")
            
            print("\n类:")
            for class_name, class_info in module_info.classes.items():
                print(f"  {class_name}:")
                print(f"    基类: {class_info.bases}")
                print(f"    依赖: {class_info.dependencies}")
                print("    方法:")
                for method_name, method_info in class_info.methods.items():
                    print(f"      {method_name}:")
                    print(f"        调用: {method_info.calls}")
                    print(f"        依赖: {method_info.dependencies}")
            
            print("\n函数:")
            for func_name, func_info in module_info.functions.items():
                print(f"  {func_name}:")
                print(f"    调用: {func_info.calls}")
                print(f"    依赖: {func_info.dependencies}")
        
        # 打印依赖统计信息
        print("\n\n依赖统计信息:")
        print("\n最频繁的函数调用:")
        for call, count in stats.call_frequencies.most_common(10):
            print(f"  {call}: {count}次")
        
        print("\n最常见的依赖:")
        for dep, count in stats.dependency_frequencies.most_common(10):
            print(f"  {dep}: {count}次")
        
        print("\n发现的循环依赖:")
        for cycle in stats.circular_dependencies:
            print(f"  {' -> '.join(cycle)} -> {cycle[0]}")
            
    except Exception as e:
        print(f"错误: {e}")
