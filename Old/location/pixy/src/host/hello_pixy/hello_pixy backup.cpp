//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string>
#include <string.h>
#include "pixy.h"
#include <math.h>       /* sin */

#define BLOCK_BUFFER_SIZE    25
#define PI 3.14159265

// Pixy Block buffer // 
struct Block blocks[BLOCK_BUFFER_SIZE];

static bool run_flag = true;
	int room_width, room_length;

void handle_SIGINT(int unused)
{
  // On CTRL+C - abort! //
	printf("stop");
  run_flag = false;
}

//begin MWE
int f_averageY (int i_inputY) 
{
	printf("Test");
	return i_inputY;
}
int getYfromBuf(char buf[128])
{
	std::string s;
	char t[20];
	int iPosOfY;
	int iPosOfWidth;
	int iReturnValue;
	
	s=buf;
	iPosOfY=s.find("y:")+3;
	iPosOfWidth=s.find("width:")-1;
	s=s.assign(s,iPosOfY,iPosOfWidth-iPosOfY);
	iReturnValue=atoi(s.c_str());
	//printf("Debug  ----- %s\n", s.c_str());
	return  iReturnValue;
}

int getXfromBuf(char buf[128])
{
	std::string s;
	int iPosOfX;
	int iPosOfY;
	int iReturnValue;
	
	s=buf;
	iPosOfX=s.find("x:")+3;
	iPosOfY=s.find("y:")-1;
	s=s.assign(s,iPosOfX,iPosOfY-iPosOfX);
	iReturnValue=atoi(s.c_str());
	//printf("Debug  ----- %s\n", s.c_str());
	return  iReturnValue;
}

int getSigfromBuf(char buf[128])
{
	std::string s;
	int iPosOfSigNum;
	int iPosOfX;
	int iReturnValue;
	
	s=buf;
	iPosOfSigNum=s.find("sig:")+5;
	iPosOfX=s.find("x:")-1;
	s=s.assign(s,iPosOfSigNum,iPosOfX-iPosOfSigNum);
	iReturnValue=atoi(s.c_str());
//	printf("Debug  ----- .%s.\n", s.c_str());
	return  iReturnValue;
}

int getWidthfromBuf(char buf[128])
{
	std::string s;
	int iPosOfWidthNum;
	int iPosOfHeight;
	int iReturnValue;
	
	s=buf;
	iPosOfWidthNum=s.find("width:")+7;
	iPosOfHeight=s.find("height:")-1;
	s=s.assign(s,iPosOfWidthNum,iPosOfHeight-iPosOfWidthNum);
	iReturnValue=atoi(s.c_str());
//	printf("Debug  ----- .%s.\n", s.c_str());

	return  iReturnValue;
}

int getHeightfromBuf(char buf[128])
{
	std::string s;
	int iPosOfHeightNum;
	int iPosOfEnd;
	int iReturnValue;
	
	s=buf;
	iPosOfHeightNum=s.find("height:")+8;
	iPosOfEnd=s.size();
	s=s.assign(s,iPosOfHeightNum,iPosOfEnd-iPosOfHeightNum);
	iReturnValue=atoi(s.c_str());
//	printf("Debug  ----- .%s.\n", s.c_str());

	return  iReturnValue;
}

void output_values(int id, int x, int y, int w, int h, float aspect, int area)
{
	int i;

	for(i = 0; i<10; ++i) { 
		printf("\n");
	}
	printf("id%i ", id);
	printf("X%i ", x);
	printf("Y%i ", y);
	printf("W%i ", w);
	printf("h%i ", h);
	printf("r%f ", aspect);
	printf("a%i \n", area);
}

void mapXY(int x, int y){
	int i,j;


	printf("x %i, y%i\n",x,y);
	printf("|");
	for(i = 1; i<=room_width; ++i) { 
		printf("-");
	}
	printf("|%i wide\n",room_width);
	for(i = 1; i<=room_length; ++i) { 
		printf("|");
		for(j = 1; j<=room_width; ++j) { 
			if ((i==y) && (j==x) )
				printf("X");
			else				
				printf(" ");
		}
		printf("|\n");
	}
	printf("|");
	for(i = 1; i<=room_width; ++i) { 
		printf("-");
	}
	printf("|%i long\n",room_length);
}

