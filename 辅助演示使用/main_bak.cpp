#include <iostream>
#include <Eigen/Dense>

#include <vector>
#include <thread>
#include <pcl/features/moment_of_inertia_estimation.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/filters/crop_box.h>
#include <pcl/filters/crop_hull.h>
#include <pcl/surface/concave_hull.h>

pcl::PointXYZ getEndPoint(pcl::PointXYZ statPoint, float yaw, float length)
{
    Eigen::Affine3f transform = Eigen::Affine3f::Identity(); 
    transform.translation() << statPoint.x, statPoint.y, statPoint.z;
    transform.rotate(Eigen::AngleAxisf (yaw, Eigen::Vector3f::UnitZ()));

    pcl::PointCloud<pcl::PointXYZ>::Ptr basePoint(new pcl::PointCloud<pcl::PointXYZ>());
    pcl::PointXYZ p;
    p.x = length;p.y = 0;;p.z = 0;basePoint->points.push_back(p);

    pcl::PointCloud<pcl::PointXYZ>::Ptr transformedPoint (new pcl::PointCloud<pcl::PointXYZ> ());

    pcl::transformPointCloud (*basePoint, *transformedPoint, transform); //点云变换，矩形框最终落点

    return transformedPoint->points[0];
}


int main(int argc, char** argv)
{
	pcl::visualization::PCLVisualizer viewer;	

    pcl::PointXYZ o;
    o.x = 0;o.y = 0;o.z = 0;
    pcl::PointXYZ ox;
    ox.x = 50;ox.y = 0;ox.z = 0;
    pcl::PointXYZ oy;
    oy.x = 0;oy.y = 50;oy.z = 0;
    pcl::PointXYZ oz;
    oz.x = 0;oz.y = 0;oz.z = 50;
    viewer.addArrow(ox, o, 255, 0, 0, false, "arrowx");
    viewer.addArrow(oy, o, 0, 255, 0, false, "arrowy");
    viewer.addArrow(oz, o, 0, 0, 255, false, "arrowz");


    float px = 0;
    float py = 0;
    float pz = 0;
    float sx = 20;
    float sy = 10;
    float sz = 15;
    float yaw = 0;

    Eigen::AngleAxisf rotation_vector(yaw, Eigen::Vector3f(0, 0, 1));
    viewer.addCube(Eigen::Vector3f(px, py, pz), Eigen::Quaternionf(rotation_vector), sx, sy, sz, "11");
    viewer.setShapeRenderingProperties(pcl::visualization::PCL_VISUALIZER_REPRESENTATION, pcl::visualization::PCL_VISUALIZER_REPRESENTATION_WIREFRAME, "11");


    // pcl::PointXYZ sp;
    // sp.x = 80;sp.y = 80;sp.z = 80;

    // viewer.addSphere(sp, 3, 0, 255, 0);
    // viewer.setShapeRenderingProperties(pcl::visualization::PCL_VISUALIZER_OPACITY, 0.3, "sphere");





    while(!viewer.wasStopped())
    {
	   viewer.spinOnce(100);
    }

    return (0);
}