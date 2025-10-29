"""Sphinx 配置文件.

FireShot 项目 API 文档自动生成配置。
"""

import os
import sys
from datetime import datetime


# -- 路径设置 -----------------------------------------------------------------

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.abspath("../.."))

# -- 项目信息 -----------------------------------------------------------------

project = "FireShot"
copyright = f"{datetime.now().year}, HawaiiHub AI Team"
author = "HawaiiHub AI Team"
version = "1.0"
release = "1.0.2"

# -- 通用配置 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",  # 自动从 docstring 生成文档
    "sphinx.ext.napoleon",  # 支持 Google/NumPy 风格的 docstring
    "sphinx.ext.viewcode",  # 添加源码链接
    "sphinx.ext.todo",  # TODO 扩展
    "sphinx.ext.coverage",  # 文档覆盖率检查
    "sphinx.ext.intersphinx",  # 跨项目链接
    "sphinx.ext.githubpages",  # GitHub Pages 支持
    "myst_parser",  # Markdown 支持
]

# 源文件后缀
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# 主文档
master_doc = "index"

# 语言设置
language = "zh_CN"

# 排除模式
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
]

# -- HTML 输出配置 ------------------------------------------------------------

html_theme = "sphinx_rtd_theme"  # Read the Docs 主题
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

html_title = "FireShot 文档"
html_short_title = "FireShot"
html_logo = None
html_favicon = None

# 自定义侧边栏
html_sidebars = {
    "**": [
        "globaltoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
    ]
}

# 静态文件目录
html_static_path = ["_static"]

# -- autodoc 配置 -------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# -- Napoleon 配置 ------------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# -- Intersphinx 配置 ---------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}

# -- MyST 配置 ----------------------------------------------------------------

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- TODO 配置 ----------------------------------------------------------------

todo_include_todos = True
todo_emit_warnings = False
