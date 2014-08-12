CONVERTER:=DepGen/convert.py
pacbio: PacBio/blasr/tool_dependencies.xml PacBio/pbalign/tool_dependencies.xml

clean:
	@rm -f PacBio/blasr/tool_dependencies.xml PacBio/pbalign/tool_dependencies.xml

PacBio/blasr/tool_dependencies.xml:
	python ${CONVERTER} PacBio/blasr/blasr.yaml |xmllint --pretty 1 -  > PacBio/blasr/tool_dependencies.xml

PacBio/pbalign/tool_dependencies.xml:
	python ${CONVERTER} PacBio/pbalign/pbalign.yaml |xmllint --pretty 1 -  > PacBio/pbalign/tool_dependencies.xml

