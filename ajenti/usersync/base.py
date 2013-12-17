from ajenti.api import *


@interface
class UserSyncProvider (BasePlugin):
    allows_renaming = False
    
    def test(self):
        return False

    def check_password(self, username, password):
        return False

    def sync(self):
        pass