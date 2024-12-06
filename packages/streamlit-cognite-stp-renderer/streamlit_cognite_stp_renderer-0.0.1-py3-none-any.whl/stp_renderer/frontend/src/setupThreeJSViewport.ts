import {
  AmbientLight,
  DirectionalLight,
  PerspectiveCamera,
  Scene,
  WebGLRenderer,
} from "three"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"

const setupThreeJSViewport = (container: HTMLElement) => {
  // Set up Three.js scene
  const scene = new Scene()
  const camera = new PerspectiveCamera(
    50, // FOV
    container.clientWidth / container.clientHeight, // Aspect ratio
    0.1, // Near plane
    1000 // Far plane
  )
  const renderer = new WebGLRenderer({ antialias: true })
  renderer.setSize(container.clientWidth, container.clientHeight)
  container.appendChild(renderer.domElement)

  // Set up scene lights
  scene.add(new AmbientLight(0x404040))
  const directionalLight = new DirectionalLight(0xffffff, 0.5)
  directionalLight.position.set(0.5, 0.5, 0.5)
  scene.add(directionalLight)

  camera.position.set(0, 50, 100)

  // Set up camera controls
  const controls = new OrbitControls(camera, renderer.domElement)
  controls.screenSpacePanning = true
  controls.target.set(0, 50, 0)
  controls.update()

  const animate = () => {
    requestAnimationFrame(animate)
    renderer.render(scene, camera)
  }
  animate()
  return { scene, camera, controls }
}

export default setupThreeJSViewport
