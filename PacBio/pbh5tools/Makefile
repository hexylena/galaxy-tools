PACKAGE_REPO:="https://github.com/PacificBiosciences/pbh5tools"
CONVERTER:=../../DepGen/convert.py
REPO_EXPORT:=../../DepGen/from_git_repo.py
XMLLINT:=xmllint --pretty 1 -

.PHONY: clean all

all: archive tool_dependencies.xml

archive: tool_dependencies.xml
	$(eval PACKAGE_VERSION := $(shell xpath -e '//tool_dependency/package/install/../@version' -q tool_dependencies.xml | sed 's/^[^"]*"//g;s/"//g'))
	tar -czf $(PACKAGE_NAME)_$(PACKAGE_VERSION).tgz tool_dependencies.xml

tool_dependencies.xml: $(PACKAGE_NAME).yaml
	python ${CONVERTER} $(PACKAGE_NAME).yaml | ${XMLLINT} > tool_dependencies.xml

$(PACKAGE_NAME).yaml:
	python ${REPO_EXPORT} $(PACKAGE_NAME) $(PACKAGE_REPO) > $(PACKAGE_NAME).yaml

clean:
	$(eval PACKAGE_VERSION := $(shell xpath -e '//tool_dependency/package/install/../@version' -q tool_dependencies.xml | sed 's/^[^"]*"//g;s/"//g'))
	@rm -f $(PACKAGE_NAME)_$(PACKAGE_VERSION).tgz 
	@rm -f tool_dependencies.xml
