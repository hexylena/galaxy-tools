objects = blasr h5py pbalign pbcore pbdagcon pbh5tools plibblasr quiver hdf5

.PHONY: all clean $(objects)

all: $(objects)

$(objects):
	$(eval export PACKAGE_NAME = $@)
	$(MAKE) -C $@
