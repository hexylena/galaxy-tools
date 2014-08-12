# Tool Dependency Generator

Writing XML is unpleasant, writing YAML isn't. Very much in-development tool to automatically generate `tool_dependencies.xml` files from a yaml definition file, ensuring that repositories can be easier to load into galaxy.

```bash
python convert.py blat.yaml |xmllint --pretty 1 -  > blat.xml
diff blat.xml blat_ref.xml
```
