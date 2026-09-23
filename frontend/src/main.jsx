import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { readEmbeddedPrerenderData } from '../lib/prerenderData';

// The HTML already contains prerendered markup for crawlers; the app renders
// fresh on top of it (createRoot replaces the container's contents).
createRoot(document.getElementById('root')).render(<App prerenderData={readEmbeddedPrerenderData()} />);
