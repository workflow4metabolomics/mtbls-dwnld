TOOL_NAME=mtbls-dwnld
TOOL_XML=mtbls-dwnld.xml

all: isaslicer.py

isaslicer.py: isatools-galaxy/tools/isatools/isaslicer.py isaslicer.deps
	ln -sf $<

test: test-venv isaslicer.py
	. test-venv/bin/activate && $(MAKE) -C $@

isaslicer.deps: test-venv
	. test-venv/bin/activate && pip3 install pandas isatools
	. test-venv/bin/activate && python3 -c 'import pandas;import isatools'

test-venv:
	virtualenv -p python3 planemo-venv

planemo-venv/bin/planemo: planemo-venv
	. planemo-venv/bin/activate && pip install --upgrade pip setuptools
	. planemo-venv/bin/activate && pip install planemo

planemo-venv:
	virtualenv -p python2.7 planemo-venv

plint: planemo-venv/bin/planemo isaslicer.py
	. planemo-venv/bin/activate && planemo lint $(TOOL_XML)

ptest: planemo-venv/bin/planemo isaslicer.py
	. planemo-venv/bin/activate && planemo test --conda_dependency_resolution --galaxy_branch release_19.01 $(TOOL_XML)

ptesttoolshed_diff: dist/$(TOOL_NAME)/ planemo-venv/bin/planemo
	. planemo-venv/bin/activate && cd $< && planemo shed_diff --shed_target testtoolshed

dist/$(TOOL_NAME)/: isaslicer.py
	mkdir -p $@
	cp -r README.md $(TOOL_NAME) $(TOOL_NAME).xml test-data isaslicer.py $@

clean:
	$(MAKE) -C test $@
	$(RM) -r $(HOME)/.planemo
	$(RM) -r planemo-venv
	$(RM) -r test-venv
	$(RM) tool_test_output.*

.PHONY:	all clean test planemolint planemotest
