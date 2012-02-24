

all:
	g++ -c hellochipmunk.c -o hellochipmunk.o
	g++ hellochipmunk.o libchipmunk.a -o hello

linktest:
	g++ -c hellochipmunk.c -o hellochipmunk.o
	g++ hellochipmunk.o -o hello -lchipmunk 
run:
	./hello

clean:
	rm *.o hello
