import os
import time
from pathlib import Path

from flask import Flask, Blueprint, request
from flask.helpers import send_from_directory
from jinja2 import FileSystemLoader
from babel import dates
from humanize import naturaltime
from markupsafe import Markup
from markdown import Markdown
from flask_caching import Cache

from chill import shortcodes
from chill import database


class ChillFlask(Flask):
    def send_root_file(self, filename):
        """
        Function used to send static files from the root of the domain.
        """
        max_age = self.get_send_file_max_age(filename)
        return send_from_directory(
            self.config["ROOT_FOLDER"], filename, max_age=max_age
        )

    def send_media_file(self, filename):
        """
        Function used to send media files from the media folder to the browser.
        """
        max_age = self.get_send_file_max_age(filename)
        return send_from_directory(
            self.config["MEDIA_FOLDER"], filename, max_age=max_age
        )

    def send_theme_file(self, filename):
        """
        Function used to send static theme files from the theme folder to the browser.
        """
        max_age = self.get_send_file_max_age(filename)
        return send_from_directory(
            self.config["THEME_STATIC_FOLDER"], filename, max_age=max_age
        )


def multiple_directory_files_loader(*args):
    """
    Loads all the files in each directory as values in a dict with the key
    being the relative file path of the directory.  Updates the value if
    subsequent file paths are the same.
    """
    d = dict()

    def load_files(folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                with open(filepath, "r") as f:
                    key = filepath[len(os.path.commonprefix([root, filepath])) + 1 :]
                    d[key] = f.read()
            for foldername in dirnames:
                load_files(os.path.join(dirpath, foldername))

    for root in args:
        load_files(root)
    return d


def make_app(config=None, database_readonly=False, **kw):
    "factory to create the app"

    app = ChillFlask("chill")

    if config:
        config_file = (
            config if config[0] == os.sep else os.path.join(os.getcwd(), config)
        )
        app.config.from_pyfile(config_file)
    app.config.update(kw, database_readonly=database_readonly)

    # Set the freezer destination path to be absolute if needed.
    freeze_folder = app.config.get("FREEZER_DESTINATION", None)
    if freeze_folder:
        if freeze_folder[0] != os.sep:
            freeze_folder = os.path.join(os.getcwd(), freeze_folder)

        app.config["FREEZER_DESTINATION"] = freeze_folder

    # TODO: fix conflict with page_uri
    root_folder = app.config.get("ROOT_FOLDER", None)
    if root_folder:
        if root_folder[0] != os.sep:
            root_folder = os.path.join(os.getcwd(), root_folder)

        app.config["ROOT_FOLDER"] = root_folder
        # root_path = '/' # See no need to have this be different
        if os.path.isdir(root_folder):
            app.add_url_rule("/<path:filename>", view_func=app.send_root_file)

    media_folder = app.config.get("MEDIA_FOLDER", None)
    if media_folder:
        if media_folder[0] != os.sep:
            media_folder = os.path.join(os.getcwd(), media_folder)

        app.config["MEDIA_FOLDER"] = media_folder
        media_path = app.config.get("MEDIA_PATH", "/media/")
        if os.path.isdir(media_folder) and media_path[0] == "/":
            app.add_url_rule(
                "%s<path:filename>" % media_path, view_func=app.send_media_file
            )

    document_folder = app.config.get("DOCUMENT_FOLDER", None)
    if document_folder:
        if document_folder[0] != os.sep:
            document_folder = os.path.join(os.getcwd(), document_folder)
        app.config["DOCUMENT_FOLDER"] = document_folder

    template_folder = app.config.get("THEME_TEMPLATE_FOLDER", app.template_folder)
    app.config["THEME_TEMPLATE_FOLDER"] = (
        template_folder
        if template_folder[0] == os.sep
        else os.path.join(os.getcwd(), template_folder)
    )

    queries_folder = app.config.get("THEME_SQL_FOLDER", "queries")
    app.config["THEME_SQL_FOLDER"] = (
        queries_folder
        if queries_folder[0] == os.sep
        else os.path.join(os.getcwd(), queries_folder)
    )

    chill_queries_folder = os.path.join(os.path.dirname(__file__), "queries")
    user_queries_folder = app.config.get("THEME_SQL_FOLDER")
    app.queries = multiple_directory_files_loader(
        chill_queries_folder, user_queries_folder
    )

    # Set the jinja2 template folder eith fallback for app.template_folder
    app.jinja_env.loader = FileSystemLoader(app.config.get("THEME_TEMPLATE_FOLDER"))

    app.logger.debug("Database init_app")
    database.init_app(app)

    cache = Cache(config=app.config)
    cache.init_app(app)

    # STATIC_URL='http://cdn.example.com/whatever/works/'
    @app.context_processor
    def inject_paths():
        """
        Inject the variables 'theme_static_path' and 'media_path' into the templates.

        Template variable will always have a trailing slash.

        """
        theme_static_path = app.config.get("THEME_STATIC_PATH", "/theme/")
        media_path = app.config.get("MEDIA_PATH", "/media/")
        # static_url = app.config.get('STATIC_URL', app.static_url_path)
        if not theme_static_path.endswith("/"):
            theme_static_path += "/"
        if not media_path.endswith("/"):
            media_path += "/"
        return dict(theme_static_path=theme_static_path, media_path=media_path)

    @app.context_processor
    def inject_config():
        """
        Inject the config into the templates.
        """
        return dict(config=dict(app.config))

    @app.context_processor
    def inject_chill_vars():
        """
        Inject some useful variables for templates to use.
        """
        return {"chill_now": int(time.time())}

    @app.template_filter("datetime")
    def datetime(value, format="y-MM-dd HH:mm:ss"):
        "Date time filter that uses babel to format."
        return dates.format_datetime(
            value, format, locale=app.config.get("LOCALE", "en")
        )

    @app.template_filter("timedelta")
    def timedelta(value):
        "time delta using humanize.time.naturaltime()"
        return naturaltime(value)

    # Add a custom markdown filter for the templates
    md = Markdown()
    @app.template_filter("markdown")
    def markdown(value):
        return Markup(md.convert(value))

    @app.template_filter("readfile")
    def readfile(filename):
        "A template filter to read files from the DOCUMENT_FOLDER"
        document_folder = app.config.get("DOCUMENT_FOLDER")
        if document_folder:
            # Restrict access to just the DOCUMENT_FOLDER.
            filepath = os.path.normpath(os.path.join(document_folder, filename))
            if os.path.commonprefix([document_folder, filepath]) != document_folder:
                app.logger.warn(
                    "The filepath: '{0}' is outside of the DOCUMENT_FOLDER".format(
                        filepath
                    )
                )
                return filename

            with open(os.path.join(document_folder, filename), "r") as f:
                # py2 return unicode str (not py3 compat)
                # content = f.read().decode('utf-8')

                # py3 (not py2 compat)
                # content = f.read()

                # py2 and py3 compat
                content = bytes(f.read(), "utf-8").decode("utf-8")
            return content
        else:
            app.logger.warning(
                "The DOCUMENT_FOLDER setting in site.cfg is not set to a value. Can't use 'readfile' filter."
            )
            return filename

        app.logger.warn(
            f"jinja2 filter 'readfile' can't find file: '{filename}' at DOCUMENT_FOLDER path: {document_folder}"
        )
        return filename

    # register any blueprints here
    # app.logger.warning("Not registering resource blueprint")
    # app.register_blueprint(resource)

    from chill.public import PageView

    # app.logger.warning("Not registering page blueprint")
    page = Blueprint("public", __name__, static_folder=None, template_folder=None)

    # TODO: The shortcode start and end is rather custom.  Make this
    # configurable or no?
    # The defualt from the shortcodes.py is '[%' and '%]'.
    app.parser = shortcodes.Parser(start="[chill", end="]", esc="\\")

    @app.template_filter("shortcodes")
    def shortcodes_filter(content):
        "Parse the rendered string for chill shortcodes"
        return Markup(app.parser.parse(content))

    theme_static_folder = app.config.get("THEME_STATIC_FOLDER", None)
    if theme_static_folder:
        if theme_static_folder[0] != os.sep:
            theme_static_folder = os.path.join(os.getcwd(), theme_static_folder)

        app.config["THEME_STATIC_FOLDER"] = theme_static_folder
        theme_static_path = app.config.get("THEME_STATIC_PATH", "/theme/")
        if os.path.isdir(theme_static_folder) and theme_static_path[0] == "/":
            app.add_url_rule(
                "%s<path:filename>" % theme_static_path, view_func=app.send_theme_file
            )

    def not_get(view, *args, **kwargs):
        return request.method != "GET"

    def page_cache_filter(rv):
        return rv.status_code == 200

    pageview = PageView.as_view("page")
    pageview = cache.cached(unless=not_get, query_string=True, response_filter=page_cache_filter)(pageview)
    page.add_url_rule("/", view_func=pageview)

    pageindexview = PageView.as_view("index")
    pageindexview = cache.cached(unless=not_get, query_string=True, response_filter=page_cache_filter)(pageindexview)
    page.add_url_rule("/index.html", view_func=pageindexview)

    pageuriview = PageView.as_view("page_uri")
    pageuriview = cache.cached(unless=not_get, query_string=True, response_filter=page_cache_filter)(pageuriview)
    page.add_url_rule("/<path:uri>/", view_func=pageuriview)

    pageuriindexview = PageView.as_view("uri_index")
    pageuriindexview = cache.cached(unless=not_get, query_string=True, response_filter=page_cache_filter)(pageuriindexview)
    page.add_url_rule("/<path:uri>/index.html", view_func=pageuriindexview)

    app.register_blueprint(page, url_prefix=app.config.get("PUBLIC_URL_PREFIX", ""))

    if app.config.get("reload"):
        reload_extra_files = []
        for item in filter(
            None,
            [
                chill_queries_folder,
                user_queries_folder,
                document_folder,
                template_folder,
            ],
        ):
            reload_extra_files.extend(map(str, Path(item).glob("**/*")))
        app.config["reload_extra_files"] = reload_extra_files

    return app
