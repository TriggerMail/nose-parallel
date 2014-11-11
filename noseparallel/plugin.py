import os
import logging
from nose.plugins.base import Plugin

log = logging.getLogger('nose.plugin.parallel')

class ParallelPlugin(Plugin):
    name = 'parallel'

    def configure(self, options, config):
        super(ParallelPlugin, self).configure(options, config)
        self.total_nodes = int(os.environ.get('CIRCLE_NODE_TOTAL') or os.environ.get('NODE_TOTAL', 1))
        self.node_index = int(os.environ.get('CIRCLE_NODE_INDEX') or os.environ.get('NODE_INDEX', 0))

    def wantMethod(self, method):
        if not method.__name__.lower().startswith("test"):
            return None
        try:
            cls = method.im_class
            if not cls.__name__.lower().startswith("test"):
                return None
            return self._pick_by_hash("%s.%s" % (cls.__name__, method.__name__))
        except AttributeError:
            return None
        return None

    def _pick_by_hash(self, name):
        class_numeric_id = abs(hash(name))
        if class_numeric_id % self.total_nodes == self.node_index:
            return None
        return False
