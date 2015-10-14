def application_to_dict(app):
    account = app.official_account
    return {
        'name': account.name,
        'description': account.description,
        'status': app.status,
        'operator_admin_name': app.operator_admin,
    }


def article_to_dict(article):
    account = article.offcial_account
    return {
        'title': article.title,
        'offcial_account_name': account.name,
        'offcial_account_id': account._id,
        'description': article.description
    }


def official_account_to_dict(account):
    return {
        'name': account.name,
        'subscriber': 0,
        'description': account.description
    }
