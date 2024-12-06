import initOpenCascade, { OpenCascadeInstance } from "opencascade.js";

import { StreamlitComponentBase, withStreamlitConnection } from "streamlit-component-lib"
import React, { ReactNode, useEffect, useMemo, useRef, useState } from "react"
import * as THREE from 'three'
import setupThreeJSViewport from "./setupThreeJSViewport"
import addShapeToScene from "./addShapeToScene";
import loadStpOrIgesFile from "./loadStpOrIgesFile";
import { CogniteClient } from "@cognite/sdk";
import { QueryClient, QueryClientProvider, useMutation } from "@tanstack/react-query";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

type CogniteClientConfig = {
  token: string // TODO: fix a way to call back to Python to generate a new token
  project: string
  baseUrl: string
}

type StpRendererProps = {
  height: number;
  fileId: number;
  clientConfig: CogniteClientConfig;
}

type RenderState = {
  openCascadeInstance: OpenCascadeInstance;
  scene: THREE.Scene;
  camera: THREE.Camera;
  controls: OrbitControls;
};

const StpRenderer: React.FC<StpRendererProps> = ({ fileId, clientConfig, height }) => {
  const [renderState, setRenderState] = useState<RenderState | null>(null);
  const mountRef = useRef<HTMLDivElement>(null);

  const sdk = useMemo(() => new CogniteClient({
      project: clientConfig.project,
      baseUrl: clientConfig.baseUrl,
      appId: "streamlit-cognite-stp-renderer",
      getToken: async () => clientConfig.token,
  }), [clientConfig]);

  const {mutate: loadStpFileToScene} = useMutation({
    mutationFn: async (stpFileId: number) => {
      if (renderState === null) {
        return undefined;
      }
      const { openCascadeInstance, scene, camera, controls } = renderState;
      await loadStpOrIgesFile(
        openCascadeInstance,
        sdk,
        stpFileId,
        (openCascade, shape, scene) => addShapeToScene(openCascade, shape, scene, camera, controls), 
        scene,
      );
    },
  });

  useEffect(() => {
    if (renderState !== null) {
      loadStpFileToScene(fileId);
    }
  }, [fileId, renderState, loadStpFileToScene]);

  useEffect(() => {
    const container = mountRef.current;
    if (container === null) {
      return;
    }
    container.style.height = `${height}px`;

    const {scene, camera, controls} = setupThreeJSViewport(container);
    initOpenCascade().then((openCascade) => {
      setRenderState({ openCascadeInstance: openCascade, scene, camera, controls });
    });
    return () => {
      const object = scene?.getObjectByName("shape")
      if (object !== undefined) {
        scene?.remove(object);
      }
    }
  }, [mountRef, height]);
  
  return (
    <div ref={mountRef} style={{ width: "100%", height: "100%" }} />
  )
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      staleTime: 10 * 60 * 1000, // Pretty long, 600 seconds
    },
  },
});

class StreamlitComponent extends StreamlitComponentBase {
  public render = (): ReactNode => {
    const clientConfig: CogniteClientConfig = this.props.args['client_config'];
    const height: number = this.props.args["height"]
    const fileId: number = this.props.args['file_id'];

    return (
      <QueryClientProvider client={queryClient}>
        <StpRenderer 
          fileId={fileId}
          height={height}
          clientConfig={clientConfig} 
        />
      </QueryClientProvider>
    )
  }
}

export default withStreamlitConnection(StreamlitComponent)
