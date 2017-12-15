
#include <cstddef>
#include <SiftGPU.hpp>
#include <stdio.h>

#include <dlfcn.h>



int main(int argc, char **argv) {
	int retval;

	//char * s_argv[] = {"-fo", "-1",  "-v", "0"};
	char * s_argv[] = {"-v", "1", "-fo", "-1", "-tc2", "7680"};
	int s_argc = sizeof(s_argv)/sizeof(char*);

	SiftGPU sift;
	//sift.ParseParam(argc, argv);
	sift.ParseParam(s_argc, s_argv);

	int support = sift.CreateContextGL();

	if (support != SiftGPU::SIFTGPU_FULL_SUPPORTED) {
		printf("support: %d\n", support);
		return -1;
	}

	retval = sift.RunSIFT("/home/fassler/3dRecon/bikeModel/DJI_0083.ppm");
	//retval = sift.RunSIFT();
	if (retval) {
		sift.SaveSIFT("1.sift");
		//sift.SaveSIFT(NULL);
	} else {
		printf("sift.RunSIFT() failed:  %d\n", retval);
	}

	printf("Hello there!\n");

	return 0;
}


