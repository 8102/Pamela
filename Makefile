CC		=	gcc

RM		=	rm -rf

NAME		=	pamela.so

SRC		=	pamela.c

OBJ_DIR		=	obj/

SRC_DIR		=	src/

#########################################################
#                        FLAGS                          #
#########################################################

CFLAGS		=	-W -Wall -Wextra -fPIC

LDFLAGS		=	-lpam -lpam_misc -shared

#########################################################
#                        RULES                          #
#########################################################

BUILD_PRINT	=	\e[1;34mBuilding\e[0m \e[1;33m$<\e[0m

OBJS		=	$(patsubst %.c, ${OBJ_DIR}%.o, $(SRC))

FIRST		:=	$(shell test -d $(OBJ_DIR) || mkdir $(OBJ_DIR))

$(OBJ_DIR)%.o	:	$(patsubst %.c, ${SRC_DIR}%.c, %.c)
			@echo -e "$(BUILD_PRINT)" && $(CC) $(CFLAGS) -c $< -o $@

$(NAME)		:	$(OBJS)
			$(CC) $(OBJS) -o $(NAME) $(LDFLAGS)

all		:
			@$(MAKE) --no-print-directory $(NAME)

clean		:
			$(RM) $(OBJS) $(OBJ_DIR)

fclean		:	clean
			$(RM) $(NAME)

re		: 	fclean all

.PHONY		:	all clean fclean re
