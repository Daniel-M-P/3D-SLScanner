import open3d as o3d
import numpy as np
import time 

inicio= time.time()

nube = o3d.io.read_point_cloud("Armadillo.ply")
print(nube)
nube, indices= nube.remove_statistical_outlier(nb_neighbors=10, std_ratio=4.0)

###checar dependiendo de la cantidad de puntos si se downea ono
print(nube)
nube = nube.voxel_down_sample(voxel_size=0.02)
print(nube)


nube.estimate_normals()
nube.orient_normals_consistent_tangent_plane(10)


#o3d.visualization.draw_geometries([nube], window_name="Nube filtrada",width=800, height=600,left=50, top=50,point_show_normal=False)

print('escoge: poisson, ball o alpha')
modo=input()
modo=modo.upper()
##### bajar resolucion pq pesa 150mb


if modo== 'POISSON':
    mesh, densities= o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(nube,depth=12)
    bounding_box = nube.get_oriented_bounding_box()
    mesh = mesh.crop(bounding_box)
    mesh.compute_vertex_normals()
    mesh = mesh.filter_smooth_simple(number_of_iterations=1)
elif modo== 'BALL':
    a=15
    radii=[a,a,a,a]
    mesh= o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(nube,o3d.utility.DoubleVector(radii))
    bounding_box = nube.get_oriented_bounding_box()
    mesh = mesh.crop(bounding_box)
    mesh.compute_vertex_normals()
    mesh = mesh.filter_smooth_simple(number_of_iterations=1)
elif modo=='ALPHA':
    a=30
    mesh= o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(nube,a)
    bounding_box = nube.get_oriented_bounding_box()
    mesh = mesh.crop(bounding_box)
    mesh.compute_vertex_normals()
    mesh = mesh.filter_smooth_simple(number_of_iterations=1)
else:
    print("malulo")

transcurrido = time.time() - inicio


mesh.compute_vertex_normals()
print(f"Tiempo transcurrido: {transcurrido:.2f} segundos")
# mesh.paint_uniform_color([1,1,1]) que pasa
o3d.visualization.draw_geometries([mesh])

ruta_salida = "Salidas\carro2.stl"
o3d.io.write_triangle_mesh(ruta_salida, mesh)