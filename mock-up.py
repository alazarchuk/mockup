import sys

class MockUpImportError(Exception):
    pass

class LazyImporter(object):
    """Lazy importer"""

    def __init__(self, top_path, module_name):
        self.__name__ = top_path + '.' + module_name

    def __getattr__(self, name):
        try:
            mod = sys.modules[self.__name__ + '.' + name]
        except KeyError:
            raise MockUpImportError('Module `%s` wasn\'t mockuped' % (self.__name__ + '.' + name))

        return mod

def MockUpImporter(top_level_module, mockups):
    """Set mockups

    :param top_level_module: full import path to top level module
    :param mockups: dict where key is module path relative to
                    `top_level_module_name` and value mockup
                    for that function
    """
    for mname in mockups:
        mp = [top_level_module] + mname.split('.')
        path_parts = [(mp[i-1],
                       '.'.join(mp[:i-1]),
                       '.'.join(mp[:i]))
                             for i in range(2, len(mp))]

        full_mod_path = top_level_module
        for mod_name, top_module_path, full_mod_path in path_parts:
            if not sys.modules.has_key(full_mod_path):
                sys.modules[full_mod_path] = LazyImporter(top_module_path, mod_name)
                setattr(sys.modules[top_module_path], mod_name, LazyImporter(top_module_path, mod_name))

        sys.modules[top_level_module + '.' + mname] = mockups[mname]
        setattr(sys.modules[full_mod_path], mp[-1], mockups[mname])

