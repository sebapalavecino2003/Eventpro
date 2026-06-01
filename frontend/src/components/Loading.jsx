import './Loading.css';

export default function Loading({ text = 'Cargando...' }) {
  return (
    <div className="loading-container">
      <div className="loading-spinner" />
      <p className="loading-text">{text}</p>
    </div>
  );
}
