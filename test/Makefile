all: isatab2w4m mtbls-dwnld

isatab2w4m:
	./test-isatab2w4m
	./test-isatab2w4m $(CURDIR)/../isatab2w4m.py

mtbls-dwnld:
	./test-mtbls-dwnld

clean:
	$(RM) -r MTBLS* *.zip outputs

.PHONY: clean all
