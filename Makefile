.PHONY: install run debug build clean fclean lint lint-strict test

build:
	poetry build -f wheel -o .

clean:
	rm -f mazegen-*
