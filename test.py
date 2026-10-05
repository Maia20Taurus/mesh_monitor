import pkgutil
import importlib

def import_submodules(package_name):
    """Import all submodules of a package, recursively."""
    # Source: https://www.tutorialspoint.com/article/how-do-i-import-all-the-submodules-of-a-python-namespace-package
    if isinstance(package_name, str):
        package = importlib.import_module(package_name)
    else:
        package = package_name
        package_name = package.__name__
    
    results = {}
    
    # Check if package has __path__ (required for pkgutil.iter_modules)
    if not hasattr(package, '__path__'):
        return results
    
    for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package_name + '.'):
        try:
            results[name] = importlib.import_module(name)
            
            # Recursively import subpackages
            if is_pkg:
                results.update(import_submodules(name))
        except ImportError as e:
            print(f"Failed to import {name}: {e}")
            
    return results

# Example usage with a standard package
modules = import_submodules('portnums')
print("Imported modules:", list(modules.keys()))
print("*"*30)
print(modules)
