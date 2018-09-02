#include <SFML/Graphics.hpp>
#include <iostream>
#include <cstdlib>
#include <time.h>
#define WIDTH 800
#define HEIGHT 600
#define A 0
#define B 1
#define RANDOM 5//Set to -1 to disable
#define HSV 1 // 1 to use hsv 0 to use rgv
#define DT 1
using namespace std;
using namespace sf;

typedef struct {
    double r;       // a fraction between 0 and 1
    double g;       // a fraction between 0 and 1
    double b;       // a fraction between 0 and 1
} rgb;

typedef struct {
    double h;       // angle in degrees
    double s;       // a fraction between 0 and 1
    double v;       // a fraction between 0 and 1
} hsv;
rgb hsv2rgb(hsv in)
{
    double      hh, p, q, t, ff;
    long        i;
    rgb         out;

    if(in.s <= 0.0) {       // < is bogus, just shuts up warnings
        out.r = in.v;
        out.g = in.v;
        out.b = in.v;
        return out;
    }
    hh = in.h;
    if(hh >= 360.0) hh = 0.0;
    hh /= 60.0;
    i = (long)hh;
    ff = hh - i;
    p = in.v * (1.0 - in.s);
    q = in.v * (1.0 - (in.s * ff));
    t = in.v * (1.0 - (in.s * (1.0 - ff)));

    switch(i) {
    case 0:
        out.r = in.v;
        out.g = t;
        out.b = p;
        break;
    case 1:
        out.r = q;
        out.g = in.v;
        out.b = p;
        break;
    case 2:
        out.r = p;
        out.g = in.v;
        out.b = t;
        break;

    case 3:
        out.r = p;
        out.g = q;
        out.b = in.v;
        break;
    case 4:
        out.r = t;
        out.g = p;
        out.b = in.v;
        break;
    case 5:
    default:
        out.r = in.v;
        out.g = p;
        out.b = q;
        break;
    }
    return out;
}

float weights[3][3] = { {0.05, 0.2, 0.05},
                        {0.2, -1, 0.2},
                        {0.05, 0.2, 0.05}};


float DB(int i, int j){
    return 0.5;
    float d = ((i-HEIGHT/2)*(i-HEIGHT/2)) + ((j-WIDTH/2)*(j-WIDTH/2));

    return 1.4 - (0.05 +  d/(((HEIGHT/2)*(HEIGHT/2))+((WIDTH/2)*(WIDTH/2))));
}

float DA(int i, int j){
    return 1;
    float d = ((i-HEIGHT/2)*(i-HEIGHT/2)) + ((j-WIDTH/2)*(j-WIDTH/2));
    return 1.4 - (0.05 +  d/(((HEIGHT/2)*(HEIGHT/2))+((WIDTH/2)*(WIDTH/2))));
}



float feed(int i, int j){
    return 0.055;
    return 0.01 + 0.1 * ((float)i/HEIGHT);
}


float kill(int i, int j){
    return 0.062;
    return 0.055 + 0.01 * ((float)j/WIDTH);

}

float*** init_map(){
    float*** arr = new float**[HEIGHT];
    for(int i = 0;i<HEIGHT;i++){
        arr[i] = new float*[WIDTH];
        for(int j = 0; j<WIDTH;j++){
            arr[i][j] = new float[2];
            arr[i][j][A] = 1;
            if(rand()%100 < RANDOM){
                arr[i][j][B] = 1;
            }else{
                arr[i][j][B] = 0;
            }

        }
    }
    return arr;
}

void fill_pixels(Uint8* pixels, float*** arr){
    for(int i = 0; i<HEIGHT; i++){
        for(int j = 0;j<WIDTH; j++){
            if(HSV){
                hsv h;
                h.s = 1;
                h.v = 1-max((arr[i][j][A] - arr[i][j][B]),(float)0);
                h.h = max((arr[i][j][A] - arr[i][j][B]),(float)0) * 360;
                rgb a = hsv2rgb(h);
                pixels[(((i*WIDTH)+j)*4)+0] = a.r*255;
                pixels[(((i*WIDTH)+j)*4)+1] = a.g*255;
                pixels[(((i*WIDTH)+j)*4)+2] = a.b*255;
                pixels[(((i*WIDTH)+j)*4)+3] = 255;
            }else{
                Uint8 c = max((arr[i][j][A] - arr[i][j][B]),(float)0)*255;
                pixels[(((i*WIDTH)+j)*4)+0] = c;
                pixels[(((i*WIDTH)+j)*4)+1] = c;
                pixels[(((i*WIDTH)+j)*4)+2] = c;
                pixels[(((i*WIDTH)+j)*4)+3] = 255;
            }

        }
    }
}


