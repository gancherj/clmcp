all:
	clang -emit-llvm -c *.c common/*.c
	llvm-link *.bc -o a.bc

clean:
	rm *.bc common/*.bc a.out


