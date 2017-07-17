run:
	clang *.c common/conv.c -g


saw:
	rm *.bc
	clang -emit-llvm -c *.c common/*.c
	llvm-link-3.4 *.bc -o a.bc

clean:
	rm *.bc common/*.bc a.out


