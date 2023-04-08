#include <iostream>
#include <cstdlib>
#include <cmath>
#include <istream>
#include <ostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <typeinfo>
#include <map>
using namespace std;



int main()

{




/// THESE ARE THE ONLY VALUES YOU INPUT INTO

double link1 = 1.195;
double link2 = 1.15;
double link3 = 0.608041;
double p1q1 =  122.27   *M_PI/180 ;
double p1q2 =  340.5  *M_PI/180;
double p2q1 =  174.71    *M_PI/180;
double p2q2 = 19.82 *M_PI/180;
double p3q1 = 69.42  *M_PI/180;
double p3q2 = 235.58 *M_PI/180;


// DON'T TOUCH ANYTHING AFTER THIS


double p1q3 = -60 * M_PI/180;
double p2q3 = 0 * M_PI/180;
double p3q3 = 45 * M_PI/180;





double link1_w = link1 * 4 * 9.81;
double link2_w = link2 * 2 * 9.81;
double link3_w = link3 * 1 * 9.81;
double gripper_w = 5 * 9.81;

//Everything for T1

double p1x1 = (link1/2)*cos(p1q1); 
double p1x2 = (link1*cos(p1q1)) + (link2/2)*cos(p1q2);
double p1x3 = (link1*cos(p1q1)) + (link2*cos(p1q2)) + (link3/2)*cos(p1q3);
double p1x4 = 0.75;


double t1 = -(p1x1*link1_w + p1x2*link2_w + p1x3*link3_w + p1x4*gripper_w);

// Everything for T2

double p2x1 = (link1/2)*cos(p2q1); 
double p2x2 = (link1*cos(p2q1)) + (link2/2)*cos(p2q2);
double p2x3 = (link1*cos(p2q1)) + (link2*cos(p2q2)) + (link3/2)*cos(p2q3);
double p2x4 = 0.5;


double t2 = -(p2x1*link1_w + p2x2*link2_w + p2x3*link3_w + p2x4*gripper_w);


//Everything for T3

double p3x1 = (link1/2)*cos(p3q1); 
double p3x2 = (link1*cos(p3q1)) + (link2/2)*cos(p3q2);
double p3x3 = (link1*cos(p3q1)) + (link2*cos(p3q2)) + (link3/2)*cos(p3q3);
double p3x4 = 0.2;


double t3 = -(p3x1*link1_w + p3x2*link2_w + p3x3*link3_w + p3x4*gripper_w);


//T_total

double t_total = sqrt(  pow(t1,2)  + pow(t2,2) + pow(t3,2)  );

cout << link1<< endl
    << link2<< endl
    << link3<< endl
    << p1q1 << endl 
    << p1q2 << endl
    << p2q1 << endl
    << p2q2 << endl
    << p3q1 << endl
    << p1q2 << endl
    << t1 <<endl
    << t2 << endl
    << t3 << endl


 <<  "t_total: " << t_total << endl
<< "x1" << p1x1 << endl
<< "x2" << p1x2 << endl
<< "x3" << p1x3 << endl
<< "x4" << p1x4 << endl





;








}