class Session:
    @classmethod
    def create(cls):
        self = Session()
        self.watchers = {}
        return self
    
    def add(self, watcher):
        self.watchers[watcher.name] = watcher
    
    def delete(self, watcher):
        del self.watchers[watcher]