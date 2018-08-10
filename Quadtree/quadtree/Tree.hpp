#pragma once
#include <vector>
#include "Point.hpp"
#include "Rect.hpp"
#include "SFML/Graphics.hpp"

using namespace std;

class Tree
{
public:
	Tree* ur = 0,*ul = 0,*dr = 0,*dl = 0;
	Rect *bb;
	bool queried = false;
	int size = 4;
	vector<MyPoint*> points;
	
	void subdivide(void);
	void insert(MyPoint*);
	
	void query(vector<MyPoint*>*, Rect&);
	
	void draw(sf::RenderWindow&, bool);
	
	Tree(float, float, float, float);
	~Tree();

};

