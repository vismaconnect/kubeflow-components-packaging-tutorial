import kfp
import pkg_resources


multiply_op = kfp.components.load_component_from_text(
    pkg_resources.resource_string(__name__, 'yaml/multiply.yaml'))
