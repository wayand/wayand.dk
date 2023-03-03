from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Setting, SettingType
from app.admin import bp, Page


@bp.route("/settings", methods=("GET", "POST"))
@login_required
def settings_general():
    page = Page(
        can_show_component_new=False,
        title="General Settings",
        h1="General Settings",
    )
    general_settings = Setting.query.filter_by(type=SettingType.GENERAL).all()
    general_settings = {setting.name: setting for setting in general_settings}

    if request.method == "POST":
        for setting_name, setting_obj in general_settings.items():
            if request.form.get(setting_name):
                setting_obj.value = request.form[setting_name]
                setting_obj.update()

        flash("Settings updated", "success")
        return redirect(url_for("admin.settings_general"))

    return render_template(
        "admin/settings/general.html", page=page, settings=general_settings
    )
