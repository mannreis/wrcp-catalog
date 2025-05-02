from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from textwrap import dedent
from pathlib import Path
import argparse
import json

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def generate_highlight_css(style="default"):
    # Generate the CSS using Pygments
    css = HtmlFormatter(style=style).get_style_defs('.source')

    # Return the CSS as a string
    return Markup(css)

def highlight_code(code, lexer_name="python"):
    lexer = get_lexer_by_name(lexer_name)
    formatter = HtmlFormatter(cssclass="source")
    return Markup(highlight(dedent(code), lexer, formatter))

def format_default_params(mlds):
    if descr := mlds.get("parameter_descriptions", {}):
        return "(" + ", ".join(f"{name}={d['default']!r}" for name, d in descr.items()) + ")"
    else:
        return ""

def format_raw_list(l):
    return ", ".join(f"{e!r}" for e in l)

def max_allowed_params(mlds):
    return {
        key: list(sorted(set(a for r in mlds["raw"].values() for a in r["allowed_parameters"][key])))
        for key in mlds.get("parameter_descriptions", {})
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mlds", type=Path, metavar="mlds.json"
    )
    parser.add_argument("outdir", type=Path, help="output folder")
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=select_autoescape(),
    )
    env.filters["highlight_css"] = generate_highlight_css
    env.filters["highlight"] = highlight_code
    env.filters["default_params"] = format_default_params
    env.filters["raw_list"] = format_raw_list

    mldss = json.load(open(args.mlds))

    template = env.get_template("index.html")

    with open(args.outdir / "index.html", "w") as outfile:
        outfile.write(template.render(mldss=mldss, sorted=sorted, max_allowed_params=max_allowed_params))

if __name__ == "__main__":
    main()