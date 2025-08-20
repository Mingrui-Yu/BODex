import numpy as np
from visualizer import Visualizer
import torch
import trimesh as tm
import yaml

if __name__ == '__main__':
    # ------------- create visualizer -------------
    robot_urdf_path = 'src/curobo/content/assets/robot/leap_tac3d/leap_tac3d.urdf'
    mesh_dir_path = 'src/curobo/content/assets/robot/leap_tac3d/'
    robot_config_path = 'src/curobo/content/configs/robot/leap_tac3d.yml'
    visualize = Visualizer(robot_urdf_path=robot_urdf_path, mesh_dir_path=mesh_dir_path)

    hand_pose = torch.zeros((1, 3 + 4 + 16))
    hand_pose[:, 3] = 1.0
    hand_pose[:, 7:] = torch.rand_like(hand_pose[:, 7:])
    visualize.set_robot_parameters(hand_pose)
    robot_mesh = visualize.get_robot_trimesh_data(i=0, color=[0, 255, 0, 100])

    with open(robot_config_path, 'r') as file:
        robot_config = yaml.safe_load(file)

    sphere_meshes = []

    collision_spheres = robot_config['robot_cfg']['kinematics']['collision_spheres']
    for link_name, spheres in collision_spheres.items():
        for sphere in spheres:
            center = sphere['center']
            radius = sphere['radius']
            pos = visualize.current_status[link_name].transform_points(torch.tensor(center).reshape(1, 3))

            sphere_mesh = tm.creation.icosphere(subdivisions=4, radius=radius)
            transform = np.eye(4)
            transform[:3, 3] = pos.numpy()
            sphere_mesh.apply_transform(transform)
            sphere_mesh.visual.face_colors = [255, 0, 0, 255] 

            sphere_meshes.append(sphere_mesh)

    scene = tm.Scene(geometry=[robot_mesh] + sphere_meshes)
    scene.show()