#include "actor.h"
#define PI 3.14159265

/*
		int x, y, w, h, area;
		int id, index;
		float aspectratio;

		n/a int pixel_width;
		float angle_from_center;
		float physical_distance_H, physical_distance_W, computed_distance, physical_aspectratio, focal_length, physical_width, physical_height;
*/

Actor::Actor(void) {

//physical_aspect=physical_distance_W / physical_distance_H;

//x=r sin t
//y=r cos t
//at 50'' distant, an object 49 inchs wide touched both sides of the screen (or w=320)
// viewing_angle = 2 * (ATAN(24.5 / 50)) = 52.2 deg => 6.1291 pixels / deg

// .163155337 deg / pixel
	room_width=13;
	room_length=19;
	angle_per_pixel=.163155337 ;
	camera_pixel_center=160;
	physical_height=22;
	physical_width=19;  //19 inches wide
	physical_aspect=physical_width/physical_height;
	physical_distance_W=48;  // 4 ft (48 inces)
	pixel_width=161;
	set_focal_length();
};


void Actor::set_focal_length(){

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

	focal_length=(pixel_width * physical_distance_W) / physical_width ;

};

void Actor::set_all(int new_x,int new_y,int new_w,int new_h,int new_id,int new_index) {
	x=new_x;
	y=new_y;
	w=new_w;
	h=new_h;
	id=new_id;
	index=new_index;
	i_average_counter++;
	if (i_average_counter>9) {
		i_average_counter=0;
		compute_average_x(9);
		compute_average_y(9);
		compute_average_w(9);
		compute_average_h(9);

	angle_from_center = -(x-camera_pixel_center+w/2)*angle_per_pixel;
	physical_distance_W=(physical_width * focal_length) / w;
	physical_distance_H=(physical_height * focal_length) / h;
	if (aspectratio>physical_aspect) {
		computed_distance=physical_distance_W;
	} else {
		computed_distance=physical_distance_H;
	};
		computed_distance=physical_distance_W;  // This line must be removed to restore the aspect control for a shirt.

	room_X_position=(int(  computed_distance /12* sin( angle_from_center *PI/180)))+room_width/2 ;
	room_Y_position=int(  computed_distance /12* cos( angle_from_center*PI/180));

//		printf("angle_from_center new = %i %i%f  %i %i %f \n", index, id, angle_from_center,camera_pixel_center,w,angle_per_pixel );
//		printf("angle_from_center =%f %f\n", angle_from_center , PI);
//		printf("room_Y_position=%i \n", room_X_position);
	} else {
		i_buf_x[i_average_counter]=new_x;
		i_buf_y[i_average_counter]=new_y;
		i_buf_W[i_average_counter]=new_w;
		i_buf_H[i_average_counter]=new_h;
//		i_buf_AFC[i_average_counter]=new_AFC;
//		i_buf_D[i_average_counter]=new_D;
	};
//	printf("counter=%i \n", i_average_counter);
};

void Actor::set_x(int new_x) {
	x=new_x;
};
void Actor::set_y(int new_y) {
	y=new_y;
};
void Actor::set_h(int new_h) {
	h=new_h;
	area=h*w;
	if (h!=0) {
		aspectratio=(w / float(h));
	};
};
void Actor::set_w(int new_w) {
	w=new_w;
	area=h*w;
	if (h!=0) {
		aspectratio=(w / float(h));
	};
};
void Actor::set_id(int new_id) {
	id=new_id;
};
void Actor::set_index(int new_index) {
	index=new_index;
};

float Actor::get_aspectratio() {
	return aspectratio;
};

float Actor::get_focal_length(){
	return focal_length;
};

int Actor::get_index() {
	return index;
};

int Actor::get_id() {
	return id;
};

int Actor::get_area() {
	return area;
};

int Actor::get_x() {
	return x;
};

int Actor::get_y() {
	return y;
};

int Actor::get_w() {
	return w;
};

int Actor::get_h() {
	return h;
};

int Actor::get_room_X_position() {
	return room_X_position;
};

int Actor::get_room_Y_position() {
	return room_Y_position;
};

void Actor::print_x() const {
		printf("x=%i ", x);
};
void Actor::print_y() const {
		printf("y=%i ", y);
};
void Actor::print_id() const {
		printf("id=%i ",id);
};
void Actor::print_index() const {
		printf("index=%i ",index);
};
void Actor::print_w() const {
		printf("w=%i ", w);
};
void Actor::print_h() const {
		printf("h=%i ", h);
};
void Actor::print_aspectratio() const {
		printf("Aspect Ratio=%f ", aspectratio);
};
void Actor::print_angle_per_pixel() const {
		printf("angle_per_pixel=%f ", angle_per_pixel);
};


//Compute averages

void Actor::compute_average_x(int count){
		int i;
		int sum;
		sum=0;
		f_average_X=0;
		for (i=1; i<= count; ++i) { 
			sum=sum+i_buf_x[i];
		};
		f_average_X=sum/float (count);
	};

void Actor::compute_average_y(int count){
		int i;
		int sum;
		sum=0;
		f_average_Y=0;
		for (i=1; i<= count; ++i) { 
			sum=sum+i_buf_y[i];
		};
		f_average_Y=sum/float (count);
	};

void Actor::compute_average_w(int count){
		int i;
		int sum;
		sum=0;
		f_average_W=0;
		for (i=1; i<= count; ++i) { 
			sum=sum+i_buf_W[i];
		};
		f_average_W=sum/float (count);
	};

void Actor::compute_average_h(int count){
		int i;
		int sum;
		sum=0;
		f_average_H=0;
		for (i=1; i<= count; ++i) { 
			sum=sum+i_buf_H[i];
		};
		f_average_H=sum/float (count);
	};

void Actor::compute_average_AFC(int count){
		int i;
		int sum;
		sum=0;
		f_average_AFC=0;
		for (i=1; i<= count; ++i) { 
			sum=sum+i_buf_AFC[i];
		};
		f_average_AFC=sum/float (count);
	};

void Actor::compute_average_D(int count){
		int i;
		int sum;
		sum=0;
		f_average_D=0;
		for (i=1; i<= count; ++i) { 
			sum=sum+i_buf_D[i];
		};
		f_average_D=sum/float (count);
	};


