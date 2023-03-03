from app.models import Setting, SettingType


general_settings = {
    "siteTitle": "My Awesome Blog website",
    "siteLanguage": "en",
    "adminEmail": "admin@example.com",
    "numberOfPostsOnBlogPage": 10,
    "includeOnBlogPagePosts": "excerpt",
    "dateFormat": "%d %b, %Y",
    "timeFormat": "%H:%M",
}


def register_general_settings():
    print("Installing general settings ....")

    for k, v in general_settings.items():
        setting = Setting(name=k, value=v, type=SettingType.GENERAL)
        if not setting.exists():
            setting.save()
        else:
            print(f"{k} already exists...")
