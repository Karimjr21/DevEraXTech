export default function Footer() {
  return (
    <footer className="border-t border-gray-800 mt-12">
      <div className="max-w-7xl mx-auto px-8 py-10 text-sm flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div className="font-semibold tracking-wide gold-gradient-text text-lg">DevEraX</div>
        <div className="flex-1 text-gray-400 leading-relaxed">
          Premium web & app experiences • Secure • Scalable • Pixel-perfect
        </div>
        <div className="text-gray-500">© {new Date().getFullYear()} DevEraX. All rights reserved.</div>
      </div>
    </footer>
  );
}
