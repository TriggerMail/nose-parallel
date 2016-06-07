from nose.plugins.base import Plugin
from operator import itemgetter
import logging
import os

log = logging.getLogger('nose.plugin.parallel')

class ParallelPlugin(Plugin):
    name = 'parallel'

    def configure(self, options, config):
        super(ParallelPlugin, self).configure(options, config)
        self.total_nodes = int(os.environ.get('CIRCLE_NODE_TOTAL') or os.environ.get('NODE_TOTAL', 1))
        self.node_index = int(os.environ.get('CIRCLE_NODE_INDEX') or os.environ.get('NODE_INDEX', 0))

    def wantMethod(self, method):
        if not method.__name__.lower().startswith("test"):
            return False
        try:
            cls = method.im_class
            if not cls.__name__.lower().startswith("test"):
                return False
            return self._pick_by_hash("%s.%s" % (cls.__name__, method.__name__))
        except AttributeError:
            return None
        return None

    def _pick_by_hash(self, name):
        node_loads = [int(os.environ.get("NODE_LOAD_%d" % i)) or 0 for i in xrange(self.total_nodes)]
        min_load_index = min(enumerate(node_loads), key=itemgetter(1))[0]
        os.environ['NODE_LOAD_%d' % min_load_index] = str(int(os.environ.get("NODE_LOAD_%d" % i)) + 1)
        if min_load_index == self.node_index:
            return True
        return False
