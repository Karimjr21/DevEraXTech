import { motion, AnimatePresence } from 'framer-motion';

export default function Lightbox({ item, onClose }) {
  return (
    <AnimatePresence>
      <motion.div
        key="overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-6"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={e=>e.stopPropagation()}
          className="relative max-w-2xl w-full glass rounded-xl overflow-hidden"
        >
          <img src={item.image} alt={item.title} className="w-full h-auto" />
          <div className="p-6 space-y-2">
            <h3 className="text-2xl font-bold text-gold">{item.title}</h3>
            <p className="text-xs text-gray-400">{item.category}</p>
            {item.url && (
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className="inline-block mt-2 px-3 py-1 border border-gold text-gold rounded-md text-xs font-semibold hover:bg-gold hover:text-dark transition-colors"
              >
                Visit Site
              </a>
            )}
            <button onClick={onClose} className="absolute top-2 right-2 px-3 py-1 bg-gold text-dark rounded-md text-xs font-semibold">Close</button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
