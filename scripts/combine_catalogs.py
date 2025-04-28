import argparse
from dataclasses import asdict, dataclass, field
from pathlib import Path
import yaml
from jinja2 import Template


@dataclass
class DataSource:
    driver: str
    args: dict
    description: str = field(default_factory=str)
    parameters: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def __or__(self, other: "DataSource | None") -> "DataSource":
        if other is None:
            return self
        assert isinstance(other, DataSource)
        return other

    def __ror__(self, other: None) -> "DataSource":
        assert other is None
        return self


@dataclass
class SimpleCat:
    sources: dict[str, "SimpleCat | DataSource"]
    location: Path | None = None
    description: str | None = None

    def __or__(self, other: "SimpleCat | None") -> "SimpleCat":
        if other is None:
            return self
        assert isinstance(other, SimpleCat)
        keys = set(self.sources) | set(other.sources)
        return SimpleCat({k: self.sources.get(k) | other.sources.get(k) for k in keys})

    def __ror__(self, other: None) -> "SimpleCat":
        assert other is None
        return self

    def to_entry(self, name) -> dict:
        res = {
            "driver": "yaml_file_cat",
            "args": {"path": f"{{{{CATALOG_DIR}}}}/{name}/catalog.yaml"},
        }
        if self.description:
            res["description"] = self.description
        return res


def parse_source(source: dict, path: Path) -> SimpleCat | DataSource:
    assert source["driver"] in ["yaml_file_cat", "zarr"]
    if source["driver"] == "yaml_file_cat":
        return read_cat(
            Path(Template(source["args"]["path"]).render(CATALOG_DIR=str(path.parent)))
        )
    else:
        return DataSource(**source)


def read_cat(path: Path) -> SimpleCat:
    cat = yaml.safe_load(open(path))
    assert set(cat) == {
        "sources"
    }, f"can't handle catalogs which not only have sources: '{ path }'"
    return SimpleCat(
        sources={k: parse_source(v, path) for k, v in cat["sources"].items()},
        location=path.parent,
    )


def write_cat(cat: SimpleCat, path: Path) -> None:
    sources = {
        k: asdict(v) if isinstance(v, DataSource) else v.to_entry(k)
        for k, v in cat.sources.items()
    }
    path.mkdir(parents=True, exist_ok=True)
    with open(path / "catalog.yaml", "w") as outfile:
        yaml.dump({"sources": sources}, outfile)

    for k, v in cat.sources.items():
        if isinstance(v, SimpleCat):
            write_cat(v, path / k)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "zones_file", type=Path, help="availability zone definition file"
    )
    parser.add_argument("outdir", type=Path, help="output folder")
    args = parser.parse_args()

    basedir = args.zones_file.absolute().parent
    outdir = args.outdir
    zones = yaml.safe_load(open(args.zones_file))
    cat = read_cat(basedir / "catalog.yaml")

    for zone, sources in zones.items():
        c = None
        for source in sources:
            c |= cat.sources[source]
        d = outdir / zone
        write_cat(c, d)

    with open(outdir / "catalog.yaml", "w") as outfile:
        yaml.dump(
            {
                "sources": {
                    zone: {
                        "driver": "yaml_file_cat",
                        "args": {"path": f"{{{{CATALOG_DIR}}}}/{zone}/catalog.yaml"},
                        "description": f"catalog as visible from {zone}",
                    }
                    for zone in zones
                }
            },
            outfile,
        )


if __name__ == "__main__":
    main()
