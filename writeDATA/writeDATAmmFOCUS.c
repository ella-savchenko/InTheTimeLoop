#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <time.h>



void setTimeout(int milliseconds){

    if (milliseconds <= 0) {

        return;
    }

    // a current time of milliseconds
    int milliseconds_since = clock() * 1000 / CLOCKS_PER_SEC;

    // needed count milliseconds of return from this timeout
    int end = milliseconds_since + milliseconds;

    // wait while until needed time comes
    do {
        milliseconds_since = clock() * 1000 / CLOCKS_PER_SEC;

	}while (milliseconds_since <= end);
}

//current timestamp in ms
u_int64_t getDate(){

    u_int64_t timestamp;
    struct timeval tv;
    gettimeofday(&tv,NULL);

    timestamp = (((u_int64_t)tv.tv_sec)*1000)+(tv.tv_usec/1000);
    return timestamp;

}




int main(){
	u_int64_t parameters=4;
	u_int64_t timestamp;
	u_int64_t xor1;
	u_int64_t xor2;
	

	int i;
	// loop = 1000s = 16.66 m
	for(i=0; i<100000; i++){	
	
		u_int64_t *ptr = mmap(NULL, parameters*sizeof(u_int64_t), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
		if(ptr == MAP_FAILED)
		{
			printf("Mapping failed\n");
			return 1;
		}
		

		timestamp = getDate();

		xor1 = 0x9488A80140AA2894;
		xor2 = 0x4A2552108054922A;

		
		ptr[0] = xor1 ^ xor2; 		//XOR = DEADFA11C0FEBABE -> BEBAFEC011FAADDE
		ptr[1] = i;
		ptr[2] = timestamp;
		ptr[3] = xor1 ^ xor2;
		
		//wait 10 ms
		setTimeout(10);
		
		printf("Written timestamps, iteration: %d\n", i);
	
		printf("%lX\n", ptr[2]);

	}
	
	


	// 1000 ms -> 1 s
	// wait 10 m
	setTimeout(600000);


	return 0;
}
