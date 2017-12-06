class Actor
{
	public:
		int x, y, w, h, area;
		int id, index;
		float aspectratio;
		int camera_pixel_center;
		int room_width, room_length;
		int room_X_position, room_Y_position;
		int  i_average_counter;
		int i_buf_x[11],i_buf_y[11],i_buf_W[11],i_buf_H[11],i_buf_AFC[11],i_buf_D[11];
		float f_average_X, f_average_Y, f_average_W, f_average_H,	f_average_AFC, f_average_D;		
		float  focal_length, physical_width, physical_distance_W, computed_distance;
		float physical_height, physical_distance_H, physical_aspect;
		int pixel_width;
		float angle_per_pixel, angle_from_center;
		Actor(void) ;
		void set_all(int new_x, int new_y, int new_w, int new_h, int new_id, int new_index);
		void set_x(int new_x);
		void set_y(int new_y);
		void set_w(int new_w);
		void set_h(int new_h);
		void set_id(int new_id);
		void set_focal_length();
		void set_index(int new_index);
		int get_index();
		int get_x();
		int get_y();
		int get_w();
		int get_h();
		int get_id();
		int get_area();
		int get_room_X_position();
		int get_room_Y_position();
		float get_focal_length();
		float get_aspectratio();
		void print_x() const;
		void print_y() const;
		void print_w() const;
		void print_h() const;
		void print_id() const;
		void print_index() const;
		void print_aspectratio() const;
		void print_angle_per_pixel() const;
	private:
		void compute_average_x(int count);
		void compute_average_y(int count);
		void compute_average_h(int count);
		void compute_average_w(int count);
		void compute_average_AFC(int count);
		void compute_average_D(int count);
};