float conv(float***arr, int index,int y, int x){
    float sum = 0;
    for(int i = 0;i<3;i++){
        for(int j = 0;j<3;j++){
            sum+= weights[i][j] * arr[(y-1)+i][(x-1)+j][index];
            //cout << (y-1)+i << " " << (x-1)+j << " "<<weights[i][j]<<endl;
        }
    }
    //cout << sum << endl;
    //float check = laplaceA(arr,y,x);
    //if(check != sum){
        //cout <<"BAD LAPLAC "<<check<<" "<<sum<<endl;
    //}
    return sum;
}



void update(float*** cur, float***prev){
    //cout << "UPDATE"<<endl;
    for(int i = 1;i<HEIGHT-1;i++){
        for(int j = 1;j<WIDTH-1;j++){
            //cout << i << " " << j << endl;
            float pa = prev[i][j][A];
            float pb = prev[i][j][B];
            cur[i][j][A] = pa + ((DA(i,j)*conv(prev,A,i,j)) - (pa*pb*pb) + (feed(i,j)*(1 - pa) )) * DT;
            cur[i][j][B] = pb + ((DB(i,j)*conv(prev,B,i,j)) + (pa*pb*pb) - ((kill(i,j)+feed(i,j))*pb)) * DT;


            cur[i][j][A] = max((float)0.0,min((float)1.0,cur[i][j][A]));
            cur[i][j][B] = max((float)0.0,min((float)1.0,cur[i][j][B]));
        }
    }
}


int main()
{
    srand(time(0));
    Clock clock;
    // Create the main window
    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "SFML window");
    sf::Image img;
    img.create(WIDTH, HEIGHT);
    Uint8 *pixels = new Uint8[WIDTH * HEIGHT * 4];
    sf::Texture texture;
    texture.create(WIDTH, HEIGHT);

    sf::IntRect r(0,0,WIDTH,HEIGHT);
    sf::Sprite sprite(texture,r);


    bool paused = true;
    float*** cur;
    float*** prev;
    cur = init_map();
    prev = init_map();
    cout << cur[0][0][0] << " "<< cur[0][0][1] << endl;

    for(int i = HEIGHT/2-20;i<HEIGHT/2+20;i++){
        for(int j = WIDTH/2-20;j<WIDTH/2+20;j++){
            prev[i][j][B] = 1;
        }
    }
	// Start the game loop
    while (window.isOpen())
    {
        float t = clock.restart().asSeconds();
        window.setTitle(to_string(1/t));
        //if((int)lol.getElapsedTime().asSeconds() % 100 > 50){
         //   lol1 = 0;
          //  lol2 = 1;
        //}else{
         //   lol1 = WIDTH;
          //  lol2 = -1;
        //}
        // Process events
        sf::Event event;
        while (window.pollEvent(event))
        {
            // Close window : exit
            if (event.type == sf::Event::Closed)
                window.close();
            if(event.type == Event::KeyPressed && event.key.code == Keyboard::Space)
                paused = !paused;
        }
        if(!paused)
       update(cur,prev);
       // cout << "SHALALALA" << endl;
        // Clear screen
       // window.clear();
        fill_pixels(pixels, cur);
        //img.create(WIDTH, HEIGHT,pixels);
        //texture.loadFromImage(img);
        //sprite.setTexture(texture);
        //sprite.setPosition(0,0);
        texture.update(pixels);
        window.draw(sprite);


        // Update the window
        window.display();
            if(!paused){
            float*** tmp = cur;
            cur = prev;
            prev = tmp;
        }
    }

    return 0;
}
