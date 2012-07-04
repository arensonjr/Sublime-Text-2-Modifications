COURSE  = /clear/www/htdocs/comp221

CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -g
LDLIBS  = -lnsl -lrt

PROG    = readjcf
OBJS    = readjcf.o csapp.o

all: $(PROG)

${PROG}: ${OBJS}
	${CC} ${CFLAGS} -o ${PROG} ${OBJS} ${LDLIBS}

csapp.o: ${COURSE}/src/csapp.c ${COURSE}/include/csapp.h
	${CC} ${CFLAGS} -I${COURSE}/include -c $< 

readjcf.o: readjcf.c ${COURSE}/include/csapp.h
	${CC} ${CFLAGS} -I${COURSE}/include -c $< 

clean:
	/bin/rm -f *.o ${PROG} core

.PHONY: clean
