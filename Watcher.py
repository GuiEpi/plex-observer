class Watcher:
    @classmethod
    def create(cls, name, title, status):
        self = Watcher()
        self.name = name
        self.title = title
        self.status = status
        return self