from setuptools import setup

setup(
    name='mkdocs-plugin-redact',
    version='0.1',
    description='MkDocs plugin to redact marked sections in Markdown files',
    packages=['plugin_redact'],
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'redact = plugin_redact:RedactPlugin',
        ],
    },
    install_requires=[
        'mkdocs>=1.0',
    ],
)
