from djongo.base import DatabaseWrapper

class PatchedDatabaseWrapper(DatabaseWrapper):
    def _close(self):
        if self.connection is not None:
            super()._close()