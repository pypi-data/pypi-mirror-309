import React from "react"
import { createRoot } from 'react-dom/client';
import StpRenderer from "./StpRenderer"

const rootElem = document.getElementById("root");
if (!rootElem)
  throw new Error('Expected a element "root" to attach to, but not found in document');

const root = createRoot(rootElem);
root.render(<StpRenderer />);
