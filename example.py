from codeweb.network_builder import NetworkBuilder
from codeweb.import_parsing.styles.python_styles import python_import_styles
from pyvis.network import Network


if __name__ == '__main__':
    # Create a new Network with desired settings
    empty_network = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    empty_network.repulsion(node_distance=150)

    # Scan project directory and populate network, export to html
    nb = NetworkBuilder(network=empty_network, import_styles=python_import_styles, ignore_external_imports=False)
    populated_network = nb.create_network(project_path='test_project')
    populated_network.show_buttons(filter_=['physics'])
    populated_network.show('example.html', notebook=False)