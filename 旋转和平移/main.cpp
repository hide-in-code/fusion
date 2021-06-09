#include <iostream>
#include <Eigen/Dense>

/**
 @File         : main.cpp
 @Date         : 2021-06-08
 @Author       : hejinlong
 @Description  : Description 
 */
int main()
{
    double px,py,pz;
    px = -0.0004217634029916384;
    py = -0.21683144949675118;
    pz = -1.0553445472201475;

    double rx,ry,rz;
    rx = 1.5518043975723739;
    ry = -0.003024701217351147;
    rz = 0.0014742699607357519;

    Eigen::Affine3f transform_2 = Eigen::Affine3f::Identity(); 
    transform_2.translation() << px, py, pz;
    transform_2.rotate(Eigen::AngleAxisf (rx, Eigen::Vector3f::UnitX()));
    transform_2.rotate(Eigen::AngleAxisf (ry, Eigen::Vector3f::UnitY()));
    transform_2.rotate(Eigen::AngleAxisf (rz, Eigen::Vector3f::UnitZ()));
    
    printf ("\n平移旋转矩阵:\n");
    std::cout << transform_2.matrix() << std::endl;
    return 0;
}