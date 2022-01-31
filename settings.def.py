SETTINGS = {
    "timezone": "Europe/Istanbul",
    "tmdb": {
        "api_key": "YOUR TMDB API KEY",
        "language": "tr",
    },
    "recaptcha": {
        "public_key": "YOUR RECAPTCHA PUBLIC KEY",
        "private_key": "YOUR RECAPTCHA PRIVATE KEY",
    },
    "email": {
        "username": "YOUR GOOGLE EMAIL ADDRESS",
        "password": "YOUR GOOGLE EMAIL PASSWORD",
    },
    "app_config": {
        "sqlalchemy_database_uri": "mysql+pymysql://{username}:{password}@{hostname}/{database}".format(
            username = "",
            password = "",
            hostname = "",
            database = "",
        ),
    },
    "debug": {
        "enabled": False,
        "session": {
            "account_username": "YOUR ACCOUNT USERNAME FOR DEBUG",
            "profile_username": "YOUR PROFILE USERNAME FOR DEBUG",
        },
    },
}
