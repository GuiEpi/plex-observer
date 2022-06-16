class Session:
    @classmethod
    def create(cls):
        self = Session()
        self.watchers = {}
        self.places = 2
        return self
    
    def add(self, watcher):
        self.watchers[watcher.name] = watcher
        self.places -= 1
    
    def delete(self, watcher):
        del self.watchers[watcher]
        self.places += 1
