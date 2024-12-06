import type {
  BRepMesh_IncrementalMesh_2,
  OpenCascadeInstance,
  TopoDS_Shape,
} from "opencascade.js"
import * as THREE from "three"

const loadGeometry = (
  openCascade: OpenCascadeInstance,
  shape: TopoDS_Shape
): THREE.BufferGeometry[] => {
  const geometries = []
  const ExpFace = new openCascade.TopExp_Explorer_1()
  for (
    ExpFace.Init(
      shape,
      openCascade.TopAbs_ShapeEnum.TopAbs_FACE as any,
      openCascade.TopAbs_ShapeEnum.TopAbs_SHAPE as any
    );
    ExpFace.More();
    ExpFace.Next()
  ) {
    const myShape = ExpFace.Current()
    const myFace = openCascade.TopoDS.Face_1(myShape)
    let inc: BRepMesh_IncrementalMesh_2 | undefined = undefined
    try {
      //in case some of the faces can not been visualized
      inc = new openCascade.BRepMesh_IncrementalMesh_2(
        myFace,
        0.1,
        false,
        0.5,
        false
      )
    } catch (e) {
      console.error("Face visualizing failed:", e)
      continue
    }

    const aLocation = new openCascade.TopLoc_Location_1()
    const myT = openCascade.BRep_Tool.Triangulation(
      myFace,
      aLocation,
      0 /* == Poly_MeshPurpose_NONE */
    )
    if (myT.IsNull()) {
      continue
    }

    const pc = new openCascade.Poly_Connect_2(myT)
    const triangulation = myT.get()

    const vertices = new Float32Array(triangulation.NbNodes() * 3)

    // write vertex buffer
    for (let i = 1; i <= triangulation.NbNodes(); i++) {
      const t1 = aLocation.Transformation()
      const p = triangulation.Node(i)
      const p1 = p.Transformed(t1)
      const baseIdx = 3 * (i - 1)
      vertices[baseIdx] = p1.X()
      vertices[baseIdx + 1] = p1.Y()
      vertices[baseIdx + 2] = p1.Z()
      p.delete()
      t1.delete()
      p1.delete()
    }

    // write normal buffer
    const myNormal = new openCascade.TColgp_Array1OfDir_2(
      1,
      triangulation.NbNodes()
    )
    openCascade.StdPrs_ToolTriangulatedShape.Normal(myFace, pc, myNormal)

    const normals = new Float32Array(myNormal.Length() * 3)
    for (let i = myNormal.Lower(); i <= myNormal.Upper(); i++) {
      const t1 = aLocation.Transformation()
      const d1 = myNormal.Value(i)
      const d = d1.Transformed(t1)

      const baseIdx = 3 * (i - 1)
      normals[baseIdx] = d.X()
      normals[baseIdx + 1] = d.Y()
      normals[baseIdx + 2] = d.Z()

      t1.delete()
      d1.delete()
      d.delete()
    }

    myNormal.delete()

    // write triangle buffer
    const orient = myFace.Orientation_1()
    const triangles = myT.get().Triangles()
    const triLength = triangles.Length() * 3
    const indices =
      triLength > 65535
        ? new Uint32Array(triLength)
        : new Uint16Array(triLength)

    for (let nt = 1; nt <= myT.get().NbTriangles(); nt++) {
      const t = triangles.Value(nt)
      let n1 = t.Value(1)
      let n2 = t.Value(2)
      let n3 = t.Value(3)
      if (orient !== openCascade.TopAbs_Orientation.TopAbs_FORWARD) {
        const tmp = n1
        n1 = n2
        n2 = tmp
      }

      const baseIdx = 3 * (nt - 1)
      indices[baseIdx] = n1 - 1
      indices[baseIdx + 1] = n2 - 1
      indices[baseIdx + 2] = n3 - 1
      t.delete()
    }
    triangles.delete()

    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3))
    geometry.setAttribute("normal", new THREE.BufferAttribute(normals, 3))

    geometry.setIndex(new THREE.BufferAttribute(indices, 1))
    geometries.push(geometry)

    pc.delete()
    aLocation.delete()
    myT.delete()
    inc.delete()
    myFace.delete()
    myShape.delete()
  }
  ExpFace.delete()
  return geometries
}

export default loadGeometry
