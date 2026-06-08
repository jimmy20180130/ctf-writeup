#include <stdio.h>

int main() {
	char FLAG[] = "DalCTF{test}";
	


	float fflag[sizeof(FLAG)];
	long lflag[sizeof(fflag)];

	int x = sizeof(FLAG);

	for(int i=0;i<x;i++){
	fflag[i] = (float) FLAG[i];
	fflag[i] = fflag[i] * fflag[i];
	lflag[i] = 0x5f3759df - ((*(long *)&fflag[i]) >> 1); // what the fuck?
	}

	x = x - 1;

	for(int i=0;i<x;i++){
	printf("\n%d", lflag[i]);
	};

	return 0;
}
