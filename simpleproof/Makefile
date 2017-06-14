saw: a.bc

a.bc:
	rm -f *.bc
	clang -emit-llvm -c *.c common/conv.c
	llvm-link-3.4 *.bc -o a.bc

run:
	clang *.c common/conv.c

