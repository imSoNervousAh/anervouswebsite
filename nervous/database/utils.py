from backend import *

def build_test_db():
    Admin.create(username = 'wyl8899', password = 'xxxxxxxx')
    account = OfficialAccount.create(name = 'Lab Mu')
    Application.create(official_account = account, user_submit = 'FANG KUAI', status = 'not_submitted')
    account = OfficialAccount.create(name = 'Lab Mu\'s')
    Application.create(official_account = account, user_submit = 'GayLou', status = 'pending')
    
def clean_test_db():
    for model in [Admin, OfficialAccount, Application, Article]:
        model.all().delete()
