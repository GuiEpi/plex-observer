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
    
    def __delete(self, watcher):
        del self.watchers[watcher]
        self.places += 1
    
    def watch_disconnected_users(self, users):
        disconnected_user = []
        for watcher in self.watchers.keys():
            if watcher not in users:
                disconnected_user.append(watcher)
                self.__delete(watcher)
            return disconnected_user
