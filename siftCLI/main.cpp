
#include <cstddef>
#include <vector>
#include <SiftGPU.hpp>
#include <stdio.h>
#include <assert.h>

using std::vector;

int main(int argc, char **argv) {
	int retval;
	int i;

	vector<float> descriptors1(1);
	vector<SiftGPU::SiftKeypoint> keys1(1);
	int num1 = 0;


	if (argc != 3) {
		fprintf(stderr, "usage: %s inputfile outputfile\n", argv[0]);
		return 0;
	}


	//const char * s_argv[] = {"-fo", "-1",  "-v", "0"};
	//const char * s_argv[] = {"-v", "1", "-fo", "-1", "-tc2", "7680"};

	// This seems to be about what VisualSfM is using:
	// -da is "darkness adaption", not documented

	//const char * s_argv[] = {"-v", "1",  "-fo", "0", "-da", "-tc2", "0", "-nomc"};
	const char * s_argv[] = {"-v", "1",  "-fo", "0", "-da", "-tc2", "7680", "-nomc"};
	int s_argc = sizeof(s_argv)/sizeof(char*);

	SiftGPU sift;
	//sift.ParseParam(argc, argv);
	sift.ParseParam(s_argc, (char **)s_argv);

	int support = sift.CreateContextGL();

	if (support != SiftGPU::SIFTGPU_FULL_SUPPORTED) {
		printf("support: %d\n", support);
		return -1;
	}

	retval = sift.RunSIFT(argv[1]);
	if (retval) {
		sift.SaveSIFT(argv[2]);
	} else {
		printf("sift.RunSIFT() failed:  %d\n", retval);
		return 1;
	}

	//get feature count
	num1 = sift.GetFeatureNum();

	// allocate memory
	keys1.resize(num1);
	descriptors1.resize(128*num1);
	sift.GetFeatureVector(&keys1[0], &descriptors1[0]);

	for (i=0; i<num1; ++i) {
		printf("i: %d, %.12f %.12f %.12f %.12f\n", i, keys1[i].x, keys1[i].y, keys1[i].s, keys1[i].o);
	}

	return 0;
}


