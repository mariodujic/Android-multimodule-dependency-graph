import os
import sys

from pyvis.network import Network

from utils import filter_dict, stand, get_between

circular_dependency_color = "#F88379"


def get_graph(path, gradle_kotlin_dsl):
    net = Network(height="1500px", width="1500px", directed=True)
    net.inherit_edge_colors(False)
    modules = dict()
    extension = '.kts' if gradle_kotlin_dsl else ''
    gradle_settings_file_name = 'settings.gradle' + extension
    gradle_build_file_name = 'build.gradle' + extension

    def retrieve_project_modules(root, files):
        if gradle_settings_file_name in files:
            root_file = root + os.sep + gradle_settings_file_name
            assert os.path.isfile(root_file)
            file = open(root_file, 'r')
            lines = file.readlines()
            for line in lines:
                if stand(line).__contains__("\':"):
                    ln = get_between(stand(line), '\'', '\'')
                    modules[ln] = []
                    net.add_node(ln, shape='circle', mass=7)

    def add_module_dependencies(root, files):
        if gradle_build_file_name in files:
            root_file = root + os.sep + gradle_build_file_name
            assert os.path.isfile(root_file)
            file = open(root_file, 'r')
            lines = file.readlines()
            current_module = ""
            root_formatted = str(root).replace(os.sep, ':').replace(".", ":")
            for module in modules.keys():
                if root_formatted.__contains__(module):
                    current_module = module
            for line in lines:
                if stand(line).__contains__("implementation"):
                    ln = get_between(stand(line), '\'', '\'')
                    for module in modules:
                        if ln == module:
                            modules[current_module].append(module)

    def get_circular_dependency_modules() -> []:
        circular_dependency_modules = []
        filtered_modules = filter_dict(modules, lambda elem: len(elem[1]) > 0).items()
        for module, module_dependencies in filtered_modules:

            def search_circular_dependencies(scope_dependencies: []):
                if scope_dependencies.__contains__(module):
                    circular_dependency_modules.append(module)
                    return
                for sub_module in scope_dependencies:
                    if len(modules[sub_module]) > 0:
                        search_circular_dependencies(modules[sub_module])

            try:
                search_circular_dependencies(module_dependencies)
            except RecursionError:
                pass
        return circular_dependency_modules

    def add_module_edges():
        circular_dependencies = get_circular_dependency_modules()
        for module, dependencies in modules.items():
            is_circular_dependency_module = circular_dependencies.__contains__(module)
            if is_circular_dependency_module:
                net.get_node(module)["color"] = circular_dependency_color
            for dependency in dependencies:
                is_circular_dependency = is_circular_dependency_module and \
                                         circular_dependencies.__contains__(dependency)
                if is_circular_dependency:
                    net.add_edge(module, dependency, color=circular_dependency_color)
                else:
                    net.add_edge(module, dependency)

    for current_root, _, current_files in os.walk(path):
        retrieve_project_modules(current_root, current_files)
        add_module_dependencies(current_root, current_files)
    # Draws directions, i.e. dependencies, checks for a circular dependencies between modules and marks modules
    # that are cause of a circular dependency.
    add_module_edges()
    return net


if __name__ == '__main__':
    has_project_path_argument = len(sys.argv) > 1
    project_path = ""
    if has_project_path_argument:
        project_path = sys.argv[1]
        project_path_exists = os.path.exists(project_path)
        if not project_path_exists:
            raise Exception("Invalid project path")
    else:
        print('Enter your project path:')
        project_path = input().strip()
    print('Generating graph..')
    kotlin_dsl: bool
    if os.path.exists(project_path + os.sep + 'settings.gradle.kts'):
        kotlin_dsl = True
    elif os.path.exists(project_path + os.sep + 'settings.gradle'):
        kotlin_dsl = False
    else:
        raise FileNotFoundError("Unable to find Gradle settings file")
    graph = get_graph(project_path, kotlin_dsl)
    graph.show('index.html')
