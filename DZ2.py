import argparse
import requests
import graphviz

def get_dependencies(package_name):
    """Получение зависимостей пакета с помощью API реестра пакетов."""
    
    url = f"https://pypi.org/pypi/{package_name}/json"  # URL API для получения информации о пакете
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка получения зависимостей для {package_name}: {response.text}")

    data = response.json()
    requires_dist = data['info'].get('requires_dist', [])

    # Обработка формата зависимостей
    dependencies = []
    if requires_dist:
        for dep in requires_dist:
            name = dep.split(';')[0].strip()  # Берем только имя пакета без условий
            name = name.split('>')[0].split('<')[0].split('=')[0].split(' ')[0].split('[')[0].split('(')[0].split('!')[0]
            if ',' in name:  # Если есть несколько зависимостей, разбиваем их
                name_parts = [n.strip() for n in name.split(',')]
                dependencies.extend(name_parts)
            else:
                dependencies.append(name)

    print(f"Зависимости для {package_name}: {dependencies}")
    return dependencies

def build_dependency_graph(package_name, level=0, visited=None):
    """Рекурсивно строит граф зависимостей с учетом уровня вложенности."""
    if visited is None:
        visited = set()
    
    # Проверка, было ли имя пакета посещено, и уровень вложенности
    if package_name in visited or level >= 2:
        return {}
    
    visited.add(package_name)
    dependencies = get_dependencies(package_name)

    graph = {package_name: dependencies}
    
    for dep in dependencies:
        graph.update(build_dependency_graph(dep, level + 1, visited))
    
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

