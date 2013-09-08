from webtranslate.bottle import route, template, abort, redirect, request
from webtranslate.protect import protected
from webtranslate import config, data, utils
from webtranslate.newgrf import language_info

@route('/newlanguage/<prjname>', method = 'GET')
@protected(['newlanguage', 'prjname', '-'])
def new_language_get(user, prjname):
    """
    Form to add another language to the project.
    """
    pmd = config.cache.get_pmd(prjname)
    if pmd is None:
        abort(404, "Project does not exist")
        return

    pdata = pmd.pdata

    base_langs = []
    translations = []
    can_be_added = []
    for lang in language_info.all_languages:
        if lang.isocode == pdata.base_language:
            base_langs.append(lang)
            continue
        if lang.isocode in pdata.languages:
            translations.append(lang)
            continue
        can_be_added.append(lang)

    translations.sort(key=lambda x: x.isocode)
    can_be_added.sort(key=lambda x: x.isocode)

    return template('newlanguage', proj_name = prjname, pdata = pdata, base_langs = base_langs,
                    translations = translations, can_be_added = can_be_added)

@route('/newlanguage/<prjname>', method = 'POST')
@protected(['newlanguage', 'prjname', '-'])
def new_language_post(user, prjname):
    """
    Construct the requested language.
    """
    pmd = config.cache.get_pmd(prjname)
    if pmd is None:
        abort(404, "Project does not exist")
        return

    pdata = pmd.pdata
    new_iso = request.forms.language_select
    for lang in language_info.all_languages:
        if lang.isocode == new_iso:
            if lang.isocode in pdata.languages:
                abort(404, "Language \"{}\" already exists".format(lang.isocode))
                return

            # Create the language.
            lng = data.Language(lang.isocode)
            lng.grflangid = lang.grflangid
            lng.plural = lang.plural
            lng.gender = lang.gender
            lng.case = lang.case
            lng.case.sort()

            pdata.languages[lng.name] = lng

            config.cache.save_pmd(pmd)
            pmd.create_statistics(lng)

            msg = "Successfully created language '" + lng.name +"' " + utils.get_datetime_now_formatted()
            redirect("/translation/{}/{}?message={}".format(prjname, lng.name, msg))
            return

    msg = "No language found that should be created"
    abort(404, msg)
    return