void process_buffer(char buf[128])
{
	int x, y, w, h, area, id, pixel_width;
	float aspect, focal_length, physical_width, physical_distance;
	int room_center;
	float angle_pixel_constant, angle_from_center;

	int return_value;

	id=getSigfromBuf(buf);
	x=getXfromBuf(buf);
	y=getYfromBuf(buf);
	w=getWidthfromBuf(buf);
	h=getHeightfromBuf(buf);
	area=w*h;
	aspect=(w / float(h));
	printf("%i ", id);
	printf("%i ", x);
	printf("%i ", y);
	printf("%i ", w);
	printf("%i ", h);
	printf("%i \n", aspect);
	

	output_values(id, x, y, w, h, aspect, area);

// 640 pix / 52 deg is 12.3 pix is 1 deg

//max view is 0 deg and area=3300 or x13 y9 
//                     52 deg and area=644  or x3 y29

// object is 1.5 ft wide
//  644 is 29 ft away = w23
// 1000 is 20 ft or w25
// 16000 is 5 ft or w130

// 3300 is 13 ft away = w
// 3300-644 = 2656 = 16 ft range 


//    dx         dy
//   -----  =  -----
//    sx         sy

// .03846 : 1.26087
//what is R?

// Perceived focal length
// Set P, D, and W
//P=pixel width
//D=distance
//W=width of object

//F=(PxD)/W

//F= Focal length (perceived)
//Now F & W is known

//D=(WxF)/P

physical_width=19;  //19 inches wide
physical_distance=48;  // 4 ft (48 inces)
pixel_width=161;

focal_length=(pixel_width * physical_distance) / physical_width ;

physical_distance=(physical_width * focal_length) / w;
//x=r sin t
//y=r cos t
//at 50'' distant, an object 49 inchs wide touched both sides of the screen (or w=320)
// viewing_angle = 2 * (ATAN(24.5 / 50)) = 52.2 deg => 6.1291 pixels / deg

// .163155337 deg / pixel
	angle_pixel_constant=.163155337 ;
	room_center=160;
	
	angle_from_center = (x-room_center)*angle_pixel_constant;
	x=(int(  physical_distance /12* sin( angle_from_center *PI/180)))+room_width/2 ;
	y=int(  physical_distance /12* cos( angle_from_center*PI/180));

	printf("afc=%f Dist=%f\n", angle_from_center, (physical_distance/12) );
//	printf("afc=%f Dist=%f Sin(afc)=%f Cos(afc)=%f\n", angle_from_center, (physical_distance/12),sin(angle_from_center*PI/180),(cos(angle_from_center*PI/180)) );

	mapXY(x,y);

	//return true;
}

// end MWE
int main(int argc, char * argv[])
{
  int      i = 0;
  int      index;
  int      blocks_copied;
  int      pixy_init_status;
  char     buf[128];
  int      return_value;

	room_width=13;
	room_length=19;

  // Catch CTRL+C (SIGINT) signals //
  signal(SIGINT, handle_SIGINT);

  printf("Hello Pixy:\n libpixyusb Version: %s\n", __LIBPIXY_VERSION__);

  // Connect to Pixy //
  pixy_init_status = pixy_init();

  // Was there an error initializing pixy? //
  if(!pixy_init_status == 0)
  {
    // Error initializing Pixy //
    printf("pixy_init(): ");
    pixy_error(pixy_init_status);

    return pixy_init_status;
  }

  // Request Pixy firmware version //
  {
    uint16_t major;
    uint16_t minor;
    uint16_t build;
    int      return_value;

    return_value = pixy_get_firmware_version(&major, &minor, &build);

    if (return_value) {
      // Error //

      printf("Failed to retrieve Pixy firmware version. ");
      pixy_error(return_value);

      return return_value;
    } else {
      // Success //
      printf(" Pixy Firmware Version: %d.%d.%d\n", major, minor, build);
    }
  }

#if 0
  // Pixy Command Examples //
  {
    int32_t response;
    int     return_value;

    // Execute remote procedure call "cam_setAWB" with one output (host->pixy) parameter (Value = 1)
    //
    //   Parameters:                 Notes:
    //
    //   pixy_command("cam_setAWB",  String identifier for remote procedure
    //                        0x01,  Length (in bytes) of first output parameter
    //                           1,  Value of first output parameter
    //                           0,  Parameter list seperator token (See value of: END_OUT_ARGS)
    //                   &response,  Pointer to memory address for return value from remote procedure call
    //                           0); Parameter list seperator token (See value of: END_IN_ARGS)
    //

    // Enable auto white balance //
    pixy_command("cam_setAWB", UINT8(0x01), END_OUT_ARGS,  &response, END_IN_ARGS);

    // Execute remote procedure call "cam_getAWB" with no output (host->pixy) parameters
    //
    //   Parameters:                 Notes:
    //
    //   pixy_command("cam_setAWB",  String identifier for remote procedure
    //                           0,  Parameter list seperator token (See value of: END_OUT_ARGS)
    //                   &response,  Pointer to memory address for return value from remote procedure call
    //                           0); Parameter list seperator token (See value of: END_IN_ARGS)
    //

    // Get auto white balance //
    return_value = pixy_command("cam_getAWB", END_OUT_ARGS, &response, END_IN_ARGS);

    // Set auto white balance back to disabled //
    pixy_command("cam_setAWB", UINT8(0x00), END_OUT_ARGS,  &response, END_IN_ARGS);
  }
#endif

  printf("Detecting blocks...\n");
  while(run_flag)
  {
    // Wait for new blocks to be available //
    while(!pixy_blocks_are_new() && run_flag); 

    // Get blocks from Pixy //
    blocks_copied = pixy_get_blocks(BLOCK_BUFFER_SIZE, &blocks[0]);

    if(blocks_copied < 0) {
      // Error: pixy_get_blocks //
      printf("pixy_get_blocks(): ");
      pixy_error(blocks_copied);
    }

if (blocks_copied>0){

     // Display received blocks //
    printf("My frame %d:\n", i);
    for(index = 0; index != blocks_copied; ++index) {    
       blocks[index].print(buf);
       //printf("  %s\n", buf);
	process_buffer(buf);
}
    }
    i++;
//	if (i>1000) {run_flag=false;}
  }
  pixy_close();
}
