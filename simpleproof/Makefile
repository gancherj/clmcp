saw:
	rm *.bc
	clang -emit-llvm -c *.c common/conv.c
	llvm-link-3.4 *.bc -o a.bc
	~/saw/bin/saw p.saw
