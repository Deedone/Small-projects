#pragma once
#include "Point.hpp"


class Rect
{
public:
	float x,y,w,h;
	Rect(float x, float y, float w, float h);
	~Rect();
	
	bool contains(MyPoint&);
	bool intersects(Rect&);

};

