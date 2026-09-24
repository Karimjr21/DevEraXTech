// Framer Motion's animation features, split into their own chunk and loaded after first paint
// through <LazyMotion> in App.jsx. Components use the lightweight `m` element instead of `motion`.
import { domAnimation } from 'framer-motion';

export default domAnimation;
