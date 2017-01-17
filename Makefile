XMLCFG=mtbls-dwnld_config.xml
CONDADIR=$(HOME)/w4m-conda

all:

test:
	$(MAKE) -C $@
	planemo lint $(XMLCFG)
	planemo conda_init --conda_prefix $(CONDADIR)
	planemo conda_install --conda_prefix $(CONDADIR) $(XMLCFG)
	planemo test --conda_prefix $(CONDADIR) --install_galaxy --galaxy_branch release_16.10 --conda_dependency_resolution $(XMLCFG)

clean:
	$(MAKE) -C test $@
	$(RM) -r $(HOME)/.planemo
	$(RM) -r $(CONDADIR)

.PHONY: clean all test
