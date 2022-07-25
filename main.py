import os

from pyvis.network import Network


def get_graph(path, gradle_kotlin_dsl):
    net = Network(height="1500px", width="1500px", directed=True)
    modules = []
    extension = '.kts' if gradle_kotlin_dsl else ''
    gradle_settings_file_name = 'settings.gradle' + extension
    gradle_build_file_name = 'build.gradle' + extension

    def insert_module_nodes(root, files):
        if gradle_settings_file_name in files:
            root_file = root + os.sep + gradle_settings_file_name
            assert os.path.isfile(root_file)
            file = open(root_file, 'r')
            lines = file.readlines()
            for line in lines:
                if stand(line).__contains__("\':"):
                    ln = get_between(stand(line), '\'', '\'')
                    modules.append(ln)
                    net.add_node(ln, shape='circle', mass=7)

    def set_node_edges(root, files):
        if gradle_build_file_name in files:
            root_file = root + os.sep + gradle_build_file_name
            assert os.path.isfile(root_file)
            file = open(root_file, 'r')
            lines = file.readlines()
            current_module = ""
            root_formatted = str(root).replace(os.sep, ':').replace(".", ":")
            for module in modules:
                if root_formatted.__contains__(module):
                    current_module = module
            for line in lines:
                if stand(line).__contains__("implementation"):
                    ln = get_between(stand(line), '\'', '\'')
                    for module in modules:
                        if ln == module:
                            net.add_edge(current_module, module)

    for current_root, _, current_files in os.walk(path):
        insert_module_nodes(current_root, current_files)
        set_node_edges(current_root, current_files)
    return net


def get_between(s, first, last) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def stand(s) -> str:
    return str(s).lower().replace('\"', '\'').replace(".", ":")


if __name__ == '__main__':
    print('Enter your project path:')
    directoryPath = input().strip()
    print('Generating graph..')
    kotlin_dsl: bool
    if os.path.exists(directoryPath + os.sep + 'settings.gradle.kts'):
        kotlin_dsl = True
    elif os.path.exists(directoryPath + os.sep + 'settings.gradle'):
        kotlin_dsl = False
    else:
        raise Exception("Unable to find Gradle settings file")
    graph = get_graph(directoryPath, kotlin_dsl)
    graph.show('dependency_graph.html')
