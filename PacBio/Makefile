CONVERTER:=../DepGen/convert.py
REPO_EXPORT:=../DepGen/from_git_repo.py
XMLLINT:=xmllint --pretty 1 -

objects = h5py/tool_dependencies.xml pbcore/tool_dependencies.xml pbalign/tool_dependencies.xml blasr/tool_dependencies.xml pbdagcon/tool_dependencies.xml pbh5tools/tool_dependencies.xml quiver/tool_dependencies.xml
archives = h5py.tgz pbcore.tgz pbalign.tgz blasr.tgz pbdagcon.tgz pbh5tools.tgz quiver.tgz
tool_deps: $(objects)
pacbio: $(archives)

h5py.tgz: h5py/tool_dependencies.xml
	tar -czf h5py.tgz -C h5py tool_dependencies.xml

pbcore.tgz: pbcore/tool_dependencies.xml
	tar -czf pbcore.tgz -C pbcore tool_dependencies.xml

pbalign.tgz: pbalign/tool_dependencies.xml
	tar -czf pbalign.tgz -C pbalign tool_dependencies.xml

blasr.tgz: blasr/tool_dependencies.xml
	tar -czf blasr.tgz -C blasr tool_dependencies.xml

pbdagcon.tgz: pbdagcon/tool_dependencies.xml
	tar -czf pbdagcon.tgz -C pbdagcon tool_dependencies.xml

pbh5tools.tgz: pbh5tools/tool_dependencies.xml
	tar -czf pbh5tools.tgz -C pbh5tools tool_dependencies.xml

quiver.tgz: quiver/tool_dependencies.xml
	tar -czf quiver.tgz -C quiver tool_dependencies.xml


h5py/tool_dependencies.xml:
	python ${CONVERTER} h5py/h5py.yaml | ${XMLLINT} > h5py/tool_dependencies.xml

pbcore/tool_dependencies.xml:
	python ${CONVERTER} pbcore/pbcore.yaml | ${XMLLINT} > pbcore/tool_dependencies.xml

pbalign/tool_dependencies.xml:
	python ${CONVERTER} pbalign/pbalign.yaml | ${XMLLINT} > pbalign/tool_dependencies.xml

blasr/tool_dependencies.xml:
	python ${CONVERTER} blasr/blasr.yaml | ${XMLLINT} > blasr/tool_dependencies.xml

pbdagcon/tool_dependencies.xml:
	python ${CONVERTER} pbdagcon/pbdagcon.yaml | ${XMLLINT} > pbdagcon/tool_dependencies.xml

pbh5tools/tool_dependencies.xml:
	python ${CONVERTER} pbh5tools/pbh5tools.yaml | ${XMLLINT} > pbh5tools/tool_dependencies.xml

quiver/tool_dependencies.xml: quiver/quiver.yaml
	python ${CONVERTER} quiver/quiver.yaml | ${XMLLINT} > quiver/tool_dependencies.xml


yaml_files = h5py/h5py.yaml pbcore/pbcore.yaml pbalign/pbalign.yaml blasr/blasr.yaml pbdagcon/pbdagcon.yaml pbh5tools/pbh5tools.yaml
# Experimental
pbcore/pbcore.yaml:
	python ${REPO_EXPORT} pbcore https://github.com/PacificBiosciences/pbcore > pbcore/pbcore.yaml

pbalign/pbalign.yaml:
	python ${REPO_EXPORT} pbalign https://github.com/PacificBiosciences/pbalign > pbalign/pbalign.yaml

blasr/blasr.yaml:
	python ${REPO_EXPORT} blasr https://github.com/PacificBiosciences/blasr > blasr/blasr.yaml

pbdagcon/pbdagcon.yaml:
	python ${REPO_EXPORT} pbdagcon https://github.com/PacificBiosciences/pbdagcon > pbdagcon/pbdagcon.yaml

pbh5tools/pbh5tools.yaml:
	python ${REPO_EXPORT} pbh5tools https://github.com/PacificBiosciences/pbh5tools > pbh5tools/pbh5tools.yaml

quiver/quiver.yaml:
	python ${REPO_EXPORT} quiver https://github.com/PacificBiosciences/GenomicConsensus > quiver/quiver.yaml



clean:
	@rm $(objects) $(archives)
