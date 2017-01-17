all:

test:
	$(MAKE) -C $@

clean:
	$(MAKE) -C test $@

.PHONY: clean all test
