from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import argparse
import json

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

    mldss = json.load(open(args.mlds))

    template = env.get_template("index.html")

    with open(args.outdir / "index.html", "w") as outfile:
        outfile.write(template.render(mldss=mldss))

if __name__ == "__main__":
    main()