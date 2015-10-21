def application_to_dict(app):
    account = app.official_account
    return {
        'id': account.id,
        'name': account.name,
        'description': account.description,
        'manager_name': app.manager_name,
        'status': app.status,
        'operator_admin_name': app.operator_admin,
    }


def article_to_dict(article):
    id = article.official_account_id
    account = OfficialAccount.get(pk=id)
    return {
        'title': article.title,
        'official_account_name': account.name,
        'official_account_id': id,
        'description': article.description,
        'views': article.views,
        'likes': article.likes,
        'avatar_url': article.avatar_url,
        'url': article.url
    }


def official_account_to_dict(account):
    return {
        'name': account.name,
        'subscriber': 0,
        'description': account.description
    }
