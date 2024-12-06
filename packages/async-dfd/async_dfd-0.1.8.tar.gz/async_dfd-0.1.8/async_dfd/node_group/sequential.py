import logging

from .pipeline import Pipeline

logger = logging.getLogger(__name__)


class Sequential(Pipeline):
    def _connect_nodes(self):
        former = None
        for node in self.all_nodes.values():
            if former is None:
                former = node
                continue
            else:
                logger.info(f"connect {former.__name__} to {node.__name__}")
                former.connect(node)
                former = node
