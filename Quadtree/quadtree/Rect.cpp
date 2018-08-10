#include "Rect.hpp"

Rect::Rect(float ax, float ay, float aw, float ah)
{
	x = ax;
	y = ay;
	w = aw;
	h = ah;
}

Rect::~Rect()
{
}

bool Rect::intersects(Rect& r){
	return !(	x > r.x + r.w ||
				x + w < r.x   ||
				y > r.y + r.h ||
				y + h < r.y);
}

bool Rect::contains(MyPoint& p)
{
	return (p.x > x &&
			p.x < x+w &&
			p.y > y &&
			p.y < y+h);
}
