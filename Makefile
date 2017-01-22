XMLCFG=mtbls-dwnld_config.xml
CONDADIR=$(HOME)/w4m-conda

all:

test: plaintest planemolint planemotest

planemotest: conda
	planemo test --conda_prefix $(CONDADIR) --install_galaxy --galaxy_branch release_16.10 --conda_dependency_resolution $(XMLCFG)

$(CONDADIR):
	planemo conda_init --conda_prefix $(CONDADIR)

conda: $(CONDADIR)
	planemo conda_install --conda_prefix $(CONDADIR) $(XMLCFG)

planemolint:
	planemo lint $(XMLCFG)

plaintest:
	$(MAKE) -C test

clean:
	$(MAKE) -C test $@
	$(RM) -r $(HOME)/.planemo
	$(RM) -r $(CONDADIR)

.PHONY: clean all test plaintest planemolint planemotest conda
