from nose.plugins.base import Plugin
import logging
import os

log = logging.getLogger('nose.plugin.parallel')

class ParallelPlugin(Plugin):
    name = 'parallel'

    def configure(self, options, config):
        super(ParallelPlugin, self).configure(options, config)
        self.total_nodes = int(os.environ.get('CIRCLE_NODE_TOTAL') or os.environ.get('NODE_TOTAL', 1))
        self.node_index = int(os.environ.get('CIRCLE_NODE_INDEX') or os.environ.get('NODE_INDEX', 0))
        self.current_test_number = 0

    def wantMethod(self, method):
        if not method.__name__.lower().startswith("test"):
            return False
        try:
            cls = method.im_class
            if not cls.__name__.lower().startswith("test"):
                return False
        except AttributeError:
            return None
        # Every node gets the same number of tests.
        will_be_executed = self.node_index == self.current_test_number % self.total_nodes
        self.current_test_number += 1
        return will_be_executed
