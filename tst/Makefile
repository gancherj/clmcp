all:
	rm *.bc
	clang -emit-llvm -c *.c common/*.c
	llvm-link-3.4 *.bc -o t.bc
