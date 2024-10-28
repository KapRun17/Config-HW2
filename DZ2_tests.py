
import pytest
from unittest import mock
from DZ2 import get_dependencies, build_dependency_graph, visualize_graph

# Тест функции get_dependencies_graph
def test_get_dependencies_success():
    package_name = 'pip'
    expected_dependencies = []

    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = 'Name: test-package\nRequires:\n'
        
        dependencies = get_dependencies(package_name)
        
        assert dependencies == expected_dependencies

# Тест функции get_dependencies_graph при ошибке получения зависимостей
def test_get_dependencies_failure():
    package_name = 'pip'

    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = 'Error: package not found\n'
        
        with pytest.raises(Exception, match=f"Ошибка получения зависимостей для {package_name}: Error: package not found"):
            get_dependencies(package_name)

# Тест функции build_dependency_graph
def test_build_dependency_graph():
    package_name = 'pip'
    mock_dependencies = {
        'pip': []
    }

    with mock.patch('subprocess.run') as mock_run:
        mock_run.side_effect = [
            mock.Mock(returncode=0, stdout='Name: pip\nRequires: \n'),
        ]
        
        graph = build_dependency_graph(package_name)
        assert graph == mock_dependencies

# Тест функции visualize_graph
def test_visualize_graph():
    graph = {
        'pip': []
    }
    
    with mock.patch('graphviz.Digraph') as mock_dot:
        mock_instance = mock_dot.return_value
        visualize_graph(graph)
        
        assert mock_instance.edge.call_count == 0
