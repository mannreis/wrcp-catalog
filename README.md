# catalog

This repo contains data catalogs for the [Digital Earths Global Hackathon](https://digital-earths-global-hackathon.github.io/hk25/).

From a user point of view, it's best to think of **one** single catalog, covering all datasets available for the hackathon.
Now, depending on where you want to access data from, a given dataset might be better reachable using a local path, instead of a global URL.
In order to facilitate usage, we technically provide one catalog per *usage* site.
Users should select the most appropriate catalog (either manually or automatically), based on where they execute an analysis.

## source catalogs and usable catalogs

We distinguish between two sets of catalogs:

* provider catalogs
* usable catalogs

**Provider** catalogs are the "source code": it's once catalog per data providing location, and should be edited by the people providing a given dataset (instance).

**Usable** catalogs are the "compiled code": based on the file `availability_zones.yaml`, multiple provider catalogs are combined into catalogs showing all the entries which can be reached from a given site. E.g. at `EU`, we might have access to all data stored locally at the `EU` node, as well as all data available `online`. Thus these two catalogs are combined.