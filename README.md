# Website source

Source code for my personal website. This iteration uses [mkdocs][].

[mkdocs]: https://www.mkdocs.org/

## Building

```
$ pip install -r requirements.txt
$ invoke build
```

The `build` and `serve` commands will first generate `mkdocs.yml` from the
template `mkdocs.yml.in` by extracting metadata from all blog entries.
Non-static pages currently have to be added to the navigation by hand.

## License

Unless otherwise indicated, web site content is available under the [Creative
Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license](https://creativecommons.org/licenses/by-sa/4.0/).
