
CPPFLAGS = -c -Wall -I${HOME}/Chipmunk-6.0.3/include `pkg-config --cflags cairo` # -pedantic                 
LIBS = -L${HOME}/Chipmunk-6.0.3/src -lchipmunk `pkg-config --libs cairo`


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
