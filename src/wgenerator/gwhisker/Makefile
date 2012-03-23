
CPPFLAGS = -c -Wall  `pkg-config --cflags cairo` # -pedantic                 
LIBS = `pkg-config --libs cairo`


all:
	g++ jointtest.c -o jointest.o $(CPPFLAGS)
	g++ jointest.o libchipmunk.a -o jointtest $(LIBS)

hello:
	g++ hellochipmunk.c -o hellochipmunk.o $(CPPFLAGS)
	g++ hellochipmunk.o libchipmunk.a -o hello $(LIBS)

run:
	./jointtest

runhello:
	./hello

clean:
	rm *.o hello
