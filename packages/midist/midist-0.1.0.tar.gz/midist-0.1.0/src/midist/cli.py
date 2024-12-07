import os
import urllib.parse
import json

import typer
from jinja2 import Template

from .generate import process_file
from . import __version__

app = typer.Typer()

pl_th_list_tmpl = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ tmpl_type }} List</title>
    <meta name="generator" content="AmaseCocoa/MiDist (v{{ __version__ }})">
</head>
<body>
    {% if tmpl_type == "Theme" %}
        <h1>Themes</h1>
        {% if themes != [] %}
            {% for theme in themes %}
                <div class="theme-container">
                    <a href="{{ theme["link"] }}">{{ theme["name"] }}</a>
                </div>
            {% endfor %}
        {% endif %}
    {% elif tmpl_type == "Plugin" %}
        <h1>Plugins</h1>
        {% if plugins != [] %}
            {% for plugin in plugins %}
                <div class="plugin-container">
                    <a href="{{ plugin["link"] }}">{{ plugin["name"] }}</a>
                </div>
            {% endfor %}
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.command(name="generate")
def generate(base_url: str, dir: str = "./"):
    if not os.path.exists(dir):
        print(f"指定したディレクトリは存在しません: {dir}")
        return

    themes = []
    plugins = []

    api_dir = os.path.join(dir, "api")
    themes_dir = os.path.join(api_dir, "themes")
    plugins_dir = os.path.join(api_dir, "plugins")

    os.makedirs(themes_dir, exist_ok=True)
    os.makedirs(plugins_dir, exist_ok=True)

    def process_themes(base_dir):
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                single_line, file_hash = process_file(file_path)
                
                # 相対パスを取得
                relative_path = os.path.relpath(file_path, start=base_dir)
                json_dir = os.path.dirname(relative_path)  # ディレクトリ部分を取得
                
                # JSONファイル保存先を決定
                json_file_path = os.path.join(themes_dir, json_dir)
                os.makedirs(json_file_path, exist_ok=True)

                theme_name = os.path.splitext(os.path.basename(file_path))[0]
                
                # リンクをbase_urlを基に生成
                themes.append(
                    {
                        "name": theme_name,
                        "link": f"https://misskey-hub.net/mi-web?path={urllib.parse.quote(f"/install-extensions?url={base_url}/api/themes/{json_dir}/{theme_name}.json&hash={file_hash}")}",
                    }
                )

                with open(os.path.join(json_file_path, f"{theme_name}.json"), "w") as f:
                    json.dump(
                        {"type": "theme", "data": single_line},
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )

    def process_plugins(base_dir):
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                single_line, file_hash = process_file(file_path)
                
                # 相対パスを取得
                relative_path = os.path.relpath(file_path, start=base_dir)
                json_dir = os.path.dirname(relative_path)  # ディレクトリ部分を取得
                
                # JSONファイル保存先を決定
                json_file_path = os.path.join(plugins_dir, json_dir)
                os.makedirs(json_file_path, exist_ok=True)

                plugin_name = os.path.splitext(os.path.basename(file_path))[0]
                
                # リンクをbase_urlを基に生成
                plugins.append(
                    {
                        "name": plugin_name,
                        "link": f"https://misskey-hub.net/mi-web?path={urllib.parse.quote(f"{base_url}/api/plugins/{json_dir}/{plugin_name}.json?hash={file_hash}")}",
                    }
                )

                with open(os.path.join(json_file_path, f"{plugin_name}.json"), "w") as f:
                    json.dump(
                        {"type": "plugin", "data": single_line},
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )

    process_themes(os.path.join(dir, "themes"))
    process_plugins(os.path.join(dir, "plugins"))

    # HTMLテンプレートの生成
    template = Template(source=pl_th_list_tmpl)
    with open(os.path.join(themes_dir, "index.html"), "w") as f:
        f.write(
            template.render(themes=themes, tmpl_type="Theme", __version__=__version__)
        )
    with open(os.path.join(plugins_dir, "index.html"), "w") as f:
        f.write(
            template.render(
                plugins=plugins, tmpl_type="Plugin", __version__=__version__
            )
        )

def main():
    return app()
