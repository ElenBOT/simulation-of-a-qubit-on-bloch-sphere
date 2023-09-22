"""
Setting version
Check change log, and return the path.
"""

_CHANGELOG_TEMPLATE = """# Title
* line1
* line2
* line3
"""

INSERT_POINTS = [
    'github_release',
    'version',
]

class Insert:
    """Replace file content"""
    def __init__(self, file_text):
        self.text = file_text
    def insert_content(self, insert_point, content):
        """Insert the content to insert point"""
        full_point = f'{{{{insert_point.{insert_point}}}}}'
        self.text = self.text.replace(full_point, content)
    def get_file_text(self):
        """return file text"""
        return self.text


if __name__ == '__main__':
    import tomllib
    from os.path import exists
    from os import mkdir

    # get version from pyproject.toml
    with open("pyproject.toml", "rb") as f:
        parsed_toml = tomllib.load(f)
    version = parsed_toml['project']['version']

    # check change log
    logdir = "./docs/changelogs"
    filepath = f"{logdir}/changelog_{version}.md"
    if not exists(logdir):
        mkdir(logdir)
    if not exists(filepath):
        with open(filepath, 'x', encoding='utf-8') as f:
            f.write(_CHANGELOG_TEMPLATE)

    # Create readme.md
    with open("docs/README_repo.md", "r", encoding='utf-8') as f:
        file_obj = Insert(f.read())
    # point 0
    content_p0 = f"[Release {version}](https://github.com/ElenBOT/simulation-of-a-qubit-on-bloch-sphere/releases/tag/{version})"
    file_obj.insert_content(INSERT_POINTS[0], content_p0)
    # point 1
    content_p1 = f"{version}"
    file_obj.insert_content(INSERT_POINTS[1], content_p1)
    with open("README.md", "w", encoding='utf-8') as f:
        f.write(file_obj.get_file_text())

    # returns
    print(version, filepath)
