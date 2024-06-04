# codeweb - Codebase Visualizer

Provides functionality to scan a codebase (any language) and create a network
graph based on imports. Each file forms a node, and each import statement creates
and edge between two nodes. Node size corresponds to number of lines in the file.

Built around the pyvis, docs: https://pyvis.readthedocs.io/en/latest/

### Example
```
  from codeweb.network_builder import NetworkBuilder
  from codeweb.import_parsing import python_import_styles
  from pyvis.network import Network

  # Create a new Network with desired settings
  empty_network = Network(directed=True)
  empty_network.repulsion(node_distance=150)

  # Scan project directory and populate network, export to html
  nb = NetworkBuilder(network=empty_network, import_styles=python_import_styles, ignore_external_imports=False)
  populated_network = nb.create_network(project_path='.')
  populated_network.show('example.html', notebook=False)
```
![image](https://github.com/tparker48/codeweb/blob/main/screenshot.PNG)
