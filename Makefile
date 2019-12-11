all:

test: 
	$(MAKE) -C $@

planemo-venv/bin/planemo: planemo-venv
	. planemo-venv/bin/activate && pip install --upgrade pip setuptools
	. planemo-venv/bin/activate && pip install planemo

planemo-venv:
	virtualenv planemo-venv

planemolint: planemo-venv/bin/planemo
	. planemo-venv/bin/activate && planemo lint

planemotest: planemo-venv/bin/planemo
	. planemo-venv/bin/activate && planemo test --conda_dependency_resolution --galaxy_branch release_19.01

clean:
	$(MAKE) -C test $@
	$(RM) -r $(HOME)/.planemo
	$(RM) -r planemo-venv
	$(RM) tool_test_output.*

.PHONY:	all clean test planemolint planemotest
