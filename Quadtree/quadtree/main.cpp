#include <SFML/Graphics.hpp>
#include "Tree.hpp"
#include "Point.hpp"
#include "iostream"
using namespace sf;

int main()
{
    sf::RenderWindow window(sf::VideoMode(700, 700), "Majestic Window");
    Tree tree(0,0,700,700);
	bool draw = true;
	tree.insert(new MyPoint(5,5));
	tree.insert(new MyPoint(50,50));
	tree.insert(new MyPoint(50,500));
	tree.insert(new MyPoint(50,5));
	tree.insert(new MyPoint(500,500));
	::Rect bb(0,0,120,120);
	RectangleShape rect(Vector2f(120,120));
	rect.setOutlineColor(Color::Green);
	rect.setOutlineThickness(1);
	rect.setFillColor(Color::Transparent);
	vector<MyPoint*> pts;
	window.setFramerateLimit(60);
	
    while (window.isOpen())
    {
        sf::Event event;
        
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
            {
                window.close();
            }else if(event.type == Event::MouseButtonPressed){
				Vector2i x = Mouse::getPosition(window);
				tree.insert(new MyPoint (x.x,x.y));
				if(Mouse::isButtonPressed(Mouse::Button::Right)){
					draw = ! draw;
					std::cout << draw << std::endl;
				}
			}else if(event.type == Event::MouseMoved){
				if(Mouse::isButtonPressed(Mouse::Button::Left)){
					Vector2i x = Mouse::getPosition(window);
					tree.insert(new MyPoint (x.x,x.y));
				}
				
				Vector2i x = Mouse::getPosition(window);
				bb.x = x.x - 60;
				bb.y = x.y - 60;
				rect.setPosition(x.x-60, x.y-60);
				
			}
        }
        
		window.clear();
		
		tree.draw(window,draw);
		window.draw(rect);
		pts.clear();
		tree.query(&pts,bb);
		for(int i = 0; i< pts.size(); i++){
			CircleShape p(2);
			p.setPosition(pts[i]->x-1,pts[i]->y-1);
			p.setFillColor(Color::Red);
			window.draw(p);
		}
		
        window.display();
    }
}
