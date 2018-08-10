#include "Tree.hpp"
#include <vector>
#include <iostream>
Tree::Tree(float x, float y, float w, float h)
{
	bb = new Rect(x,y,w,h);
	//points.resize(4);
	std::cout << "end const" << std::endl;
	
}

Tree::~Tree()
{
}

void Tree::query(vector<MyPoint*>* res, Rect& bound){
	if(! bb->intersects(bound)){
		return;
	}
	queried = true;
	for(int i = 0; i<points.size(); i++){
		if(bound.contains(*points[i])){
			res->push_back(points[i]);
		}
	}
	if(ul != 0){
		ul->query(res,bound);
		ur->query(res,bound);
		dl->query(res,bound);
		dr->query(res,bound);

	}
}

void Tree::subdivide(){
	float x = bb->x, y = bb->y, w = bb->w, h = bb->h;
	ul = new Tree(x,y,w/2,h/2);
	ur = new Tree(x+w/2,y,w/2,h/2);
	dl = new Tree(x,y+h/2,w/2,h/2);
	dr = new Tree(x+w/2,y+h/2,w/2,h/2);
}


void Tree::draw(sf::RenderWindow& window, bool b){
	using namespace sf;
	if(b){
		RectangleShape r(Vector2f(bb->w,bb->h));
		r.setPosition(bb->x,bb->y);
		r.setOutlineColor(Color::White);
		if(queried){
			r.setOutlineColor(Color::Red);
			queried = false;
		}
		r.setFillColor(Color::Transparent);
		r.setOutlineThickness(0.5);
		window.draw(r);
	}
	
	for(int i =0;i<points.size();i++){
		CircleShape p(1);
		p.setPosition(points[i]->x,points[i]->y);
		p.setFillColor(Color::Green);
		window.draw(p);
	}
	
	
	if(ul != 0){
		ul->draw(window,b);
		ur->draw(window,b);
		dl->draw(window,b);
		dr->draw(window,b);
	}
	
	
}

void Tree::insert(MyPoint* p){
	if(!bb->contains(*p)){
		return;
	}
	
	if(points.size() < size){
		points.push_back(p);
		std::cout << "got point" << std::endl;
	}else{
		if(ur == 0){
			this->subdivide();
		}
		
		ur->insert(p);
		ul->insert(p);
		dr->insert(p);
		dl->insert(p);
	}
}