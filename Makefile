XMLCFG=isatab.xml
CONDADIR=$(HOME)/w4m-conda

all:

test:
	$(MAKE) -C $@
	planemo lint $(XMLCFG)
	planemo conda_init --conda_prefix $(CONDADIR)
	planemo conda_install --conda_prefix $(CONDADIR) $(XMLCFG)
	planemo test --conda_prefix $(CONDADIR) --galaxy_branch release_16.07 --conda_dependency_resolution $(XMLCFG)

clean:
	$(MAKE) -C test $@

.PHONY: clean all test
