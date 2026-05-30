MODE = None
NAME = v52
all:
ifneq ($(NAME), v52)
	@(find . -type f -name "*" -print0 | xargs -0 sed -i'' -e "s/v52/$(NAME)/g")
	@(mv v52/v52.tex v52/$(NAME).tex)
	@(mv v52 $(NAME))
endif
	$(MAKE) -C $(NAME) MODE=$(MODE)
	cp $(NAME)/build/tex/$(NAME).pdf $(NAME)_rosenbaum_hikade.pdf

plots:
	$(MAKE) -C $(NAME) plot

clean:
	$(MAKE) -C $(NAME) clean

.PHONY: all clean
