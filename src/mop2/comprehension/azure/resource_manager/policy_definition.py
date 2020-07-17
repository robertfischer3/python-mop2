
class PolicyDefinition:
    def get(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def batch_create(self):
        raise NotImplementedError