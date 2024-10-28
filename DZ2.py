import argparse
import subprocess
import graphviz

def get_dependencies(package_name):
    """Получение зависимостей пакета с помощью pip (без сторонних средств)."""
    result = subprocess.run(
        ['pip', 'show', package_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Ошибка получения зависимостей для {package_name}: {result.stderr}")

    dependencies = []
    for line in result.stdout.splitlines():
        if line.startswith('Requires:'):
            requirements = line.split(':')[1].strip()
            dependencies = [dep.strip() for dep in requirements.split(',')] if requirements else []
            break
    print(f"Зависимости для {package_name}: {dependencies}")
    return dependencies

def build_dependency_graph(package_name, visited=None):
    """Рекурсивно строит граф зависимостей."""
    if visited is None:
        visited = set()
    
    if package_name in visited:
        return {}
    
    visited.add(package_name)
    dependencies = get_dependencies(package_name)

    graph = {package_name: dependencies}
    
    for dep in dependencies:
        graph.update(build_dependency_graph(dep, visited))
    
    return graph

def visualize_graph(graph):
    """Создание визуализации графа с помощью Graphviz."""
    dot = graphviz.Digraph()

    for package, dependencies in graph.items():
        for dep in dependencies:
            dot.edge(package, dep)
    
    return dot

def main():
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей Python пакетов.')
    parser.add_argument('output_path', help='Путь для вывода графа')
    parser.add_argument('package_name', help='Имя анализируемого пакета')
    parser.add_argument('repository_url', help='URL-адрес репозитория (не используется)')
    
    args = parser.parse_args()
    
    graph = build_dependency_graph(args.package_name)
    if not graph:  # Проверка на пустой граф
        print("Граф зависимостей пуст!")
        return
    
    dot = visualize_graph(graph)
    dot.render(args.output_path, format='png', cleanup=True)
    print(f"Граф зависимостей сохранён в {args.output_path}.png")

if __name__ == '__main__':
    main()

