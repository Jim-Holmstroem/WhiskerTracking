
CPPFLAGS = -c -Wall `pkg-config --cflags cairo` # -pedantic                 
LIBS = `pkg-config --libs cairo`

all:
	g++ hellochipmunk.c -o hellochipmunk.o $(CPPFLAGS)
	g++ hellochipmunk.o libchipmunk.a -o hello $(LIBS)

linktest:
	g++ -c hellochipmunk.c -o hellochipmunk.o
	g++ hellochipmunk.o -o hello -lchipmunk 
run:
	./hello

clean:
	rm *.o hello
