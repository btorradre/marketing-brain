import { X } from 'lucide-react';

export default function Modal({ title, children, onClose, footer, className }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className={`modal ${className || ''}`} onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{title}</h3>
          <button className="btn btn-ghost btn-sm" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
}
