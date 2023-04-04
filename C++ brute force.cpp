#include <iostream>
#include <cmath>
#include <vector>

const double W1 = 4 * 9.81;
const double W2 = 2 * 9.81;
const double W3 = 1 * 9.81;
const double WL = 5 * 9.81;

bool ccw(double ax, double bx, double cx, double ay, double by, double cy)
{
    return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax);
}

bool intersect(double ax, double bx, double cx, double ay, double by, double cy, double dx, double dy)
{
    return ccw(ax, cx, dx, ay, cy, dy) != ccw(bx, cx, dx, by, cy, dy) and ccw(ax, bx, cx, ay, by, cy) != ccw(ax, bx, dx, ay, by, dy);
}

void check_lengths(double l1, double l2, double l3, std::vector<double> &min_res)
{
    std::vector<std::vector<double>> positions = {
        {0.75, 0.1, -60 * M_PI / 180, 1000000, 0, 0, 0},
        {0.5, 0.5, 0, 1000000, 0, 0, 0},
        {0.2, 0.6, 45 * M_PI / 180, 1000000, 0, 0, 0}};

    for (auto &pos : positions)
    {
        double x = pos[0];
        double y = pos[1];
        double q3 = pos[2];
        double x2 = x - l3 * std::cos(q3);
        double y2 = y - l3 * std::sin(q3);

        if (y2 >= 0)
        {
            double l12 = std::sqrt(x2 * x2 + y2 * y2);
            double angle = std::atan(y2 / x2);
            double a1 = std::acos((l1 * l1 + l12 * l12 - l2 * l2) / (2 * l1 * l12));
            std::vector<double> q1 = {angle + a1, angle - a1};
            std::vector<double> x1 = {l1 * std::cos(q1[0]), l1 * std::cos(q1[1])};
            std::vector<double> y1 = {l1 * std::sin(q1[0]), l1 * std::sin(q1[1])};
            std::vector<double> q2 = {std::acos((l1 * l1 + l2 * l2 - l12 * l12) / (2 * l1 * l2)) - M_PI + q1[0], std::acos((l1 * l1 + l2 * l2 - l12 * l12) / (2 * l1 * l2)) - M_PI + q1[1]};
            for (int i = 0; i < 2; ++i)
            {
                if (!intersect(0, x1[i], x2, 0, y1[i], y2, x, y))
                {
                    double T = (l1 / 2) * W1 * l1 * std::cos(q1[i]) + W2 * l2 * (l1 * std::cos(q1[i]) + l2 / 2 * std::cos(q2[i])) + W3 * l3 * (l1 * std::cos(q1[i]) + l2 * std::cos(q2[i]) + l3 / 2 * std::cos(q3)) + WL * x;

                    if (T < pos[3] && y1[i] >= 0)
                    {
                        pos[3] = T;
                        pos[4] = q1[i];
                        pos[5] = q2[i];
                    }
                }
            }
        }
    }

    double T_Total = std::sqrt(positions[0][3] * positions[0][3] + positions[1][3] * positions[1][3] + positions[2][3] * positions[2][3]);
    if (T_Total < min_res[3])
    {
        min_res[0] = l1;
        min_res[1] = l2;
        min_res[2] = l3;
        min_res[3] = T_Total;
        min_res[4] = positions[0][3];
        min_res[5] = positions[1][3];
        min_res[6] = positions[2][3];
        min_res[7] = positions[0][4];
        min_res[8] = positions[0][5];
        min_res[9] = positions[0][2];
        min_res[10] = positions[1][4];
        min_res[11] = positions[1][5];
        min_res[12] = positions[1][2];
        min_res[13] = positions[2][4];
        min_res[14] = positions[2][5];
        min_res[15] = positions[2][2];
    }
}

int main()
{
    std::vector<double> min_res(16, 1000000);
    min_res[0] = min_res[1] = min_res[2] = 0;

    int i = 0;
    
    for (double l1 = 0.005; l1 <= 5; l1 += (7 - 0.005) / 3000)
    {
        for (double l2 = 0.005; l2 <= 5; l2 += (7 - 0.005) / 3000)
        {
            for (double l3 = 0.005; l3 <= 0.84852813742; l3 += (0.84852813742 - 0.005) / 300)
            {
                if(i %100000 == 0)
                {
                    std::cout<<i<<std::endl;
                }
                i++;
                check_lengths(l1, l2, l3, min_res);
            }
        }
    }

    for (const auto &val : min_res)
    {
        std::cout << val << "  ";
    }
    std::cout << std::endl;

    return 0;
}