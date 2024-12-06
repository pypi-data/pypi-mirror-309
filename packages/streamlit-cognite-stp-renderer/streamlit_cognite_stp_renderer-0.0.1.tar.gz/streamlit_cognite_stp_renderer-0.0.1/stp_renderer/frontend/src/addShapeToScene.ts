import {
  Box3,
  Camera,
  Color,
  Group,
  Mesh,
  MeshStandardMaterial,
  Object3D,
  Scene,
  Vector3,
} from "three"
import loadGeometry from "./loadGeometry"
import type { OpenCascadeInstance, TopoDS_Shape } from "opencascade.js"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"

const centerCameraAroundObject = (
  camera: Camera,
  controls: OrbitControls,
  object: Object3D
) => {
  // Compute the center point of the object
  const boundingBox = new Box3().setFromObject(object)
  const center = new Vector3()
  boundingBox.getCenter(center)

  // Optionally, compute the size of the bounding box to adjust the distance
  const size = new Vector3()
  boundingBox.getSize(size)
  const maxDimension = Math.max(size.x, size.y, size.z)

  // Position the camera
  const distanceMultiplier = 2 // Adjust this value to control how far the camera is
  const distance = maxDimension * distanceMultiplier
  camera.position.copy(center).add(new Vector3(0, distance, distance)) // Offset the camera
  camera.lookAt(center)

  // Update OrbitControls
  controls.target.copy(center)
  controls.update()
}

const addShapeToScene = async (
  openCascade: OpenCascadeInstance,
  shape: TopoDS_Shape,
  scene: Scene,
  camera: Camera,
  controls: OrbitControls
): Promise<void> => {
  const objectMat = new MeshStandardMaterial({
    color: new Color(0.9, 0.9, 0.9),
  })

  const group = new Group()
  const geometries = loadGeometry(openCascade, shape)
  geometries.forEach((geometry) => {
    group.add(new Mesh(geometry, objectMat))
  })
  centerCameraAroundObject(camera, controls, group)

  group.name = "shape"
  group.rotation.x = -Math.PI / 2
  scene.add(group)
}

export default addShapeToScene
