import { CogniteClient } from "@cognite/sdk"
import type { OpenCascadeInstance, TopoDS_Shape } from "opencascade.js"
import { Scene } from "three"

const getFileData = async (
  sdk: CogniteClient,
  fileId: number
): Promise<string> => {
  const downloadLinks = await sdk.files.getDownloadUrls([{ id: fileId }])
  if (downloadLinks.length !== 1) {
    throw new Error(
      "Expected to get exactly one download URL. This should not happen"
    )
  }
  const response = await fetch(downloadLinks[0].downloadUrl)
  return response.text()
}

const loadStpOrIgesFile = async (
  openCascade: OpenCascadeInstance,
  sdk: CogniteClient,
  fileId: number,
  onSuccessfulLoad: (
    openCascade: OpenCascadeInstance,
    shape: TopoDS_Shape,
    scene: Scene
  ) => Promise<void>,
  scene: Scene
) => {
  const inputFiles = await sdk.files.retrieve([{ id: fileId }])
  if (inputFiles.length !== 1) {
    throw new Error("Expected to get exactly one file. This should not happen")
  }
  const inputFile = inputFiles[0]

  const stpData = await getFileData(sdk, fileId)
  const fileType = (() => {
    const fileExtension = inputFile.name.toLowerCase().split(".").pop()
    if (fileExtension === "stp" || fileExtension === "step") {
      return "step"
    }
    if (fileExtension === "igs" || fileExtension === "iges") {
      return "iges"
    }
    return undefined
  })()
  // Writes the uploaded file to Emscripten's Virtual Filesystem
  openCascade.FS.createDataFile(
    "/",
    `file.${fileType}`,
    stpData,
    true, // canRead
    true, // canWrite
    true // canOwn
  )

  // Choose the correct OpenCascade file parsers to read the CAD file
  if (fileType !== "step" && fileType !== "iges") {
    throw new Error(`Unsupported file type '${fileType}' was provided.`)
  }
  const reader =
    fileType === "step"
      ? new openCascade.STEPControl_Reader_1()
      : new openCascade.IGESControl_Reader_1()

  const readResult = reader.ReadFile(`file.${fileType}`) // Read the file
  if (readResult !== openCascade.IFSelect_ReturnStatus.IFSelect_RetDone) {
    console.error(
      "Something in OCCT went wrong while trying to read " + inputFile.name
    )
    return
  }

  console.log("File loaded successfully! Converting to OCC now...")
  reader.TransferRoots(new openCascade.Message_ProgressRange_1()) // Translate all transferable roots to OpenCascade
  const stepShape = reader.OneShape() // Obtain the results of translation in one OCCT shape
  console.log(`${inputFile.name} successfully converted. Triangulating...`)

  // Out with the old, in with the new!
  const obj = scene.getObjectByName("shape")
  if (obj !== undefined) {
    scene.remove(obj)
  }

  await onSuccessfulLoad(openCascade, stepShape, scene)
  console.log(`${inputFile.name} triangulated and added to the scene!`)

  // Remove the file when we're done (otherwise we run into errors on reupload)
  openCascade.FS.unlink(`/file.${fileType}`)
}

export default loadStpOrIgesFile
