all:

test: 
	$(MAKE) -C test

planemotest:
	planemo test --install_galaxy --galaxy_branch 17.01 --conda_dependency_resolution

$(VENV):
	virtualenv $@

$(CONDADIR): planemo-install
	. $(ACTIVATE_VENV) && planemo conda_init --conda_prefix $(CONDADIR)

planemo-install: $(VENV)
	. $(ACTIVATE_VENV) && pip install --upgrade pip setuptools
	. $(ACTIVATE_VENV) && pip install planemo==$(PLANEMO_VERSION)

conda: $(CONDADIR)
	. $(ACTIVATE_VENV) && planemo conda_install --conda_prefix $(CONDADIR) $(XMLCFG)

planemolint:
	planemo lint

plaintest:

clean:
	$(MAKE) -C test $@
	$(RM) -r $(HOME)/.planemo
	$(RM) -r $(CONDADIR)
	$(RM) -r $(VENV)

.PHONY: clean all test plaintest planemolint planemotest conda planemo-install
