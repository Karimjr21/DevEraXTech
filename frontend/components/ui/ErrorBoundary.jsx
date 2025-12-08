import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) { return { hasError: true, error }; }
  componentDidCatch(err) { console.error('UI ErrorBoundary:', err); }
  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="text-gold text-xs">
          Something went wrong loading visuals.
          <pre className="mt-2 text-[10px] text-gray-400 whitespace-pre-wrap">{String(this.state.error)}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}
