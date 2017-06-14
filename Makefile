XMLCFG=mtbls-dwnld_config.xml
CONDADIR=$(HOME)/w4m-conda
VENV=$(HOME)/planemo-venv
ACTIVATE_VENV=$(VENV)/bin/activate

all:

test: plaintest planemolint planemotest

planemotest: conda
	. $(ACTIVATE_VENV) && planemo test --conda_prefix $(CONDADIR) --install_galaxy --galaxy_branch release_16.10 --conda_dependency_resolution $(XMLCFG)

$(VENV):
	virtualenv $@

$(CONDADIR): planemo-install
	. $(ACTIVATE_VENV) && planemo conda_init --conda_prefix $(CONDADIR)

planemo-install: $(VENV)
	. $(ACTIVATE_VENV) && pip install --upgrade pip setuptools
	. $(ACTIVATE_VENV) && pip install planemo

conda: $(CONDADIR)
	. $(ACTIVATE_VENV) && planemo conda_install --conda_prefix $(CONDADIR) $(XMLCFG)

planemolint: planemo-install
	. $(ACTIVATE_VENV) && planemo lint $(XMLCFG)

plaintest:
	$(MAKE) -C test

clean:
	$(MAKE) -C test $@
	$(RM) -r $(HOME)/.planemo
	$(RM) -r $(CONDADIR)
	$(RM) -r $(VENV)

.PHONY: clean all test plaintest planemolint planemotest conda planemo-install
